# -*- coding:utf-8 -*-
'''
Created on 2016年2月25日

@author: greshem
线下转账的数据库操作
'''
from oslo_log import log as logging
from billing.db.sqlalchemy import session as sa
from billing.db.object.models import TransferInfo
LOG = logging.getLogger(__name__)
class TransferInfoDao():
    
    def __init__(self,tansferinfo=None):
        self.tansferinfo=tansferinfo
    
    def getQuery(self, session=None):
        if not session:
            session = sa.get_session()
        return session.query(TransferInfo)
    
    def add(self, session=None):
        '''添加线下转账信息'''
        try:
            if not session:
                session = sa.get_session()
            session.add(self.tansferinfo)
            session.flush()
        except Exception as e:
            session.close()
            LOG.error(str(e))
#            raise e
        