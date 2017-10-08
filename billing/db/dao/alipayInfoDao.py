# -*- coding:utf-8 -*-
'''
Created on 2015年9月9日

@author: greshem
'''
from billing.db.object.models import AlipayInfo
from billing.db.object.models import Account
from billing.db.object.models import Order
from billing.db.object.models import Recharge
from billing.util.handlerUtil import getJsonFromObj
from billing.db.sqlalchemy import session as sa
from oslo_log import log as logging
LOG = logging.getLogger(__name__)
class AlipayInfoDao():
    def __init__(self,alipayInfo=None):
        self.alipayInfo=alipayInfo
        
    def add(self,session=None):
        """添加支付宝信息"""
        try:
            if session is None:
                session=sa.get_session()
            session.add(self.alipayInfo)
            session.flush()
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e
    
    def update(self,values,session=None):
        """更新支付宝信息"""
        try:
            if session is None:
                session=sa.get_session()
            session.begin()
            self.alipayInfo=session.query(AlipayInfo).filter(AlipayInfo.alipay_info_id==self.alipayInfo.alipay_info_id).first()
            self.alipayInfo.update(values)
            session.commit()
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e
    
    def rechargeAmount(self,session=None):
        """充值金额"""
        try:
            if session is None:
                session = sa.get_session()
            session.begin()
            amount = self.alipayInfo.amount
            status=self.alipayInfo.status
            order=session.query(Order).filter(Order.order_no==self.alipayInfo.order_no).first()
            account_id=order.account_id
            recharge=session.query(Recharge).filter(Recharge.order_no==self.alipayInfo.order_no).first()
            query=session.query(AlipayInfo).filter(AlipayInfo.order_no==self.alipayInfo.order_no)
            if self.alipayInfo.trade_no:
                query=query.filter(AlipayInfo.trade_no==self.alipayInfo.trade_no)
            alipayInfo=query.first()
            if status=='pay_success':
                if alipayInfo and alipayInfo.status=='pay_success':
                    session.commit()
                    session.close()
                    return "支付成功信息已经处理过了！"
                self._updateAccountCashAmount(account_id,amount,session)
                if alipayInfo:
                    alipayInfo.update(getJsonFromObj(self.alipayInfo))
                else:
                    self.alipayInfo.recharge_id=recharge.recharge_id
                    session.add(self.alipayInfo)
                '''更新order'''
                self._update_order(self.alipayInfo.order_no, status, session)
            elif status=='pay_error':
                if alipayInfo and alipayInfo.status=='pay_error':
                    session.commit()
                    session.close()
                    return "支付失败信息已经处理过了！"
                if alipayInfo:
                    alipayInfo.update(getJsonFromObj(self.alipayInfo))
                else:
                    self.alipayInfo.recharge_id=recharge.recharge_id
                    session.add(self.alipayInfo)
            '''更新recharge'''
            recharge.status=status
            recharge.pay_at=self.alipayInfo.pay_at
            session.flush()
            self._make_frozen(account_id, session)
            session.flush()
            session.commit()
            session.close()
        except Exception as e:
            session.rollback()
            session.close()
            LOG.error(str(e))
            raise e
        
    def _updateAccountCashAmount(self,account_id,amount,session):
        account = session.query(Account).filter(Account.account_id == account_id).with_lockmode("update").first()
        account.cash_balance = float(account.cash_balance)+amount
    
    def _update_order(self,order_no,status,session):
        order=session.query(Order).filter(Order.order_no==order_no).first()
        order.status=status
        
    def _make_frozen(self,account_id,session):
        '''解冻账户'''
        account=session.query(Account).filter(Account.account_id==account_id).first()
        if account.status=='frozen' and float(account.cash_balance)+float(account.gift_balance)+float(account.credit_line)>0:
            account.status='normal'
            account.frozen_status='normal'
            from billing.emailsms.customer_communication import info_center
            infocenter=info_center()
            infocenter.unfreezen(account_id)
        
        
#    def _update_recharge(self,order_no,status,pay_at,session):
#        recharge=session.query(Recharge).filter(Recharge.order_no).first()
#        recharge.status=status
#        recharge.pay_at=pay_at    
    
