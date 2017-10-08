# -*- coding:utf-8 -*-
'''
Created on 2015-12-18

@author: yamin
工单数据库操作类
'''
from billing.api import wsgi
from billing.hander import WorkOrder
from billing.hander.Recharge import getinsteadrechargelist
from billing.util.controllerUtil import *
import json
from oslo_config import cfg
CONF = cfg.CONF
from billing.util.tzUtil import change2UTC
from billing.db.dao.workOrderDao import *
#from billing.util.handlerUtil import *
import traceback
from sqlalchemy import desc
import random
import datetime
not_include=["records","type",]

class Controller(wsgi.Controller):

    def _check_params(self,json_dict,params={}):
        if params <= set(json_dict.keys()):
            return True
        else:
            return False

    def create_workorder_type(self,req, *args,**kwargs):
        '''
        创建工单类型
        :param req:
        :param args:
        :param kwargs:
        :return:
        '''
        try:
            info=req.json_body
            self._check_params(info,{"code","name","remark"})
            db_params={
                "name":info["name"],
                "code":info["code"],
                "remark":info["remark"],

            }
            record=WorkOrderTypeDao().create(db_params)
            return outSuccess("workordertype", record)
        except Exception as e:
            LOG.error(str(e))
            LOG.error(traceback.format_exc())
            return outError("创建工单类型失败！")

    def create_workorder(self,req, *args,**kwargs):
        '''
        创建工单
        '''
        try:
            info=req.json_body
            self._check_params(info,{"applier","type","theme","content","source"})
            import datetime
            workorder_no=generation()
            db_params={
                "apply_by":info["applier"],
                "theme":info["theme"],
                "content":info["content"],
                "workordertype.WorkOrderType.code":info["type"],
                "workorder_no":workorder_no,
                "status":"apply",#初始状态
                "apply_source":info["source"]
            }
            record=WorkOrderDao().create(db_params)
            return outSuccess("workorder", record)
        except Exception as e:
            LOG.error(str(e))
            LOG.error(traceback.format_exc())
            return outError("创建工单失败！")

    def create_workorder_record(self,req,*args,**kwargs):
        '''
        创建工单评论
        :param args:
        :param kwargs:
        :return:
        '''
        try:
            info=req.json_body
            self._check_params(info,{"workorderno","content","applier"})
            db_params={
                "workorder.WorkOrder.workorder_no":info["workorderno"],#订单编号
                "content":info["content"],
                "record_by":info["applier"],
            }
            if "status" in info:
                db_params["status"]=info["status"] #能够设置处理状态的为管理员
            record1=WorkOrderRecordDao().create(db_params)
            return_data={"workorderrecord":record1}
            if info.get("status",None):#更新订单状态
                db_params={
                    "key":{"workorder_no":info["workorderno"],},
                    "status":info["status"],
                    "lasthandled_by":info["applier"],
                }

                record2=WorkOrderDao().update(db_params)
                return_data.update({"workorder":record2})
            return_data.update({"success":"success"})
            return json.dumps(return_data)
        except Exception as e:
            LOG.error(str(e))
            LOG.error(traceback.format_exc())
            return outError("创建工单评论失败！")

    def update_workorder(self,req,*args,**kwargs):
        '''
        处理工单
        :param req:
        :param args:
        :return:
        '''
        try:
            info=req.json_body
            self._check_params(info,{"workorderno","status"})
            db_params={
                        "key":{
                            "workorder_no":info["workorderno"]
                        },
                        "status":info["status"]
                    }
            record=WorkOrderDao().update(db_params)
            return outSuccess("workorder", record)
        except Exception as e:
            LOG.error(str(e))
            LOG.error(traceback.format_exc())
            return outError("更新工单失败！")

    def workorder_detail(self,req,*args,**kwargs):
        '''
        工单详情
        :param req:
        :param args:
        :return:
        '''
        try:
            workorderno=kwargs.get('workorderno')
            db_params={
                "key":{"workorder_no":workorderno,}
            }
            record=WorkOrderDao().detail(db_params)
            return outSuccess("detail", record)
        except Exception as e:
            LOG.error(str(e))
            LOG.error(traceback.format_exc())
            return outError("获取工单失败！")

    def workorder_statics(self,req,*args,**kwargs):
        '''
        工单信息统计:各个状态工单数量
        :param req:
        :param args:
        :param kwargs:
        :return:
        '''
        try:
            apply_by=req.params.get('apply_by')
            info={
                "filter_expression":[
                    WorkOrder.apply_by==apply_by if apply_by else None,
                ],
            }
            records,total=WorkOrderDao().list(info)
            status_info={}
            for record in records:
                if record["status"] not in status_info:
                    status_info[record["status"]]=1
                else:
                    status_info[record["status"]]+=1
            return outSuccess("statics",status_info)
        except Exception as e:
            LOG.error(str(e))
            LOG.error(traceback.format_exc())
            return outError("统计工单信息失败！")

    def workorder_list(self,req,*args,**kwargs):
        '''
        工单列表
        :param req:
        :param args:
        :return:
        '''
        try:
            page_no = req.params.get('pageNo')
            page_size = req.params.get('pageSize')
            user=req.params.get('user')
            operate=req.params.get('operate')
            status=req.params.get('status')
            type=req.params.get('type')
            workorder_no=req.params.get('sno')
            permission=req.params.get('workorder_type_per').split(",") if req.params.get('workorder_type_per') else []
            apply_start=req.params.get('apply_start')
            apply_end=req.params.get('apply_end')
            apply_by=req.params.get('apply_by')
            source=req.params.get('source')
            info={
                "user":user,
                "join":{
                    WorkOrderType:[
                        WorkOrderType.code==type if type and type!="all" else None,
                        WorkOrderType.code.in_(permission) if permission else None,
                    ]
                },
                "filter_and":{
                  "workorder_no like :sno" if workorder_no else None:("sno","%"+workorder_no+"%" if workorder_no else ""),
                },
                "filter_expression":[
                    WorkOrder.status==status if status and status!="all" else None,
                    WorkOrder.apply_by==apply_by if apply_by else None,
                    WorkOrder.apply_at>=apply_start if apply_start else None,
                    WorkOrder.apply_at<=apply_end if apply_end else None,
                    WorkOrder.apply_source == source if source else None,
                ],

                "page":{
                    "page_no":page_no,
                    "page_size":page_size
                },
                "order_by":[
                    desc(WorkOrder.lasthandled_at),
                    desc(WorkOrder.apply_at)
                ]
            }

            # if type=="all" or not type:
            #     info.pop("join")
            if not (page_no and page_size):
                info.pop("page")
            else:
                info["page"]["page_no"]=int(page_no)
                info["page"]["page_size"]=int(page_size)
            # if not workorder_no:
            #     info.pop("filter_and")
            if not user:
                info.pop("user")
            # if status=="all" or  not status:
            #     info.pop("filter_expression")
            if user:
                records,total=WorkOrderDao().list(info)
            else:
                return outError("获取工单列表失败！")
                # if "join" not in info:
                #     info["join"]={}
                #     info["join"][WorkOrderType]=[WorkOrderType.code.in_(permission)]
                # else:
                #     info["join"][WorkOrderType].append(WorkOrderType.code.in_(permission))
            #     records,total=WorkOrderDao().list(info)
            # elif operate=="me_apply" and user:
                # if "filter_expression" not in info:
                #     info["filter_expression"]=[]
                # info["filter_expression"].append(WorkOrder.apply_by==user) #加入条件申请者
            #     records,total=WorkOrderDao().list(info)
            # elif operate=="all" or not operate and user:
            return json.dumps({"workorders":records,"total":total,"success":"success"})
        except Exception as e:
            LOG.error(str(e))
            LOG.error(traceback.format_exc())
            return outError("获取工单列表失败！")

    def workorder_type_list(self,req,*args,**kwargs):
        '''
        工单评论列表
        :param args:
        :param kwargs:
        :return:
        '''
        try:
            records,total=WorkOrderTypeDao().list({})
            return outSuccess("types",records)
        except Exception as e:
            LOG.error(str(e))
            LOG.error(traceback.format_exc())
            return outError("获取工单类型失败！")

    def workorder_record_list(self,req,*args,**kwargs):
        '''
        工单评论列表
        :param args:
        :param kwargs:
        :return:
        '''
        try:
            workorderno=kwargs.get('workorderno')
            info={
                "join":{
                    WorkOrder:[WorkOrder.workorder_no==workorderno]
                },
                "order_by":
                    [desc(WorkOrderRecord.record_at)]
            }
            if not workorderno:
                info.pop("join")
            records,total=WorkOrderRecordDao().list(info)
            return outSuccess("records", records)
        except Exception as e:
            LOG.error(str(e))
            LOG.error(traceback.format_exc())
            return outError("获取工单记录失败！")
def generation():
    order_id=datetime.datetime.strftime(datetime.datetime.utcnow(),'%y%m')
    for _ in range(10):
        order_id+=str(random.randint(0,9))
    return order_id
def create_resource():
    return wsgi.Resource(Controller())