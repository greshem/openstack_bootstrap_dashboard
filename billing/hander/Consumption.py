# -*- coding:utf-8 -*-
'''
Created on 2015-8-24

@author: greshem
'''
from billing.db.dao.ConsumptionDao import ConsumptionDao
from billing.db.object.models import Account
from billing.db.dao.accountDao import AccountDao
from billing.util.handlerUtil import *
from billing.util.pagePackage import pagePackage
from oslo_log import log as logging
import copy
import traceback
LOG = logging.getLogger(__name__)
def consumptionList(account_id,started_at,ended_at,region_id,resource_type,page_no=1, page_size=15, headers=None, **kwargs):
    '''
    查询消费记录
    '''
    try:
        consumptionDao = ConsumptionDao()
        result=consumptionDao.getAmountTotal(account_id, started_at, ended_at,region_id,resource_type,page_no, page_size)
        dataResult=[]
        if result:
            for consumption in result:
                dataResult.append(consumption)
            dataResult=totalAmount(dataResult)
        return outSuccess("consumptionList",pagePackage('consumptions',dataResult,page_no=result.no, page_size=result.page_size, total=result.total))
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("取得消费记录列表失败！")
        

def consumptionForecast(account_id, headers=None, **kwargs):
#    try:
        consumptionDao = ConsumptionDao()
        result=consumptionDao.getForecast(account_id)
        result_cdn=consumptionDao.getCDNForecast(account_id)
        result_naas=consumptionDao.getNAASForcast(account_id)
        
        dataResult=[]
        if result_cdn:
            for cdn in result_cdn:
                result.append(cdn)
        if result_naas:
            for naas in result_naas:
                result.append(naas)
        dataResult=forecast(result)
        return outSuccess('forecast',createForecast(dataResult))
#    except Exception as e:
#        LOG.error(str(e))
#        return outError("取得消费预估失败！")

def totalAmount(dataArry):
    '''
    合计统计金额
    '''
    if dataArry:
        for data in dataArry:
            if data['parent_id'] and data['resource_type'] in ('cpu','memory'):
                for data_new in dataArry:
                    if data_new['resource_id']==data['parent_id']:
                        data_new['amount_total']=data_new['amount_total'] if data_new['amount_total'] else 0
                        data['amount_total']=data['amount_total'] if data['amount_total'] else 0
                        data_new['amount_total']+=data['amount_total']
        
    return filter(lambda x:x['resource_type'] not in ('cpu','memory'),dataArry)

def totalAmount_bill(dataArry):
    '''
    合计统计金额
    '''
    if dataArry:
        for data in dataArry:
            if data['resource_type'] in ('cpu','memory'):
                for data_new in dataArry:
                    if data_new['resource_type']=='instance' and data_new['region_id']==data['region_id']:
                        data_new['amount_total']=data_new['amount_total'] if data_new['amount_total'] else 0
                        data['amount_total']=data['amount_total'] if data['amount_total'] else 0
                        data_new['gift_total']=data_new['gift_total'] if data_new['gift_total'] else 0
                        data['gift_total']=data['gift_total'] if data['gift_total'] else 0
                        data_new['standard_total']=data_new['standard_total'] if data_new['standard_total'] else 0
                        data['standard_total']=data['standard_total'] if data['standard_total'] else 0
                        
                        data_new['amount_total']+=data['amount_total']
                        data_new['gift_total']+=data['gift_total']
                        data_new['standard_total']+=data['standard_total']
        
    return filter(lambda x:x['resource_type'] not in ('cpu','memory'),dataArry)

#def totalAmount_new(dataArry):
#    '''
#    合计统计金额
#    '''
#    data_cdn=None
#    if dataArry:
#        for data in dataArry:
#            if data['parent_id'] and data['resource_type'] in ('cpu','memory'):
#                for data_new in dataArry:
#                    if data_new['resource_id']==data['parent_id']:
#                        data_new['amount_total']+=data['amount_total']
#            if data['resource_type'] in ('cdnflow','cdnbandwidth'):
#                if data_cdn is None:
#                    data_cdn=copy.copy(data)
#                    data['resource_type']='cdn'
#                else:
#                    data_cdn['amount_total']+=data['amount_total']
#        if data_cdn is not None:
#            dataArry.append(data_cdn)
#    return filter(lambda x:x['resource_type'] not in ('cpu','memory','cdnflow','cdnbandwidth'),dataArry)


def forecast(dataArry):
    '''
    消费预估
    '''
    if dataArry:
        for data in dataArry:
            if data['resource_type'] in ('cpu','memory'):
                for data_new in dataArry:
                    if data_new['resource_type']=='instance':
                        data_new['amount_total']+=data['amount_total']
        
    return filter(lambda x:x['resource_type'] not in ('cpu','memory'),dataArry)


def get_prices(res_type, unit_price):
    if res_type in ['cdnbandwidth_1_M', 'cdnflow_1_G']:
        return {'resource_type': 'cdn', 'hour': 0.0,
                'day': unit_price*24, 'month': unit_price*24*30, 'year': unit_price*24*30*365}
    else:
        return {'resource_type': res_type, 'hour': unit_price,
                'day': unit_price*24, 'month': unit_price*24*30, 'year': unit_price*24*30*365}


def createForecast(dataArry):
    forecast_datas = []
    if dataArry:
        for data in dataArry:
            forecast_datas.append(get_prices(data['resource_type'], data['amount_total']))
        total = {'resource_type': 'total',
                 'hour': sum(x['hour'] for x in forecast_datas),
                 'day': sum(x['day'] for x in forecast_datas),
                 'month': sum(x['month'] for x in forecast_datas),
                 'year': sum(x['year'] for x in forecast_datas),
                 }
        forecast_datas.append(total)
    return forecast_datas


def getAmountSummary(account_id,started_at,ended_at):
    '''查看账户消费总额汇总'''
    try:
        consumptionDao = ConsumptionDao()
        result=consumptionDao.getAmountSummary(account_id, started_at, ended_at)
        return outSuccess("amountsummary",result)
    except Exception as e:
            LOG.error(str(e))
            return outError("取得账户消费汇总失败！")

def getConsumptionSummary(account_id,started_at,ended_at):
    '''账户消费明细汇总'''
    try:
        consumptionDao = ConsumptionDao()
        result=consumptionDao.getConsumptionSummary(account_id, started_at, ended_at)
        return outSuccess("consumptionsummary",result)
    except Exception as e:
            LOG.error(str(e))
            return outError("取得账户消费汇总失败！")

    
if __name__ =="__main__":
    print consumptionForecast('0e638909-b50b-4b04-97cc-2692d88a9033')  

 