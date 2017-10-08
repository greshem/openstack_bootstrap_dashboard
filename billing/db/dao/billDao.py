# -*- coding:utf-8 -*-
'''
Created on 2015-8-21

@author: greshem
账单数据库操作类
'''
from billing.db.object.models import Bill,BillItem
from billing.db.sqlalchemy import session as sa
from sqlalchemy import func
from oslo_log import log as logging
from billing.db.Pagination import Pagination
LOG = logging.getLogger(__name__)
import datetime

class BillDao():
    def __init__(self, bill=None):
        self.bill = bill
        
    def getQuery(self, session=None):
        if not session:
            session = sa.get_session()
        return session.query(Bill)
    
    def list(self, account_id, started_at=None, ended_at=None,page_no=1, page_size=15, edge_size=0,isBillItems=False,session=None, bill_type=None):
        """账单列表"""
        if not session:
            session = sa.get_session()
        query = session.query(Bill)
        if account_id:
            query = query.filter(Bill.account_id == account_id)
        if started_at:
            if isinstance(started_at, str):
                started_at=datetime.datetime.strptime(started_at, '%Y-%m-%d %H:%M:%S')
            query = query.filter(Bill.started_at >= started_at)
        if ended_at:
            if isinstance(ended_at, str):
                ended_at=datetime.datetime.strptime(ended_at, '%Y-%m-%d %H:%M:%S')
            query = query.filter(Bill.ended_at <= ended_at)
        if bill_type:
            query = query.filter(Bill.type == bill_type)
        pagination = Pagination(query)
        rows = pagination.paginate(page_no, page_size, edge_size)
        if isBillItems and rows:
            for row in rows:
                row.bill_items
        return rows

    
    def detail(self, session=None):
        """账单详情"""
        if not session:
            session = sa.get_session()
        query = session.query(Bill).filter(Bill.bill_id == self.bill.bill_id)
        row = query.first()
        if row:
            row.bill_items
        self.bill = row
    
    def bill_item_list(self,bill_id,session=None):
        if session is None:
            session=sa.get_session()
        query = session.query(BillItem.resource_type,func.sum(BillItem.amount).label("amount"),func.sum(BillItem.gift_amount).label('gift_amount'))\
        .filter(BillItem.bill_id==bill_id).group_by(BillItem.resource_type)
        rows= query.all()
        result=[]
        for row in rows:
            result.append({'resource_type':row.resource_type, 'amount':row.amount, 'gift_amount':row.gift_amount})
        return result
            
        
        
    def add(self, session=None):
        """创建账单"""
        try:
            if not session:
                session = sa.get_session()
            session.add(self.bill)
            session.flush()
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e
        
    def maxNo(self, session=None):
        """取得最大流水号"""
        try:
            if not session:
                session = sa.get_session()
            row = session.query(func.max(Bill.no).label("max_no")).first()
            return row.max_no
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e
        
    def checkBill(self, account_id, started_at, ended_at, session=None):
        """检查账单是否生成"""
        try:
            if not session:
                session = sa.get_session()
            row = session.query(Bill).filter(Bill.account_id == account_id).filter(Bill.started_at >= started_at)\
            .filter(Bill.ended_at <= ended_at).filter(Bill.type == 'cloud').first()
            if row:
                return True
            else:
                return False
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e

    def checkBill_naas(self, account_id, started_at, ended_at, session=None):
        """检查账单是否生成"""
        try:
            if not session:
                session = sa.get_session()
            row = session.query(Bill).filter(Bill.account_id == account_id).filter(Bill.started_at >= started_at)\
            .filter(Bill.ended_at <= ended_at).filter(Bill.type == 'naas').first()
            if row:
                return True
            else:
                return False
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e
        
