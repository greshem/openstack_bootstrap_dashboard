# -*- coding:utf-8 -*-
'''
Created on 2016-3-7

@author: yamin
Boss系统的用户数据库操作类
'''
from billing.db.sqlalchemy import session as sa
from billing.constant.sql import SQL
from billing.util.handlerUtil import *
from oslo_log import log as logging
LOG = logging.getLogger(__name__)
class BossUserDao():
    '''
    查询数据库
    '''
    def _query_user(self,codename,session=None):
        if not session:
            session = sa.get_session()
        query=session.execute(SQL.sql_boss_user_code,{"codename":codename})
        return query

    def _query_all(self,session=None):
        query=session.execute(SQL.sql_boss_user_all)
        return query

    def all_user(self,session=None):
        try:
            user_list=self._query_all().fetchall()
            return [row2dict(item) for item in user_list]
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e

    def sale_list(self,session=None):
        try:
            user_list=self._query_user("salesman").fetchall()
            return [row2dict(item) for item in user_list]
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e

    def salemanager_list(self,session=None):
        try:
            user_list=self._query_user("sales_manager").fetchall()
            return [row2dict(item) for item in user_list]
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e

    def admin_list(self,session=None):
        try:
            user_list=self._query_user("admin").fetchall()
            return [row2dict(item) for item in user_list]
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e

    def finance_list(self,session=None):
        try:
            user_list=self._query_user("finance").fetchall()
            return [row2dict(item) for item in user_list]
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e

    def dev_ops_list(self,session=None):
        try:
            user_list=self._query_user("dev_ops").fetchall()
            return [row2dict(item) for item in user_list]
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e

    def customer_service_list(self,session=None):
        try:
            user_list=self._query_user("customer_service").fetchall()
            return [row2dict(item) for item in user_list]
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e