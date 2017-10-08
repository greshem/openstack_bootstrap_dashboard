# -*- coding:utf-8 -*-
'''
Created on 2015-8-24

@author: greshem
'''
from billing.db.dao.billDao import BillDao
from billing.db.object.models import Bill
from billing.db.object.models import BillItem
from billing.util.handlerUtil import *
from billing.db.dao.ConsumptionDao import ConsumptionDao
from billing.db.dao.accountDao import AccountDao
from billing.hander.Consumption import totalAmount_bill
from billing.util.pagePackage import *
import datetime
import time
import random
from oslo_log import log as logging
import traceback
LOG = logging.getLogger(__name__)

BILL_OBJECT_KEY = ['account', 'bill_items']
BILL_OBJECT_KEY_SIMPLE = ['account']

def list(account_id, started_at=None, ended_at=None, page_no=1, page_size=15,isBillItems=False, bill_type=None):
    try:
        billDao = BillDao()
        result = billDao.list(account_id, started_at, ended_at,page_no,page_size, isBillItems, bill_type=bill_type)
        dataresult = []
        if result:
            if isBillItems:
                dataresult = [getJsonFromObj(bill, BILL_OBJECT_KEY_SIMPLE)for bill in result]
            else:
                dataresult = [getJsonFromObj(bill, BILL_OBJECT_KEY)for bill in result]
        return outSuccess("billList", pagePackage("bills", dataresult, page_no=result.no, page_size=result.page_size, total=result.total))
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("取得账单列表失败！")

def billItemList(bill_id):
    try:
        billDao = BillDao()
        result=billDao.bill_item_list(bill_id)
        return outSuccess("billitemList", result)
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("取得账单项列表失败！")
    
def getBillDetail(bill_id):
    try:
        bill = Bill()
        bill.bill_id = bill_id
        billDao = BillDao(bill)
        billDao.detail()
        return outSuccess('bill', getJsonFromObj(billDao.bill, BILL_OBJECT_KEY_SIMPLE))
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("取得账单详情失败！")

def generateBill(started_at=None, ended_at=None,last=None,current=None):
    '''生成账单'''
    if isinstance(started_at, str):
        started_at=datetime.datetime.strptime(started_at, '%Y-%m-%d %H:%M:%S')
    if isinstance(ended_at, str):
        ended_at=datetime.datetime.strptime(ended_at, '%Y-%m-%d %H:%M:%S')
    accountDao = AccountDao()
    consumptionDao = ConsumptionDao()
#    rows = accountDao.list(condition={"status":"normal"})
    rows = accountDao.list()
    billDao = BillDao()
    for row in rows:
        account_id = row.account_id
        if billDao.checkBill(account_id, started_at,ended_at):
            continue        
        result = consumptionDao.getAmountTotal_new(account_id, started_at, ended_at)
        if result:
            result = totalAmount_bill(result)
            bill = Bill()
            bill.account_id = account_id
            bill.started_at = started_at
            bill.ended_at = ended_at
            bill.no = generation()
            bill.bill_items = []
            bill.amount = 0
            bill.gift_amount=0
            bill.standard_amount=0
            for bill_item_data in result:
                billItem = BillItem()
                getObjFromJson(billItem, bill_item_data)
                if bill_item_data['amount_total'] is None:
                    bill_item_data['amount_total']=0
                if bill_item_data['standard_total'] is None:
                    bill_item_data['standard_total']=0
                if bill_item_data['gift_total'] is None:
                    bill_item_data['gift_total']=0
                bill.amount += float(bill_item_data['amount_total'])
                bill.standard_amount += float(bill_item_data['standard_total'])
                bill.gift_amount += float(bill_item_data['gift_total'])
                billItem.amount = round(float(bill_item_data['amount_total']),2)
                billItem.standard_amount=round(float(bill_item_data['standard_total']),2)
                billItem.gift_amount=round(float(bill_item_data['gift_total']),2)
                bill.bill_items.append(billItem)
            bill.amount=round(bill.amount,2)
            bill.type='cloud'
            billDao.bill = bill
            billDao.add()


def generateBill_naas(started_at=None, ended_at=None, last=None, current=None):
    '''生成naas账单'''
    if isinstance(started_at, str):
        started_at = datetime.datetime.strptime(started_at, '%Y-%m-%d %H:%M:%S')
    if isinstance(ended_at, str):
        ended_at = datetime.datetime.strptime(ended_at, '%Y-%m-%d %H:%M:%S')
    accountDao = AccountDao()
    consumptionDao = ConsumptionDao()
    rows = accountDao.list()
    billDao = BillDao()
    for row in rows:
        account_id = row.account_id
        if billDao.checkBill_naas(account_id, started_at, ended_at):
            continue
        result = consumptionDao.getAmountTotal_new_naas(account_id, started_at, ended_at)
        if result:
            bill = Bill()
            bill.account_id = account_id
            bill.started_at = started_at
            bill.ended_at = ended_at
            bill.no = generation()
            bill.bill_items = []
            bill.amount = 0
            bill.gift_amount = 0
            bill.standard_amount = 0
            for bill_item_data in result:
                billItem = BillItem()
                getObjFromJson(billItem, bill_item_data)
                if bill_item_data['amount_total'] is None:
                    bill_item_data['amount_total'] = 0
                if bill_item_data['standard_total'] is None:
                    bill_item_data['standard_total'] = 0
                if bill_item_data['gift_total'] is None:
                    bill_item_data['gift_total'] = 0
                bill.amount += float(bill_item_data['amount_total'])
                bill.standard_amount += float(bill_item_data['standard_total'])
                bill.gift_amount += float(bill_item_data['gift_total'])
                billItem.amount = round(float(bill_item_data['amount_total']), 2)
                billItem.standard_amount = round(float(bill_item_data['standard_total']), 2)
                billItem.gift_amount = round(float(bill_item_data['gift_total']), 2)
                bill.bill_items.append(billItem)
            bill.amount = round(bill.amount, 2)
            bill.type = 'naas'
            billDao.bill = bill
            billDao.add()
    
        
#import threading
#mu = threading.Lock()
#start = 1000000000
#def generation():
#    '''自动生成流水号'''
#    mu.acquire()
#    global start
#    try:
#        if start == 1000000000:
#            billDao = BillDao()
#            max=billDao.maxNo()
#            start = int(max) if max else start-1
#        start += 1
#        mu.release()
#    except Exception:
#        mu.release()
#    return start

def generation():
    order_id=datetime.datetime.strftime(datetime.datetime.utcnow(),'%y%m')
    for _ in range(10):
        order_id+=str(random.randint(0,9))
    return order_id
    
            
    

if __name__ == '__main__':
#    print generation()
#    print generation()
#    print generation()
    generateBill(started_at='2015-11-01 00:00:00', ended_at='2015-12-01 00:00:00')
#    generateBill(datetime.date(datetime.date.today().year,datetime.date.today().month-1,1)\
#                      , datetime.date(datetime.date.today().year,datetime.date.today().month,1))
            
