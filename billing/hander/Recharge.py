# -*- coding:utf-8 -*-
'''
Created on 2015年9月9日

@author: greshem
'''
from billing.db.dao.rechargeDao import RechargeDao
from billing.db.dao.orderDao import OrderDao
from billing.db.dao.insteadRechargeDao import InsteadRechargeDao
from billing.db.dao.transferInfoDao import TransferInfoDao
from billing.db.object.models import Recharge
from billing.db.object.models import InsteadRecharge
from billing.db.object.models import Order
from billing.db.object.models import TransferInfo
from billing.util.handlerUtil import *
from billing.util.tzUtil import change2UTC
from billing.db.sqlalchemy import session as sa

import json
from oslo_log import log as logging
from billing.util.pagePackage import *
import traceback
import random
import datetime
from billing.constant.sql import SQL
LOG = logging.getLogger(__name__)


def create(account_id, rechargeJson, headers=None, **kwargs):
    """创建充值信息（包含代充值和订单信息）"""
    try:
        if isinstance(rechargeJson, str):
            rechargeJson = json.loads(rechargeJson)
        LOG.info('rechargeJson ..'+json.dumps(rechargeJson))
        rechargeDict = rechargeJson['recharge']
        recharge = Recharge()
        getObjFromJson(recharge, rechargeDict)
        order = Order()
        order.account_id = account_id
        order.amount = recharge.amount
        order.payment_type = "recharge" #"recharge" "gift"
        order.status = "ordered"  # "ardered","payed"
        order.order_no = generation()
        recharge.order = order
        """判断是否是代充值"""
        if recharge.is_instead_recharge:
            insteadRechargeDict = rechargeJson['instead_recharge']
            insteadRecharge = InsteadRecharge()
            getObjFromJson(insteadRecharge, insteadRechargeDict)
            insteadRecharge.recharge = recharge
            insteadRechargeDao = InsteadRechargeDao(insteadRecharge)
            insteadRechargeDao.add()
            return outSuccess("recharge", getJsonFromObj(insteadRechargeDao.insteadRecharge.recharge))
        
        rechargeDao = RechargeDao(recharge)
        rechargeDao.add()
        return outSuccess("recharge", getJsonFromObj(rechargeDao.recharge))
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("生成充值记录失败！")


def getOrderRechargeList(account_id=None, payment_type=None, started_at=None, ended_at=None,page_no=1,page_size=15):
    try:
        orderDao = OrderDao()
        result,count = orderDao.getOrderRechargeList(account_id, payment_type, started_at, ended_at,page_no,page_size)
        return outSuccess("billList", pagePackage("bills", result, page_no=page_no, page_size=page_size, total=count))
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("取得账单列表失败！")


def insteadRecharge(insteadRechargeJson, headers=None, **kwargs):
    try:
        if isinstance(insteadRechargeJson, str):
            insteadRechargeJson = json.loads(insteadRechargeJson)
        order = Order()
        account_id = insteadRechargeJson['recharge']['account_id']
        amount = float(insteadRechargeJson['recharge']['amount'])
        remark = insteadRechargeJson['instead_recharge']['remark']
        instead_recharge_by = insteadRechargeJson['instead_recharge']['instead_recharge_by']
        instead_recharge_account = insteadRechargeJson['instead_recharge']['instead_recharge_account']

        insteadRechargeDict = insteadRechargeJson['instead_recharge']
        insteadRecharge = InsteadRecharge()
        getObjFromJson(insteadRecharge, insteadRechargeDict)
        
        transferinfoDict=insteadRechargeJson['transferinfo']
        transferinfo=TransferInfo()
        getObjFromJson(transferinfo,transferinfoDict)

        order.account_id = account_id
        order.amount = amount
        order.payment_type = "recharge"
        order.status = "pay_success"
        order.order_no = generation()

        recharge = Recharge()
        recharge.order = order
        recharge.payment_way = "transfer_pay"
        recharge.status = "pay_success"
        recharge.pay_at = datetime.datetime.utcnow()
        recharge.is_instead_recharge = True
        recharge.remark = insteadRecharge.remark
        recharge.amount = amount

        insteadRecharge = InsteadRecharge()
        insteadRecharge.recharge = recharge
        insteadRecharge.instead_recharge_by = instead_recharge_by
        insteadRecharge.instead_recharge_account = instead_recharge_account
        insteadRecharge.remark = remark

        insteadRechargeDao = InsteadRechargeDao(insteadRecharge)
        insteadRechargeDao.insteadRechargeAmount()
        
        transferinfo.recharge_id=insteadRechargeDao.insteadRecharge.recharge_id
        transferinfo.amount=amount
        transferinfo.inward_at=change2UTC(transferinfo.inward_at,format='%Y-%m-%d')
        transferInfoDao=TransferInfoDao(transferinfo)
        transferInfoDao.add()
        
        insteadRechargeDao.insteadRecharge.transferInfo=transferInfoDao.tansferinfo
        return outSuccess("insteadecharge", getJsonFromObj(insteadRechargeDao.insteadRecharge))
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("代充值失败！")

# added by zhangaw
def getinsteadrechargelist(instead_account,condition=None,**args):
    sql=SQL.insteadRechargeList
    sql=sql%(str(instead_account))
    try:
        session=sa.get_session()
        if condition:
            for key,value in condition.items():
                if key=='usernamelike':
                    value1='%'
                    value2='%'
                    if '_' in value:
                        value=value.replace('_','\_')
                    sql+=' and username like \'%s%s%s\''%(value1,value,value2)
                if key=='max_amount':
                    sql+=' and amount<=%d'%int(value)
                if key=='min_amount':
                    sql+=' and amount>=%d'%int(value)
                if key=='started_at':
                    value+=' 00:00:00'
                    sql+=' and pay_at>=\'%s\''%value
                if key=='ended_at':
                    value+=' 23:59:59'
                    sql+=' and pay_at<=\'%s\''%value
        sql+=' order by pay_at desc'      
        insteadRechargeList=session.execute(sql).fetchall()
        count=len(insteadRechargeList) if insteadRechargeList else 0
        if condition:
            if condition.has_key('limit'):
                limit=int(condition['limit'])
                offset=int(condition['offset']) if condition.has_key('offset') else 0
                insteadRechargeList=insteadRechargeList[(limit*offset):((offset+1)*limit)]
        result=[]
        for item in insteadRechargeList:
            tempdict={}
            tempdict['username']=item.username
            tempdict['amount']=float(item.amount) if item.amount else 0
            tempdict['pay_at']=item.pay_at
            tempdict['remark']=item.remark
            result.append(tempdict)
        session.close()
        return json.dumps({'count':count,'insteadRechargeList':result,'success':'success'},cls=CJsonEncoder, ensure_ascii=False)
    except Exception as e:
        session.close()
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("获取代充值列表失败")

def getinsteadamount(instead_account,**args):
    sql=SQL.insteadTotalAmount
    try:
        session=sa.get_session()
        totalAmount=session.execute(sql,dict({'instead_recharge_account':instead_account})).first()
        if  totalAmount:
            total=float(totalAmount.total) if totalAmount.total else 0
        else:
            total=0
        session.close()
        return outSuccess('totalamount',total)
    except Exception as e:
        session.close()
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("获取代充值总额失败")
# end edit





#import threading
#mu = threading.Lock()
#order_start = 1000000
#def generation():
#    '''自动生成流水号'''
#    mu.acquire()
#    global order_start
#    if order_start == 1000000:
#        orderDao = OrderDao()
#        order_start = int(orderDao.maxNo())
#    order_start += 1
#    mu.release()
#    return order_start

def generation():
    order_id=datetime.datetime.strftime(datetime.datetime.utcnow(),'%y%m')
    for _ in range(10):
        order_id+=str(random.randint(0,9))
    return order_id

if __name__ == "__main__":
    tempdict={'instead_recharge':{'instead_recharge_by':'xiaow','instead_recharge_account':'eeeeeeeeeeeeeee','remark':'woquwoquwoqu'},'recharge':{'account_id':'ed709b66-e7dd-47f1-bd6e-6ac3464017c2','amount':2000.96}}
    temp=insteadRecharge(tempdict)
    print temp
