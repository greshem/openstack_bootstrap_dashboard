# -*- coding:utf-8 -*-
'''
Created on 2015年9月9日

@author: greshem
'''
from billing.db.object.models import Recharge
from billing.db.sqlalchemy import session as sa
from oslo_log import log as logging
LOG = logging.getLogger(__name__)
class RechargeDao():
    def __init__(self, recharge=None):
        self.recharge = recharge
    
    def add(self, session=None):
        """添加支付信息"""
        try:
            if not session:
                session = sa.get_session()
            session.add(self.recharge)
            session.flush()
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e
    
    def update(self,values,session=None):
        """更新支付信息"""
        try:
            if session is None:
                session=sa.get_session()
            session.begin()
            self.recharge = session.query(Recharge).filter(Recharge.recharge_id== self.recharge.recharge_id).first()
            self.recharge.update(values)
            session.commit()
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e



if __name__=="__main__":
    recharge=Recharge()
    recharge.recharge_id=1
    values={"status":"payed"}
    rechargeDao=RechargeDao(recharge)
    rechargeDao.update(values)
#    from billing.db.object.models import Order
#    order=Order()
#    order.account_id="asdasjdjajsdjsajdj"
#    order.amount=1000.00
#    order.order_no=100000001
#    order.payment_type="recharge"
#    order.status="ordered"
#    recharge=Recharge()
#    recharge.order=order
#    recharge.is_instead_recharge="False"
#    recharge.payment_way="alipay"
#    recharge.receive_account="1234567890"
#    recharge.status="paying"
#    recharge.order_no="100000000001"
#    rechargeDao=RechargeDao(recharge)
#    rechargeDao.add()
    