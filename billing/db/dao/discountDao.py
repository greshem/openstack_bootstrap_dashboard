# -*- coding:utf-8 -*-
'''
Created on 2015-8-21

@author: greshem
折扣数据库操作类
'''
from billing.db.object.models import Discount,BillingItem
from billing.db.sqlalchemy import session as sa
from oslo_log import log as logging
from billing.util.handlerUtil import *
from billing.db.dao.billingItemDao import BillingItemDao

LOG = logging.getLogger(__name__)

class DiscountDao():
    def __init__(self, discount=None):
        self.discount = discount
        
    def getQuery(self, session=None):
        if not session:
            session = sa.get_session()
        return session.query(Discount)
    
    def add(self,session=None):
        try:
            if not session:
                session = sa.get_session()
            session.add(self.discount)
            session.flush()
            self.discount.billing_item
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e
    
    def getQueryByCondition(self,condition=None,session=None):
        '''条件查询'''
        if not session:
            session = sa.get_session()
        if condition is None:
            return session.query(Discount)
        query = session.query(Discount)
        if condition:
            billingItem = None
            for (attr,attrValue) in [(key,value)for (key,value) in condition.items()]:
                if attr=='account_id':
                    query=query.filter(Discount.account_id==attrValue)
                if attr=='billing_item_id':
                    query=query.filter(Discount.billing_item_id==attrValue)
                if attr=='region_id':
                    if not billingItem:
                        billingItem=BillingItem()
                    billingItem.region_id=attrValue
                if attr=='billing_item':
                    if not billingItem:
                        billingItem=BillingItem()
                    billingItem.billing_item=attrValue
            if billingItem:
                billingItemDao=BillingItemDao(billingItem)
                billingItem=billingItemDao.getBillingItem(session)
                query=query.filter(Discount.billing_item==billingItem)
   
#        if likeCondition:
#            for (attr,attrValue) in [(key,value)for (key,value) in likeCondition.items()]:
#                if attr=='username':
#                    query=query.filter(Discount.username.like('%'+attrValue+'%'))
        return query
    
    def getDiscountByCondition(self,condition=None,session=None):
        return self.getQueryByCondition(condition,session).first()
    
    def getDiscountDetail(self,condition=None,session=None):
        if not session:
            session = sa.get_session()
        if condition is None:
            return session.query(Discount)
        query = session.query(Discount)
        if condition:
            billingItem=None
            for (attr,attrValue) in [(key,value)for (key,value) in condition.items()]:
                if attr=='account_id':
                    query=query.filter(Discount.account_id==attrValue)
                if attr=='billing_item_id':
                    query=query.filter(Discount.billing_item_id==attrValue)
                if attr=='region_id':
                    if not billingItem:
                        billingItem=BillingItem()
                    billingItem.region_id=attrValue
                if attr=='billing_item':
                    if not billingItem:
                        billingItem=BillingItem()
                    billingItem.billing_item=attrValue
            if billingItem:
                billingItemDao=BillingItemDao(billingItem)
                billingItem=billingItemDao.getBillingItem(session)
                query=query.filter(Discount.billing_item==billingItem)
        row=query.first()
        if row:
            row.billing_item
        return row
    
    
    def update(self,values,session=None):
        try:
            if not session:
                session = sa.get_session()
            session.begin()
            self.discount = session.query(Discount).filter(Discount.discount_id == self.discount.discount_id).first()
            values={key:values[key] for key in values.keys() if key not in ('billing_item_id','account_id')}
            self.discount.update(values)
            session.commit()
            self.discount.billing_item
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e
    
    def list(self,account_id,region_id=None,session=None):
        if not session:
            session = sa.get_session()
        query= session.query(Discount)
        if account_id :
            query= query.filter(Discount.account_id == account_id)
        if region_id:
            billingItem=BillingItem()
            billingItem.region_id=region_id
            billingItemDao=BillingItemDao(billingItem)
            billingItems=billingItemDao.list(session)
            query=query.filter(Discount.billing_item_id.in_(billingItem.billing_item_id for billingItem in billingItems))
        rows=query.all()
        if rows:
            for row in rows:
                row.billing_item
        return rows
            
            
    
        
    

