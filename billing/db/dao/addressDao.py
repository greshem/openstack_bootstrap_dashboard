# -*- coding:utf-8 -*-
'''
Created on 2015-8-21

@author: greshem
地址数据库操作类
'''
from billing.db.object.models import Address
from billing.db.sqlalchemy import session as sa

class AddressDao():
    def __init__(self,address=None):
        self.address=address
        
    def getQuery(self, session=None):
        if not session:
            session = sa.get_session()
        return session.query(Address)
    
    def list(self,account_id,session=None):
        if not session:
            
            session=sa.get_session()
        query=session.query(Address)
        if account_id:
            query=query.filter(Address.account_id==account_id)
        query=query.filter(Address.status=="using")    
        return query.all()
    
    def add(self, session=None):
        if not session:
            session = sa.get_session()
        session.add(self.address)
        session.flush()
    
    def update(self,values,session=None):
        if not session:
            session = sa.get_session()
        session.begin()
        self.address = session.query(Address).filter(Address.address_id == self.address.address_id).first()
        self.address.update(values)
        session.commit()
    
    def detail(self,session=None):
        if not session:
            session = sa.get_session()
        self.address=session.query(Address).filter(Address.address_id == self.address.address_id).first()
        return self.address
        
            


