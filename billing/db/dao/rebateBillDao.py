# -*- coding:utf-8 -*-
from billing.db.sqlalchemy import session as sa
from billing.db.object.models import Account,RebateBill
from billing.db.Pagination import Pagination
from oslo_log import log as logging
from billing.util.handlerUtil import *
from billing.constant.sql import SQL
import json
from billing.util.tzUtil import change2UTC,datetime2Str
import datetime
from billing.db.object.models import RebateBill,RebateSubBill,RebateBillItem

LOG = logging.getLogger(__name__)

class RebateBillDao():
    def __init__(self,rebateBill= None):
        self.rebateBill = rebateBill

    def getQuery(self,session=None):
        if not session:
            session = sa.get_session()
        return session.query(RebateBill)

    def checkRebateBill(self,account_id, started_at, ended_at, session=None):
        """检查返现账单是否生成"""
        try:
            if not session:
                session = sa.get_session()
            row = session.query(RebateBill).filter(RebateBill.account_id == account_id).filter(RebateBill.started_at >= started_at)\
            .filter(RebateBill.ended_at <= ended_at).first()
            if row:
                return True
            else:
                return False
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e

    def getQueryByCondition(self,condition=None,likeCondition=None,session=None):
        '''条件查询'''
        if not session:
            session = sa.get_session()
        if condition is None and likeCondition is None:
            return session.query(RebateBill)
        query = session.query(RebateBill)
        if condition:
            pass
        if likeCondition:
            for (attr,attrValue) in [(key,value) for (key,value) in likeCondition.items()]:
                if attr == 'no':
                    query = query.filter(RebateBill.no.like('%' + attrValue + '%'))
        return query

    def list(self,condition=None,likeCondition=None,session=None):
        '''按条件查询所有的返现账单'''
        if not session:
            session = sa.get_session()
        query = self.getQueryByCondition(condition,likeCondition)
        rows = query.all()
        return rows

    def getRebateBillByPage(self,query=None,page_no=1,page_size=15,edge_size=0,session=None):
        '''分页查询'''
        if not session:
            session = sa.get_session()
        if query is None:
            query = self.getQuery(session)
        pagination = Pagination(query)
        return pagination.paginate(page_no,page_size,edge_size)

    def add(self,session=None):
        try:
            if not session:
                session = sa.get_session()
            session.add(self.rebateBill)
            session.flush()
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e

if __name__=='__main__':
    rebateBillDao = RebateBillDao()
    likecondition = {'no':'no2'}
    rows = rebateBillDao.getQueryByCondition(likeCondition=likecondition)
    for item in rows:
        print item.rebate_bill_id