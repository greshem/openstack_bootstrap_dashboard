# -*- coding:utf-8 -*-
'''
Created on 2015年9月9日

@author: greshem
'''
from sqlalchemy import func

from billing.db.sqlalchemy import session as sa
from oslo_log import log as logging
LOG = logging.getLogger(__name__)


class cdnDomainDao():
    def __init__(self, cdnDomain=None):
        self.cdnDomain = cdnDomain
    
#    def getQuery(self, session=None):
#        if not session:
#            session = sa.get_session()
#        return session.query(cdnDomain)

    def getCDNDomainList(self, tenant_id, session=None):
        try:
            if not session:
                session = sa.get_session()
            rows=session.execute(self._getCDNDomainListSql(tenant_id)).fetchall()
            result=[]
            if rows:
                for row in rows:
                    result.append(dict(zip(row.keys(), row.values())))
            session.close()
            return result
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e
        
    def updateCdnDomainEnable(self,domain_id,enable,status,session=None):
        try:
            if session is None:
                session=sa.get_session()
            session.execute(self._updateCdnDomainEnableSql(enable,status),{'domain_id':domain_id,'enable':enable,'status':status})
            session.close()
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e


    def _getCDNDomainListSql(self, tenant_id=None):

        sql_cdndomain = "SELECT * FROM cdn.cdn_domain_manager_domain WHERE tenant_id = " + "'" +tenant_id + "'"

        return sql_cdndomain
    
    def _updateCdnDomainEnableSql(self,enable,status):
        sql_cdndomainenable="update cdn.cdn_domain_manager_domain set domain_id=domain_id"
        if enable:
            sql_cdndomainenable+=",Enable=:enable"
        if status:
            sql_cdndomainenable+=",status=:status"
        sql_cdndomainenable+= " where domain_id=:domain_id"
        return sql_cdndomainenable
    
    



# if __name__ == "__main__":
#     cdnDomainDao = cdnDomainDao()
#     print cdnDomainDao.getCDNDomainList("f3773d5249864d358e0b40fec6566228")
