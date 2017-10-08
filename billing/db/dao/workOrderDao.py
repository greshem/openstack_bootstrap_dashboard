# -*- coding:utf-8 -*-
'''
Created on 2015-12-18

@author: yamin
账户数据库操作类
'''
from billing.db.sqlalchemy import session as sa
from billing.db.object.models import *
from billing.db.Pagination import Pagination
from oslo_log import log as logging
from billing.util.handlerUtil import *
from billing.constant.sql import SQL
import json
from billing.util.tzUtil import change2UTC,datetime2Str
import datetime
from billing.util.handlerUtil import *
from billing.db.Pagination import Pagination

LOG = logging.getLogger(__name__)

class WorkBaseDao():
    model_class=""
    _session=None
    def __init__(self,object=None):
        '''
        :return:
        '''
        self.object=object

    def getObjFromDict(self,obj, jsonDict):
        if jsonDict and isinstance(obj,BillingBase):
            for (key, value) in jsonDict.items():
                if hasattr(obj, key):
                    obj[key] = value
                else:#是一个外键
                    if len(key.split("."))>2:
                        current_key=key.split(".")[0]
                        klass=eval(key.split(".")[1])
                        innerkey=key.split(".")[2]
                        foreign_obj=self.session.query(klass).filter_by(**{innerkey:value}).first()
                        if hasattr(obj,current_key):
                            obj[current_key]=foreign_obj.id
                        else:
                            return False
                    else:
                        return False
            return obj

    def getDictFromObj_nr(self,obj):
        return_dict={}
        if isinstance(obj,BillingBase):
            for key in obj.__dict__ :
                if key.startswith('_'):continue
                return_dict[key]=getattr(obj,key)
                if isinstance(return_dict[key],datetime):
                    return_dict[key]=return_dict[key].strftime("%Y-%m-%d %H:%M:%S")
        return return_dict

    def getDictFromObj_rp(self,obj,rp_list={}):
        return_dict=self.getDictFromObj_nr(obj)
        for key in rp_list:
            if hasattr(obj,key):
                sub_obj=getattr(obj,key)
                if isinstance(sub_obj,BillingBase):
                    if hasattr(sub_obj,rp_list[key]):
                        return_dict[key]=getattr(sub_obj,rp_list[key])
        return return_dict

    def query_info(self,info):
        '''
        对筛选条件进行清理，使得保留正确筛选条件，凡是筛选条件中包括None的都清除掉
        :param info:
        :return:
        '''
        join=info.pop("join") if "join" in info else {}
        filter_and=info.pop("filter_and") if "filter_and" in info else {}
        filter_expression=info.pop("filter_expression") if "filter_expression" in info else []
        order_by=info.pop("order_by") if "order_by" in info else []

        #清理join语句
        if None in join :join.pop(None)
        for key in join:
            #删除表达式列表中为空的语句
            expression_list=join[key]
            expression_list=[expression for expression in expression_list if type(expression).__name__!="NoneType"]
            join[key]=expression_list
        join={key:value for key ,value in join.items() if value}
        if join:info["join"]=join

        #清理filter_and语句,filter_and中的value对filter_and没有影响
        if None in filter_and:filter_and.pop(None)
        if filter_and:info["filter_and"]=filter_and

        #清理filter_expression语句
        filter_expression=[expression for expression in filter_expression if type(expression).__name__!="NoneType"]
        if filter_expression:info["filter_expression"]=filter_expression

        #清理order_by语句
        order_by=[expression for expression in order_by if type(expression).__name__!="NoneType"]
        if order_by:info["order_by"]=order_by

        return info

    def getDictFromObj(self,obj):
        '''
        包括relation,对象转dict
        :param obj:
        :return:
        '''
        return_dict={}
        if isinstance(obj,BillingBase):
            for key in [x for x in dir(obj) if not x.startswith('_') and x not in ["get", "iteritems", "metadata", "next", "save", "update"]]:
                value=getattr(obj,key)
                if isinstance(value,list):
                    return_dict[key]=[]
                    for item in value:
                        if isinstance(item,BillingBase):
                            return_dict[key].append(self.getDictFromObj_nr(item))
                        else:
                            return_dict[key].append(item)
                elif isinstance(value,BillingBase):
                    return_dict[key]=self.getDictFromObj_nr(value)
                else:
                    return_dict[key]=getattr(obj,key)
                    if isinstance(return_dict[key],datetime):
                        return_dict[key]=return_dict[key].strftime("%Y-%m-%d %H:%M:%S")
            return return_dict
        else:
            return obj

    @property
    def session(self):
        if not self._session:
            self._session=sa.get_session()
        return self._session

    def create(self,info):
        '''
        创建
        :return:
        '''
        try:
            obj=self.model_class()
            record=self.getObjFromDict(obj,info)
            self.session.add(record)
            self.session.flush()
            return self.getDictFromObj(record)
        except Exception as e:
            self.session.close()
            LOG.error(str(e))
            raise e

    def update(self,info):
        '''
        更新
        :return:
        '''
        try:
            key_params=info.pop("key")
            self.session.begin()
            record=self.session.query(self.model_class).filter_by(**key_params).first()
            record.update(info)
            self.session.commit()
            return self.getDictFromObj(record)
        except Exception as e:
            self.session.close()
            LOG.error(str(e))
            raise e

    def detail(self,info):
        '''
        详情
        :return:
        '''
        try:
            key_params=info.pop("key")
            record=self.session.query(self.model_class).filter_by(**key_params).first()
            return self.getDictFromObj(record)
        except Exception as e:
            self.session.close()
            LOG.error(str(e))
            raise e

    def delete(self,info):
        '''
        删除
        '''
        try:
            key_params=info.pop("key")
            self.session.query(self.model_class).filter_by(**key_params).delete()
            self.session.flush()
        except Exception as e:
            self.session.close()
            LOG.error(str(e))
            raise e


    def _list_query(self,query,info):
        info=self.query_info(info)
        try:
            if "join" in info:
                key,value=info["join"].items()[0]
                query=query.join(key).filter(*value)
            if "filter_and" in info:#使用语句来过滤
                sql_word=" and ".join([key for key in info["filter_and"]])
                params=dict([value for key,value in info["filter_and"].items() if value !=""])
                query=query.filter(sql_word).params(**params)
            if "filter_expression" in info:#使用表字段表达式过滤
                query=query.filter(*info["filter_expression"])
            if "order_by" in info:
                query=query.order_by(*info["order_by"])
            return query
        except Exception as e:
            return False

    def list(self,info):
        '''
        info
        列表
        :return:
        '''
        try:
            query=self.session.query(self.model_class)
            query=self._list_query(query,info)
            if "page" in info:
                records= Pagination(query).paginate(**info["page"])
                total=records.total
            else:
                records=query.all()
                total=len(records)
            return [self.getDictFromObj_nr(item) for item in records],total
        except Exception as e:
            LOG.error(str(e))
            raise e

class WorkOrderDao(WorkBaseDao):
    model_class=WorkOrder
    def list_by_me(self,info):
        '''
        所有被我处理的工单
        '''
        try:
            current_user=info["user"]
            query=self.session.query(self.model_class).filter(self.model_class.records.any(WorkOrderRecord.record_by==current_user))
            query=self._list_query(query,info)
            if "page" in info:
                records=Pagination(query).paginate(**info["page"])
                total=records.total
            else:
                records=query.all()
                total=len(records)
            return [self.getDictFromObj_rp(item,{"type":"name"}) for item in records],total
        except Exception as e:
            LOG.error(str(e))
            raise e
    def list(self,info):
        '''
        工单列表
        '''
        try:
            query=self.session.query(self.model_class)
            query=self._list_query(query,info)
            if "page" in info:
                records= Pagination(query).paginate(**info["page"])
                total=records.total
            else:
                records=query.all()
                total=len(records)
            return [self.getDictFromObj_rp(item,{"type":"name"}) for item in records],total
        except Exception as e:
            LOG.error(str(e))
            raise e
        
    def checkPaymentWorkOrder(self,workordertype,apply_by,apply_source,status,theme,apply_at):
        try:
            row=self.session.query(self.model_class).filter(self.model_class.workordertype==workordertype).filter(self.model_class.apply_by==apply_by)\
            .filter(self.model_class.apply_source==apply_source).filter(self.model_class.status==status).filter(self.model_class.theme.like('%'+theme+'%'))\
            .filter(self.model_class.apply_at>apply_at).first()
            if row:
                return False
            return True
        except Exception as e:
            LOG.error(str(e))
            raise e
class WorkOrderRecordDao(WorkBaseDao):
    '''
    工单评论
    '''
    model_class=WorkOrderRecord


class WorkOrderTypeDao(WorkBaseDao):
    '''
    工单类型
    '''
    model_class=WorkOrderType


if __name__=="__main__":
    WorkOrderDao().detail({"id":'3'})