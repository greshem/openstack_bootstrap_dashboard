# -*- coding:utf-8 -*-
'''
Created on 2016年1月14日

@author： zhangaw
'''
from billing.db.object.models import Advert
from billing.db.sqlalchemy import session as sa
from oslo_log import log as logging
from billing.db.Pagination import Pagination
import datetime
LOG = logging.getLogger(__name__)
class AdvertDao():
    def __init__(self,advert=None):
        self.advert = advert

    def add(self,session=None):
        '''添加公告'''
        try:
            if session is None:
                session = sa.get_session()
            session.add(self.advert)
            session.flush()
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e

    def update(self,values,session=None):
        '''更新公告'''
        try:
            if session is None:
                session = sa.get_session()
            session.begin()
            self.advert = session.query(Advert).filter(Advert.advert_id == self.advert.advert_id).first()
            self.advert.update(values)
            session.commit()
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e

    def list(self,condition=None,session=None):
        '''获取公告列表'''
        if not session:
            session = sa.get_session()
        query = session.query(Advert)
        if condition:
            for (attr, attrValue) in [(key,value) for (key, value) in condition.items() ]:
                if attr == 'created_start':
                    query = query.filter(Advert.created_at >= attrValue)
                if attr == 'created_end':
                    query = query.filter(Advert.created_at <= attrValue)
                if attr == 'titlelike':
                    query = query.filter(Advert.title.like('%' + attrValue + '%'))
        rows = query.order_by(Advert.created_at.desc()).all()
        return rows

    def delete(self,session=None):
        '''删除某条公告'''
        try:
            if not session:
                session = sa.get_session()
            query = session.query(Advert).filter(Advert.advert_id == self.advert.advert_id)
            query.delete()
            session.flush()
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e
    def getadvertinfo(self,session=None):
        if not session:
            session = sa.get_session()
        query = session.query(Advert).filter(Advert.advert_id == self.advert.advert_id)
        row = query.first()
        return row
    def getvalidadvert(self,session=None):
        if not session:
            session = sa.get_session()
        today = datetime.datetime.now().strftime('%Y-%m-%d')+' 00:00:00'
        query = session.query(Advert).filter(Advert.ended_at >= today)
        query = query.filter(Advert.started_at <= today)
        rows = query.all()
        return rows

if __name__=='__main__':
    temp=AdvertDao()
    result = temp.getvalidadvert()
    for item in result:
        print item.started_at,item.ended_at