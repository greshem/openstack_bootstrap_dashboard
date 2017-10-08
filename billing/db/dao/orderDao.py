# -*- coding:utf-8 -*-
'''
Created on 2015年9月9日

@author: greshem
'''
from sqlalchemy import func
from billing.db.object.models import Order
from billing.db.sqlalchemy import session as sa
from oslo_log import log as logging
LOG = logging.getLogger(__name__)


class OrderDao():
    def __init__(self, order=None):
        self.order = order
    
    def getQuery(self, session=None):
        if not session:
            session = sa.get_session()
        return session.query(Order)
    
    def add(self, session=None):
        try:
            if not session:
                session = sa.get_session()
            session.add(self.order)
            session.flush()
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e
    
    def getOrderRechargeList(self, account_id=None, payment_type=None, started_at=None, ended_at=None, page_no=1, page_size=15,session=None):
        try:
            if not session:
                session = sa.get_session()
            count=session.execute(self._getOrderRechargeListCount(account_id, payment_type, started_at, ended_at)).first().total_sum
            rows=session.execute(self._getOrderRechargeListSql(account_id, payment_type, started_at, ended_at, (page_no-1)*page_size, page_size)).fetchall()
            result=[]
            if rows:
                for row in rows:
                    result.append(dict(zip(row.keys(), row.values())))
            session.close()
            return result,count
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e
        
    def maxNo(self, session=None):
        """取得最大的订单流水号"""
        try:
            if not session:
                session = sa.get_session()
            row = session.query(func.max(Order.order_no).label("max_no")).first()
            return row.max_no
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e
        
    def _getOrderRechargeListSql(self, account_id=None, payment_type=None, started_at=None, ended_at=None,offset=0,page_size=15):
        sql_recharge = "SELECT order.order_no,order.amount,order.status,order.payment_type,recharge.pay_at,order.account_id,recharge.remark FROM `order` JOIN recharge ON order.order_no=recharge.order_no WHERE order.status='pay_success'"
        sql_gift = "SELECT order.order_no,order.amount,order.status,order.payment_type,gift.gift_at AS pay_at,order.account_id,gift.remark FROM `order` JOIN gift ON order.order_no=gift.order_no WHERE order.status='pay_success'"
        sql= self.__getOrderRechargeListCondition(sql_recharge, sql_gift, account_id, payment_type, started_at, ended_at)
        return sql+' limit '+str(offset)+','+str(page_size)
    def _getOrderRechargeListCount(self,account_id=None, payment_type=None, started_at=None, ended_at=None):
        sql_recharge = "SELECT order.order_no,order.amount,order.status,order.payment_type,recharge.pay_at,order.account_id ,recharge.remark FROM `order` JOIN recharge ON order.order_no=recharge.order_no WHERE order.status='pay_success'"
        sql_gift = "SELECT order.order_no,order.amount,order.status,order.payment_type,gift.gift_at AS pay_at,order.account_id,gift.remark FROM `order` JOIN gift ON order.order_no=gift.order_no WHERE order.status='pay_success'"
        sql= self.__getOrderRechargeListCondition(sql_recharge, sql_gift, account_id, payment_type, started_at, ended_at)
        return "select count(*) as total_sum from ("+sql+") recharge"
    
    def __getOrderRechargeListCondition(self,sql_recharge,sql_gift,account_id=None, payment_type=None, started_at=None, ended_at=None):
        if account_id:
            sql_recharge += " and account_id='" + account_id + "'"
            sql_gift += " and account_id='" + account_id + "'"
#            sql_recharge = "SELECT order.order_no,order.amount,order.status,order.payment_type,recharge.pay_at FROM `order` JOIN recharge ON order.order_no=recharge.order_no WHERE order.status='pay_success'"
#            sql_gift = "SELECT order.order_no,order.amount,order.status,order.payment_type,gift.gift_at AS pay_at FROM `order` JOIN gift ON order.order_no=gift.order_no WHERE order.status='pay_success'"
        if started_at:
            sql_recharge += " and pay_at >='" + started_at + "'"
            sql_gift += " and gift_at >='" + started_at + "'"
        if ended_at:
            sql_recharge += " and pay_at <='" + ended_at + "'"
            sql_gift += " and gift_at <='" + ended_at + "'"
        if payment_type == 'recharge':
            return sql_recharge + " order by pay_at desc"
        if payment_type == 'gift':
            return sql_gift + " order by pay_at desc"
        return sql_recharge + " UNION " + sql_gift + " order by pay_at desc"

if __name__ == "__main__":
    orderDao = OrderDao()
    print orderDao.getOrderRechargeList("asdasjdjajsdjsajdj", "", "2013-01-01", '2016-01-01')
            
    
