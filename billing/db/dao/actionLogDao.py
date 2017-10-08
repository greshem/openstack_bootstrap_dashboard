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
from billing.constant.sql import SQL
LOG = logging.getLogger(__name__)
import datetime
class ActionLogDao():
    def insert_log(self,log_dict):
        '''
        插入一条记录
        :return:
        '''
        session = sa.get_session()
        try:
            if log_dict.keys() == {"user_id","user_name","resource_name","resource_type","action_id","action_name","detail"}:
                log_dict["action_at"]=datetime.datetime.utcnow()
                session.execute(SQL.insert_log, log_dict)
                session.flush()
            else:
                return False
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e

    def list(self,info):

        query=self._list_query(info)
        records=query.fetchall()
        total=len(records)
        return [row2dict(row) for row in records],total

    def _list_query(self,info):
        session = sa.get_session()
        sql_sentence="select * from billing.action_log"
        sql_condition=[]
        condition=info.get("condition")
        page=info.get("page")
        params={}
        if condition.get("dateFrom") :
            params["dateFrom"]=condition.get("dateFrom")
            sql_condition.append("action_at >=:dateFrom")
        if condition.get("dateTo"):
            params["dateTo"]=condition.get("dateTo")
            sql_condition.append("action_at<=:dateTo")
        if condition.get("keyword"):
            params["keyword"]=condition.get("keyword")
            sql_condition.append("CONCAT_WS(' ',`user_name`,`resource_name`,`resource_type`,`action_name`,`detail`,`status`) like :keyword")
        condition=" and ".join(sql_condition)
        if condition:
            sql_sentence+=" where "+condition
        if page.get("offset") and page.get("page_size"):
            page_size=int(page.get("page_size"))
            offset=int(page.get("offset"))
            params["offset"]=offset
            params["page_size"]=page_size
            sql_sentence+=" LIMIT :page_size OFFSET :offset"
        query=session.execute(sql_sentence,params)
        return query
