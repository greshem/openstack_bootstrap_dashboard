# -*- coding:utf-8 -*-
'''
Created on 2015年9月9日

@author: greshem
'''
from billing.db.object.models import InsteadRecharge
from billing.db.object.models import Account
from billing.db.sqlalchemy import session as sa
from oslo_log import log as logging
LOG = logging.getLogger(__name__)
class InsteadRechargeDao():
    def __init__(self, insteadRecharge):
        self.insteadRecharge = insteadRecharge
    
    def add(self, session=None):
        """添加代充值记录"""
        try:
            if session is None:
                session = sa.get_session()
            session.add(self.insteadRecharge)
            session.flush()
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e
        
    def upadte(self, values, session=None):
        """更新代充值记录"""
        try:
            if session is None:
                session = sa.get_session()
            session.begin()
            self.insteadRecharge = session.query(InsteadRecharge).filter(InsteadRecharge.instead_recharge_id == self.insteadRecharge.instead_recharge_id).first()
            self.insteadRecharge.update(values)
            session.commit()
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e
        
    
    def insteadRechargeAmount(self,session=None):
        try:
            if session is None:
                session = sa.get_session()
            session.begin()
            account_id=self.insteadRecharge.recharge.order.account_id
            amount = float(self.insteadRecharge.recharge.amount)
            account = session.query(Account).filter(Account.account_id == account_id).with_lockmode("update").first()
            cash_balance=account.cash_balance if account.cash_balance else 0
            account.cash_balance=float(cash_balance)+amount
            session.add(self.insteadRecharge)
            session.flush()
            self._make_frozen(account_id,session)
            session.flush()
            session.commit()
            session.close()
        except Exception as e:
            session.rollback()
            session.close()
            LOG.error(str(e))
            raise e
    
    def _make_frozen(self,account_id,session):
        '''解冻账户'''
        account=session.query(Account).filter(Account.account_id==account_id).first()
        if account.status=='frozen' and float(account.cash_balance)+float(account.gift_balance)+float(account.credit_line)>0:
            account.status='normal'
            account.frozen_status='normal'
            session.commit()
            from billing.emailsms.customer_communication import info_center
            infocenter=info_center()
            infocenter.unfreezen(account_id)
#    def InsteadRechargeAmount(self,account_id,session=None):
#        '''代充值'''
#        try:
#            if session is None:
#                session=sa.get_session()
#            session.begin()
#            account=session.query(Account).filter(Account.account_id==account_id).first()
#            account.gift_balance=float(account.gift_balance)+float(self.insteadRecharge.recharge.amount)
#            session.add(self.insteadRecharge)
#            session.flush()
#            session.commit()
#            session.close()
#        except Exception as e:
#            session.rollback()
#            session.close()
#            LOG.error(str(e))
#            raise e
            

if __name__=="__main__":
    session=sa.get_session()
    account_id="deyrteyrtyuryurtuty"
    temp=session.query(Account).filter(Account.account_id == account_id).with_lockmode("update").first()
    print dir(temp)