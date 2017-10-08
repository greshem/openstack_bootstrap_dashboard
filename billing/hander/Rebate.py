# -*- coding:utf-8 -*-
from billing.api import wsgi
from billing.hander import Account
from billing.util.controllerUtil import *
import traceback
import json
import datetime
from billing.db.sqlalchemy import session as sa
from oslo_config import cfg
from billing.util.tzUtil import change2UTC
from billing.util.handlerUtil import *
from oslo_log import log as logging
from billing.db.dao import rebateBillDao,rebateSubBillDao,rebateBillItemDao
from billing.db.dao.ConsumptionDao import ConsumptionDao
from billing.db.dao.accountDao import AccountDao
from billing.db.dao.rebateBillDao import RebateBillDao
from billing.db.dao.rebateBillItemDao import RebateBillItemDao
from billing.db.dao.rebateSubBillDao import RebateSubBillDao
from billing.db.object.models import RebateBill,RebateSubBill,RebateBillItem
from billing.hander.Bill import generation

LOG=logging.getLogger(__name__)

'''
生成返现账单
'''
def generateRebateBill(started_at=None,ended_at=None,last=None,current=None):
    if isinstance(started_at,str):
        started_at=datetime.strptime(started_at,'%Y-%m-%d %H:%M:%S')
    if isinstance(ended_at,str):
        ended_at = datetime.strptime(ended_at,'%Y-%m-%d %H:%M:%S')
    accountDao = AccountDao()
    consumptionDao = ConsumptionDao()
    rebatebillDao = RebateBillDao()
    rows = accountDao.getAllProjectAdminAccount()
    if rows:
        for row in rows:
            account_id = row.account_id
            user_id = row.user_id
            if rebatebillDao.checkRebateBill(account_id,started_at,ended_at):
                continue
            subaccounts = accountDao.subAccountList(user_id,page_size=50000)[0]
            if subaccounts:
                rebatebill = RebateBill()
                rebatebill.started_at = started_at
                rebatebill.ended_at = ended_at
                rebatebill.account_id = account_id
                rebatebill_rebate_amount = 0
                rebatebill_subaccount_amount = 0
                rebatebill_subaccount_gift_amount = 0
                rebatebill.rebate_subbills = []
                rebatebill.no = generation()
                for subaccount in subaccounts:
                    temp_account_id = subaccount['account_id']
                    result = consumptionDao.getRebateSubBill(temp_account_id,started_at,ended_at)
                    if result:
                        rebatesubbill = RebateSubBill()
                        rebatesubbill.rebate_bill_items = []
                        for item in result:
                            result2 = consumptionDao.getrebatebillitem(temp_account_id,started_at,ended_at)
                            if result2:
                                for item2 in result2:
                                    rebatebillitem = RebateBillItem()
                                    rebatebillitem.started_at = started_at
                                    rebatebillitem.ended_at = ended_at
                                    rebatebillitem.amount = round(item2['amount_total'],2)
                                    rebatebillitem.rebate_amount = round(item2['rebate_amount_total'],2)
                                    rebatebillitem.resource_id = item2['resource_id']
                                    rebatebillitem.resource_type = item2['resource_type']
                                    rebatebillitem.resource_name = item2['resource_name']
                                    rebatebillitem.region_id = item2['region_id']
                                    rebatebillitem.gift_amount = round(item2['gift_amount_total'],2) if item2['gift_amount_total'] else 0
                                    rebatesubbill.rebate_bill_items.append(rebatebillitem)
                            rebatebill_rebate_amount += float(item['rebate_amount_total']) if item['rebate_amount_total'] else 0
                            rebatebill_subaccount_amount += float(item['amount_total']) if item['amount_total'] else 0
                            rebatebill_subaccount_gift_amount += float(item['gift_amount_total']) if item['gift_amount_total'] else 0
                            rebatesubbill.account_id = temp_account_id
                            rebatesubbill.started_at = started_at
                            rebatesubbill.ended_at = ended_at
                            rebatesubbill.rebate_amount = round(item['rebate_amount_total'],2)
                            rebatesubbill.amount = round(item['amount_total'],2)
                            rebatesubbill.gift_amount = round(item['gift_amount_total'],2)
                            rebatebill.rebate_subbills.append(rebatesubbill)
                rebatebill.rebate_amount = round(rebatebill_rebate_amount,2)
                rebatebill.subaccount_amount = round(rebatebill_subaccount_amount,2)
                rebatebill.subaccount_gift_amount = round(rebatebill_subaccount_gift_amount,2)
                rebatebillDao.rebateBill = rebatebill
                rebatebillDao.add()

def getDictFromObj(temp_list,objectlist,attrs):
    for object in objectlist:
        temp_dict = {}
        for item in attrs:
            if hasattr(object,item):
                temp_dict[item] = str(getattr(object,item))
        temp_list.append(temp_dict)

def getrebatebillList(condition,likecondition,page_no,page_size):
    try:
        session = sa.get_session()
        sql = '''select temp.*,user.name as username,user.company from (select rebate_bill.*,account.user_id from rebate_bill join account on rebate_bill.account_id = account.account_id)as temp join keystone.user on temp.user_id = user.id'''
        if condition:
            for item in condition:
                sql += ' and {}=\'{}\''.format(str(item),str(condition[item]))
        if likecondition:
            for item in likecondition:
                if item == 'username':
                    sql += ' and name like \'%{}%\''.format(str(likecondition[item]))
                if item == 'company':
                    sql += ' and company like \'%{}%\''.format(str(likecondition[item]))
                if item == 'no':
                    sql += ' and no like \'%{}%\''.format(str(likecondition[item]))
        rows = session.execute(sql).fetchall()
        temp_list = []
        if rows:
            getDictFromObj(temp_list,rows,['rebate_bill_id','account_id','no','started_at','ended_at','username','company','rebate_amount','subaccount_amount','subaccount_gift_amount','created_at'])
        count = len(temp_list)
        temp_list = temp_list[(page_no-1)*page_size:(page_no*page_size)]
        return json.dumps({'count':count,'rebate_bill_list':temp_list,'success':'success'})
    except Exception as e:
        session.close()
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("获取返现列表失败!")

def getrebatesubbillList(condition,likecondition,page_no,page_size):
    try:
        session = sa.get_session()
        temp_list = []
        rebate_bill_id = condition['rebate_bill_id']
        sql = 'select user.company,temp.* from keystone.user join (select rebate_subbill.*,account.username,account.user_id,account.type from rebate_subbill join account on rebate_bill_id =:rebate_bill_id and rebate_subbill.account_id = account.account_id)as temp on user.id = temp.user_id'
        if likecondition:
            pass
        rows = session.execute(sql,dict({'rebate_bill_id':rebate_bill_id})).fetchall()
        if rows:
            getDictFromObj(temp_list,rows,['rebate_subbill_id','username','company','rebate_bill_id','account_id','rebate_amount','type','amount','gift_amount','started_at','ended_at','created_at'])
        count = len(temp_list)
        temp_list = temp_list[(page_no-1)*page_size:(page_no*page_size)]
        return json.dumps({'count':count,'rebate_subbill_list':temp_list,'success':'success'})
    except Exception as e:
        session.close()
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("获取返现子账户列表失败!")

def getrebatebillitemList(condition,likecondition,page_no,page_size):
    try:
        session = sa.get_session()
        temp_list = []
        rebatebillitemDao = rebateBillItemDao.RebateBillItemDao()
        rows = rebatebillitemDao.list(condition,likecondition,session)
        if rows:
            getDictFromObj(temp_list,rows,['rebate_bill_item','rebate_subbill_id','resource_id','resource_name','resource_type','region_id','amount','gift_amount','rebate_amount','started_at','ended_at','created_at'])
        count = len(temp_list)
        temp_list = temp_list[(page_no-1)*page_size:(page_no*page_size)]
        return json.dumps({'count':count,'rebate_billitem_list':temp_list,'success':'success'})
    except Exception as e:
        session.close()
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("获取返现详情列表失败!")


if __name__=='__main__':
    print float(None)
       # consumptionDao = ConsumptionDao()
       # result = consumptionDao.getRebateSubBill('fe08405a-9f6a-43f1-b53c-efdb866209f4','2015-02-02 00:00:00','2016-12-12 00:00:00')
       # print result