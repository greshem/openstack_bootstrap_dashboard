# -*- coding:utf-8 -*-
'''
Created on 2015-8-21

@author: greshem
地址数据库操作类
'''
from billing.db.sqlalchemy import session as sa
from billing.constant.sql import SQL
class CommonDao():
    def __init__(self,address=None):
        pass
    
    def getRegionList(self,session=None):
        '''得到区域列表'''
        if session is None:
            session= sa.get_session()
        rows=session.execute(SQL.regionList).fetchall()
        result=[]
        for row in rows:
            result.append({'region_id':row.id,'region_desc':row.description}) 
        session.close()
        return result
    
    def checkProjectAdmin(self,user_id,session=None):
        '''判断是否是分销商用户'''
        if session is None:
            session= sa.get_session()
        row=session.execute(SQL.checkProjectAdmin,{'user_id':user_id}).fetchall()
        if row:
            return True
        return False
            


