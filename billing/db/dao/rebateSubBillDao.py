# -*- coding:utf-8 -*-
from billing.db.sqlalchemy import session as sa
from billing.db.object.models import Account,RebateBill,RebateSubBill
from billing.db.Pagination import Pagination
from oslo_log import log as logging
from billing.util.handlerUtil import *
from billing.constant.sql import SQL
import json
from billing.util.tzUtil import change2UTC,datetime2Str
import datetime

LOG = logging.getLogger(__name__)

class RebateSubBillDao():
    def __init__(self,rebateBill= None):
        self.rebateBill = rebateBill
    def getQuery(self,session=None):
        if not session:
            session = sa.get_session()
        return session.query(RebateSubBill)
    def getQueryByCondition(self,condition=None,likeCondition=None,session=None):
        '''条件查询'''
        if not session:
            session = sa.get_session()
        if condition is None and likeCondition is None:
            return session.query(RebateSubBill)
        query = session.query(RebateSubBill)
        if condition:
            for (attr,attrValue) in [(key,value) for (key,value) in condition.items()]:
                if attr == 'rebate_bill_id':
                    query = query.filter(RebateSubBill.rebate_bill_id == attrValue)
        if likeCondition:
            for (attr,attrValue) in [(key,value) for (key,value) in likeCondition.items()]:
                pass
        return query
    def list(self,condition=None,likeCondition=None,session=None):
        '''按条件查询所有的返现账单'''
        if not session:
            session = sa.get_session()
        query = self.getQueryByCondition(condition,likeCondition)
        rows = query.all()
        return rows

    def getRebateSubBillByPage(self,query=None,page_no=1,page_size=15,edge_size=0,session=None):
        '''分页查询'''
        if not session:
            session = sa.get_session()
        if query is None:
            query = self.getQuery(session)
        pagination = Pagination(query)
        return pagination.paginate(page_no,page_size,edge_size)

if __name__=='__main__':
    rebateSubBillDao = RebateSubBillDao()
    likecondition = {'no':'no2'}
    rows = rebateSubBillDao.getQueryByCondition()
    for item in rows:
        print item.account_id