# -*- coding:utf-8 -*-
'''
Created on 2015-8-21

@author: greshem
消费记录数据库操作类
'''
from sqlalchemy import func, or_,not_
from billing.db.object.models import Consumption
from billing.db.sqlalchemy import session as sa
import datetime
from billing.constant.sql import SQL
from billing.db.Pagination import Pagination, PageResult

class ConsumptionDao():
    def __init__(self, consumption=None):
        self.consumption = consumption
        
    def getQuery(self, session=None):
        if not session:
            session = sa.get_session()
        return session.query(Consumption)
    
    def getConsumptionSummary(self, account_id, started_at, ended_at, session=None):
        '''取得消费总额汇总'''
        if not session:
            session = sa.get_session()
        query = session.query(Consumption.account_id.label("account_id"), Consumption.resource_type.label("resource_type"), func.sum(Consumption.amount).label("amount_total"))
        if account_id:
            query = query.filter(Consumption.account_id == account_id)
        if started_at is not None:
            query = query.filter(Consumption.started_at >= started_at)
        if ended_at is not None :
            query = query.filter(Consumption.ended_at <= ended_at)
        query = query.group_by(Consumption.resource_type)
        row_totals = query.all()
        query = query.filter(Consumption.discount_by == 'gift_balance')
        row_gifts = query.all()
        result = []
        for row_total in row_totals:
            amount_gift_total = 0
            for row_gift in row_gifts:
                if row_total.resource_type == row_gift.resource_type:
                    amount_gift_total = row_gift.amount_total
            result.append({'account_id':row_total.account_id, 'resource_type':row_total.resource_type, 'amount_total':row_total.amount_total, 'amount_gift_total':amount_gift_total})
        session.close()
        return result
    
    def getAmountSummary(self, account_id, started_at, ended_at, session=None):
        if not session:
            session = sa.get_session()
        query = session.query(func.sum(Consumption.amount).label("amount_total"), func.sum(Consumption.standard_amount).label("standard_amount_total"))
        if account_id:
            query = query.filter(Consumption.account_id == account_id)
        if started_at is not None:
            query = query.filter(Consumption.started_at >= started_at)
        if ended_at is not None :
            query = query.filter(Consumption.ended_at <= ended_at)
        row_amount = query.first()
        query_gift = query.filter(Consumption.discount_by == 'gift_balance')
        row_gift = query_gift.first()
        session.close()
        return {'amount_total':row_amount.amount_total, 'standard_amount_total':row_amount.standard_amount_total, 'amount_gift_total':row_gift.amount_total}

    def getAmountTotal(self, account_id, started_at, ended_at, region_id=None, resource_type=None, page_no=1, page_size=15, edge_size=0, session=None):
        '''取得消费明细汇总'''
        if not session:
            session = sa.get_session()
        query = session.query(Consumption.account_id.label("account_id"), Consumption.resource_id.label("resource_id"),Consumption.sum.label('sum'), Consumption.resource_name.label("resource_name"), Consumption.region_id.label("region_id")\
                              , Consumption.resource_type.label("resource_type"), Consumption.parent_id.label("parent_id"), func.sum(Consumption.amount).label("amount_total"), func.max(Consumption.ended_at).label("ended_at"), func.min(Consumption.started_at).label("started_at"))
        if account_id:
            query = query.filter(Consumption.account_id == account_id)
        if region_id:
            query = query.filter(Consumption.region_id == region_id)
        if resource_type:
            if resource_type not in ('instance', 'cdn'):
                query = query.filter(Consumption.resource_type == resource_type)
            else:
                if resource_type == 'instance':
                    query = query.filter(or_(Consumption.resource_type == resource_type, Consumption.resource_type == 'cpu', Consumption.resource_type == 'memory'))
                if resource_type=='cdn':
                    query = query.filter(or_(Consumption.resource_type == 'cdnflow', Consumption.resource_type == 'cdnbandwidth'))
        if started_at is not None:
            query = query.filter(Consumption.started_at >= started_at)
        if ended_at is not None :
            query = query.filter(Consumption.ended_at <= ended_at)
        query_instance=query
        query = query.filter(not_(Consumption.resource_type=='cpu')).filter(not_(Consumption.resource_type=='memory'))
        
#        rows = query.group_by(Consumption.account_id, Consumption.resource_id).order_by(Consumption.region_id).all()
        query = query.group_by(Consumption.account_id, Consumption.resource_id).order_by(Consumption.region_id)
        pagination = Pagination(query)
        result = pagination.paginate(page_no, page_size, edge_size)
        pageResult = PageResult(result.total, page_no, page_size, edge_size)
        for row in result:
            pageResult.append({'account_id':row.account_id, 'resource_id':row.resource_id, 'resource_name':row.resource_name if row.resource_name else row.sum\
                           , 'region_id':row.region_id, 'resource_type':row.resource_type, 'parent_id':row.parent_id\
                           , 'amount_total':row.amount_total, 'started_at':row.started_at, 'ended_at':row.ended_at})
            if row.resource_type=='instance':
                query_cpu_memory=query_instance
                query_cpu_memory=query_cpu_memory.filter(Consumption.parent_id==row.resource_id)
                query_cpu_memory=query_cpu_memory.group_by(Consumption.account_id, Consumption.resource_id).order_by(Consumption.region_id)
                cpu_memory_rows=query_cpu_memory.all()
                for cpu_memory_row in cpu_memory_rows:
                    pageResult.append({'account_id':cpu_memory_row.account_id, 'resource_id':cpu_memory_row.resource_id, 'resource_name':cpu_memory_row.resource_name\
                           , 'region_id':cpu_memory_row.region_id, 'resource_type':cpu_memory_row.resource_type, 'parent_id':cpu_memory_row.parent_id\
                           , 'amount_total':cpu_memory_row.amount_total, 'started_at':cpu_memory_row.started_at, 'ended_at':cpu_memory_row.ended_at})
                
        session.close()
        return pageResult
    
    def getAmountTotal_new(self, account_id, started_at, ended_at, session=None):
        if not session:
            session = sa.get_session()
#        if isinstance(started_at, datetime.date):
#            started_at=datetime.date.strftime(started_at,'%Y-%m-%d')
#        if isinstance(ended_at, datetime.date):
#            ended_at=datetime.date.strftime(ended_at,'%Y-%m-%d')
        query = session.execute(SQL.bill, {'account_id':account_id, 'started_at':started_at, 'ended_at':ended_at})
        rows = query.fetchall()
        result = []
        for row in rows:
            result.append({'account_id':row.account_id, 'resource_id':row.resource_id, 'resource_name':row.resource_name\
                           , 'region_id':row.region_id, 'resource_type':row.resource_type, 'parent_id':row.parent_id\
                           , 'amount_total':row.amount_total, 'started_at':row.started_at, 'ended_at':row.ended_at\
                           , 'standard_total':row.standard_total, 'gift_total':row.gift_total})
        session.close()
        return result

    def getRebateSubBill(self,account_id,started_at,ended_at,session=None):
        if not session:
            session = sa.get_session()
        query = session.execute(SQL.get_rebate_subbill_item,{'started_at':started_at,'ended_at':ended_at,'account_id':account_id})
        rows = query.fetchall()
        result = []
        if rows:
            for row in rows:
                gift_amount = 0
                gift_amount_query = session.execute(SQL.get_rebate_subbill_giftamount,{'started_at':started_at,'ended_at':ended_at,'account_id':row.account_id}).first()
                if gift_amount_query and gift_amount_query.gift_amount_total:
                    gift_amount = gift_amount_query.gift_amount_total
                result.append({'account_id':row.account_id,'parent_account':row.parent_account,
                               'rebate_amount_total':row.rebate_amount_total,'amount_total':row.amount_total,'gift_amount_total':gift_amount})
        session.close()
        return result

    def getAmountTotal_new_naas(self, account_id, started_at, ended_at, session=None):
        if not session:
            session = sa.get_session()
#        if isinstance(started_at, datetime.date):
#            started_at=datetime.date.strftime(started_at,'%Y-%m-%d')
#        if isinstance(ended_at, datetime.date):
#            ended_at=datetime.date.strftime(ended_at,'%Y-%m-%d')
        query = session.execute(SQL.bill_naas, {'account_id':account_id, 'started_at':started_at, 'ended_at':ended_at})
        rows = query.fetchall()
        result = []
        for row in rows:
            result.append({'account_id':row.account_id, 'resource_id':row.resource_id, 'resource_name':row.resource_name\
                           , 'region_id':row.region_id, 'resource_type':row.resource_type, 'parent_id':row.parent_id\
                           , 'amount_total':row.amount_total, 'started_at':row.started_at, 'ended_at':row.ended_at\
                           , 'standard_total':row.standard_total, 'gift_total':row.gift_total})
        session.close()
        return result
    
    def getForecast(self, account_id, session=None):
        if not session:
            session = sa.get_session()
        query = session.query(Consumption.account_id.label("account_id"), Consumption.resource_type.label("resource_type"), Consumption.parent_id.label("parent_id"), func.sum(Consumption.amount).label("amount_total"), func.max(Consumption.discounted_at).label("ended_at"), func.min(Consumption.discounted_at).label("started_at"))
        if account_id:
            query = query.filter(Consumption.account_id == account_id)
#            query=query.filter(Consumption.discounted_at.between(datetime.strptime(start,'%Y-%m-%d %H:%M:%S'),datetime.strptime(end,'%Y-%m-%d %H:%M:%S')))
        d1 = datetime.datetime.utcnow()
        started_at = (d1 - datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H')
        ended_at = d1.strftime('%Y-%m-%d %H')
        query = query.filter(Consumption.started_at == started_at).filter(Consumption.ended_at == ended_at)
        result = []
        rows = query.group_by(Consumption.resource_type).all()
        for row in rows:
            result.append({'account_id':row.account_id, 'resource_type':row.resource_type, 'parent_id':row.parent_id\
                           , 'amount_total':row.amount_total, 'started_at':row.started_at, 'ended_at':row.started_at})
        return result
    
    def getCDNForecast(self, account_id, session=None):
        if not session:
            session = sa.get_session()
        query = session.query(Consumption.account_id.label("account_id"), Consumption.resource_type.label("resource_type"), Consumption.parent_id.label("parent_id"), func.sum(Consumption.amount).label("amount_total"), func.max(Consumption.discounted_at).label("ended_at"), func.min(Consumption.discounted_at).label("started_at"))
        if account_id:
            query = query.filter(Consumption.account_id == account_id)
#            query=query.filter(Consumption.discounted_at.between(datetime.strptime(start,'%Y-%m-%d %H:%M:%S'),datetime.strptime(end,'%Y-%m-%d %H:%M:%S')))
        d1 = datetime.datetime.utcnow()
        started_at = (d1 - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        ended_at = d1.strftime('%Y-%m-%d')
        query_cdnbandwidth = query.filter(Consumption.billing_item == 'cdnbandwidth_1_M').filter(Consumption.started_at == started_at).filter(Consumption.ended_at == ended_at)
        row = query_cdnbandwidth.group_by(Consumption.resource_type).first()
        result = []
        if row:
            result.append({'account_id':row.account_id, 'resource_type':row.resource_type, 'parent_id':row.parent_id\
                           , 'amount_total':row.amount_total, 'started_at':row.started_at, 'ended_at':row.started_at})
            return result
#        d1 = datetime.date(datetime.date.today().year, datetime.date.today().month, 1)
#        started_at = datetime.date(datetime.date.today().year if datetime.date.today().month - 1 else datetime.date.today().year - 1, \
#                                datetime.date.today().month - 1 or 12, 1).strftime('%Y-%m-%d')
#        ended_at = d1.strftime('%Y-%m-%d')
        query_cdnflow = query.filter(Consumption.billing_item == 'cdnflow_1_G').filter(Consumption.started_at == started_at).filter(Consumption.ended_at == ended_at)
        row = query_cdnflow.group_by(Consumption.resource_type).first()
        if row:
            result.append({'account_id':row.account_id, 'resource_type':row.resource_type, 'parent_id':row.parent_id\
                           , 'amount_total':row.amount_total, 'started_at':row.started_at, 'ended_at':row.started_at})
            return result

    def getNAASForcast(self, account_id, session=None):
        if not session:
            session = sa.get_session()
        query = session.query(Consumption.account_id.label('account_id'), Consumption.resource_type.label('resource_type'),
                              Consumption.parent_id.label('parent_id'), func.sum(Consumption.amount).label('amount_total'),
                              func.max(Consumption.discounted_at).label('ended_at'),
                              func.min(Consumption.discounted_at).label('started_at'))
        if account_id:
            query = query.filter(Consumption.account_id == account_id)
        d1 = datetime.datetime.utcnow()
        started_at = (d1 - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        ended_at = d1.strftime('%Y-%m-%d')
        query = query.filter(Consumption.resource_type == 'tunnel').filter(Consumption.started_at == started_at).filter(
            Consumption.ended_at == ended_at)
        row = query.group_by(Consumption.resource_type == 'tunnel').first()
        result = []
        if row:
            result.append({'account_id': row.account_id, 'resource_type': row.resource_type,
                           'parent_id': row.parent_id, 'amount_total': row.amount_total, 'started_at': row.started_at,
                           'ended_at': row.started_at})
            return result


    def getrebatebillitem(self,account_id,started_at,ended_at,session=None):
        if not session:
            session = sa.get_session()
        query = session.execute(SQL.get_one_rebatebill_item,{'account_id':account_id,'started_at':started_at,'ended_at':ended_at})
        rows = query.fetchall()
        result = []
        if rows:
            for row in rows:
                gift_amount = 0
                row2 = session.execute(SQL.get_one_rebatebill_item_gift_amount,{'resource_id':row.resource_id,'account_id':account_id,'started_at':started_at,'ended_at':ended_at}).first()
                if row2 and row2.gift_amount_total:
                    gift_amount = row2.gift_amount_total
                result.append({'resource_id':row.resource_id,'region_id':row.region_id,'resource_type':row.resource_type,
                               'amount_total':row.amount_total,'rebate_amount_total':row.rebate_amount_total,
                               'gift_amount_total':gift_amount,'resource_name':row.resource_name})
        session.close()
        return result


if __name__ == "__main__":
    consumptionDao = ConsumptionDao()
    consumptionDao.getRebateSubBill('xxxx','1999-01-01','2000-01-01')
