# -*- coding:utf-8 -*-
'''
Created on 2015-8-21

@author: greshem
计费项数据库操作类
'''
from billing.db.object.models import BillingItem
from billing.db.sqlalchemy import session as sa

class BillingItemDao():
    def __init__(self, billingItem=None):
        self.billingItem = billingItem
        
    def getQuery(self, session=None):
        if not session:
            session = sa.get_session()
        return session.query(BillingItem)
    
    def list(self,session=None):
        if not session:
            session = sa.get_session()
        query = session.query(BillingItem)
        if self.billingItem and self.billingItem.region_id:
            query = query.filter(BillingItem.region_id == self.billingItem.region_id)
        return query.all()
    
    def getBillingItem(self,session=None):
        if not session:
            session = sa.get_session()
        query = session.query(BillingItem)
        if self.billingItem and self.billingItem.region_id:
            query = query.filter(BillingItem.region_id == self.billingItem.region_id)
        if self.billingItem and self.billingItem.billing_item_id:
            query = query.filter(BillingItem.billing_item_id == self.billingItem.billing_item_id)
        if self.billingItem and self.billingItem.billing_item:
            query = query.filter(BillingItem.billing_item == self.billingItem.billing_item)
        return query.first()
    
    def update(self,values):
        session = sa.get_session()
        session.begin()
        self.billingItem = session.query(BillingItem).filter(BillingItem.billing_item_id == self.billingItem.billing_item_id).first()
        self.billingItem.update(values)
        session.commit()
        session.close()

    def get_price_for_nass(self, network_type, bandwidth, distance):
        sql = """
        SELECT bb.price
        FROM (
               SELECT
                 network_type,
                 cast(SUBSTRING_INDEX(distance, '-', 1) as UNSIGNED)   AS dist_lower,
                 cast(SUBSTRING_INDEX(distance, '-', -1) as UNSIGNED)  AS dist_upper,
                 cast(SUBSTRING_INDEX(bandwidth, '-', 1) as UNSIGNED)  AS bw_lower,
                 cast(SUBSTRING_INDEX(bandwidth, '-', -1) as UNSIGNED) AS bw_upper,
                 price
               FROM
                 (
                   SELECT
                     SUBSTRING_INDEX(billing_item, '_', 1)                           AS network_type,
                     substr(SUBSTRING_INDEX(billing_item, '_', 2), length('%s') + 2) AS distance,
                     SUBSTRING_INDEX(billing_item, '_', -1)                          AS bandwidth,
                     price
                   FROM billing_item
                   WHERE region_id = 'naas' AND billing_item LIKE '%s%%')
                   AS aa) AS bb
        WHERE %f >= dist_lower and %f <= dist_upper
              and
              %f >= bw_lower and %f <= bw_upper;
        """ % (network_type, network_type, distance, distance, bandwidth, bandwidth)
        return sa.get_session().execute(sql).first()



