# -*- coding:utf-8 -*-
from billing.db.sqlalchemy import session as sa
from billing.db.object.models import Account,RebateBill,RebateBillItem
from billing.db.Pagination import Pagination
from oslo_log import log as logging
from billing.util.handlerUtil import *
from billing.constant.sql import SQL
import json
from billing.util.tzUtil import change2UTC,datetime2Str
import datetime

LOG = logging.getLogger(__name__)

class RebateBillItemDao():
    def __init__(self,rebateBill= None):
        self.rebateBill = rebateBill
    def getQuery(self,session=None):
        if not session:
            session = sa.get_session()
        return session.query(RebateBillItem)
    def getQueryByCondition(self,condition=None,likeCondition=None,session=None):
        '''条件查询'''
        if not session:
            session = sa.get_session()
        if condition is None and likeCondition is None:
            return session.query(RebateBillItem)
        query = session.query(RebateBillItem)
        if condition:
            for (attr,attrValue) in [(key,value) for (key,value) in condition.items()]:
                if attr == 'region_id':
                    query = query.filter(RebateBillItem.region_id == attrValue)
                if attr == 'rebate_subbill_id':
                    query = query.filter(RebateBillItem.rebate_subbill_id == attrValue)
                if attr == 'resource_type':
                    query = query.filter(RebateBillItem.resource_type == attrValue)
        if likeCondition:
            pass
        return query
    def list(self,condition=None,likeCondition=None,session=None):
        '''按条件查询所有的返现账单'''
        if not session:
            session = sa.get_session()
        query = self.getQueryByCondition(condition,likeCondition)
        rows = query.all()
        return rows
    def getRebateBillItemByPage(self,query=None,page_no=1,page_size=15,edge_size=0,session=None):
        '''分页查询'''
        if not session:
            session = sa.get_session()
        if query is None:
            query = self.getQuery(session)
        pagination = Pagination(query)
        return pagination.paginate(page_no,page_size,edge_size)

if __name__=='__main__':
    rebateBillItemDao = RebateBillItemDao()
    query = rebateBillItemDao.getQueryByCondition()
    result = rebateBillItemDao.getRebateBillItemByPage(query)
    print result