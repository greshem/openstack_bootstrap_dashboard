# -*- coding:utf-8 -*-
'''
Created on 2015年9月9日

@author: greshem
'''
from billing.db.object.models import Gift,Order
from billing.db.object.models import Account
from billing.db.sqlalchemy import session as sa
from oslo_log import log as logging
LOG = logging.getLogger(__name__)
class GiftDao():
    def __init__(self, gift=None):
        self.gift = gift
    
    def add(self, session=None):
        """添加赠送记录"""
        try:
            if session is None:
                session = sa.get_session()
            session.add(self.gift)
            session.flush()
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e

    def isFirstGift(self,account_id,session=None):
        try:
            if session is None:
                session = sa.get_session()
            records=session.query(Gift).join(Order).filter(Gift.gift_by==self.gift.gift_by,Order.account_id==account_id).all()
            if records:
                return False
            else:
                return True
        except Exception as e:
            session.rollback()
            session.close()
            LOG.error(str(e))
            raise e

    def update(self, values, session=None):
        """更新赠送记录"""
        try:
            if session is None:
                session = sa.get_session()
            session.begin()
            self.gift = session.query(Gift).filter(Gift.gift_id == self.gift.gift_id).first()
            self.gift.update(values)
            session.commit()
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e
        
    def giftAmount(self, account_id, session=None):
        """赠送金额"""
        try:
            if session is None:
                session = sa.get_session()
            session.begin()
            amount = self.gift.amount
            account = session.query(Account).filter(Account.account_id == account_id).with_lockmode("update").first()
            if account.gift_balance==None:
                account.gift_balance=0
            account.gift_balance = float(account.gift_balance)+amount
            session.add(self.gift)
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
            from billing.emailsms.customer_communication import info_center
            infocenter=info_center()
            infocenter.unfreezen(account_id)
if __name__ == "__main__":
    giftDao = GiftDao()
    giftDao.giftAmount()
    
    
    
            
        
