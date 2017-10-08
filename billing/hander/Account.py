# -*- coding:utf-8 -*-
'''
Created on 2015-8-24

@author: greshem
'''
from billing.db.dao.accountDao import AccountDao
from billing.db.dao.ConsumptionDao import ConsumptionDao
from billing.db.object.models import Account
import json
from billing.util.handlerUtil import *
from oslo_log import log as logging
from billing.util.pagePackage import *
from billing.util.uuidUtil import *
from billing.util.md5 import *
import datetime
import traceback
from billing.util.tzUtil import change2UTC,datetime2Str
from billing.db.dao.workOrderDao import WorkOrderDao
from billing.db.sqlalchemy import session as sa
LOG = logging.getLogger(__name__)

ACCOUNT_OBJECT_KEY = ["billes", "addresses", "consumptions"]


def add(accountJson, headers=None, **kwargs):
    """创建账户"""
    try:
        LOG.info('account add....')
        if isinstance(accountJson, str):
            accountJson = json.loads(accountJson)
        accountDict = accountJson['account']
        account = Account()
        getObjFromJson(account, accountDict)
        if not account.account_id:
            account.account_id = getUUID()
        LOG.info('account add start ..'+account.account_id)
    # *** add by zhangaw ***
#        session = sa.get_session()
#        parent_userid = accountDict['parent_id'] if accountDict.has_key('parend_id') else ''
#        if not parent_userid:
#            user_id = accountDict['user_id']
#            query_temp = session.execute('select parent_id from keystone.user where id=\'{}\' '.format(str(user_id))).first()
#            parent_userid = query_temp.parent_id if query_temp else ''
#        sql2 = 'select * from billing.account where user_id=\'{}\''.format(str(parent_userid))
#        query2 = session.execute(sql2).first()
#        if query2:
#            account.parent_account = query2.account_id
#        session.close()
    # *** end ***
        accountDao = AccountDao(account)
        accountDao.add()
#        user=accountDao.getUserById(account.user_id)
#        accountDao.addcontact(accountDao.account.account_id, {'name': user['name'],
#                                      'position':None,
#                                      'telephone': user['telephone'],
#                                      'email':user['email'],
#                                      'remark': None,
#                                      'created_by': None,
#                                      'created_at': datetime.datetime.now()})
        LOG.info('account add end ..'+account.account_id)
        return outSuccess("account", getJsonFromObj(accountDao.account, ACCOUNT_OBJECT_KEY))
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("创建账户失败！")
    

def update(accountJson, headers=None, **kwargs):
    """更新账户"""
    try:
        if isinstance(accountJson, str):
            accountJson = json.loads(accountJson)
        accountDict = accountJson['account']
        account = Account()
        account.account_id = accountDict['account_id']
        accountDao = AccountDao(account)
        accountDao.update(accountDict)
        return outSuccess("account", getJsonFromObj(accountDao.account, ACCOUNT_OBJECT_KEY))
    except Exception as e:
            LOG.error(str(e))
            LOG.error(traceback.format_exc())
            return outError("更新账户失败！")
    
   
def listByPage(conditionJson, likeConditionjson=None, page_no=1, page_size=15, headers=None, **kwargs):
    '''
    分页查询账户信息
    ''' 
    try:
        conditionJson = json.loads(conditionJson)
        likeConditionjson = json.loads(likeConditionjson)
        accountDao = AccountDao()
        result = accountDao.getAccountByPage(accountDao.getQueryByCondition(conditionJson, likeConditionjson), page_no, page_size)
        dataResult = []
        if result:
            for account in result:
                dataResult.append(getJsonFromObj(account, ACCOUNT_OBJECT_KEY))
        return outSuccess("accountList", pagePackage("accounts", dataResult, page_no=result.no, page_size=result.page_size, total=result.total))
    except Exception as e:
            LOG.error(str(e))
            LOG.error(traceback.format_exc())
            return outError("取得账户列表失败！")


def detail(account_id):
    '''账号详情'''
    try:
        account = Account()
        account.account_id = account_id
        accountDao = AccountDao(account)
        accountDao.detail()
        return outSuccess("account", getJsonFromObj(accountDao.account, ACCOUNT_OBJECT_KEY))
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("取得账号详情失败！")

def detail_dict(account_id):
    '''帐号详情字典,包括account信息，user信息以及region信息'''
    try:
        account = Account()
        account.account_id = account_id
        accountDao = AccountDao(account)
        accountDao.detail_dict()
        return_dict={
            "account":getJsonFromObj(accountDao.account,ACCOUNT_OBJECT_KEY),
            "user":accountDao.user_info,
            "region":accountDao.region_info,
            "success":"success"
        }
        return json.dumps(return_dict,cls=CJsonEncoder, ensure_ascii=False)

    
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("取得账号详情字典失败！")

def getAccountByUserID(user_id):
    '''根据user的ID查找账号'''
    try:
        accountDao = AccountDao()
        accountDao.getAccountByUserID(user_id)
        return outSuccess("account", getJsonFromObj(accountDao.account, ACCOUNT_OBJECT_KEY))
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("取得账号失败！")

def getAccountByProjectId(project_id):
    '''根据project的ID查找账号'''
    try:
        accountDao = AccountDao()
        accountDao.getAccountByProjectId(project_id)
        return outSuccess("account", getJsonFromObj(accountDao.account, ACCOUNT_OBJECT_KEY))
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("取得账号失败！")


# def getAccountByUserMD5(user_md5):
#    '''根据user的md5查找账号'''
#    try:
#        accountDao = AccountDao()
#        accountDao.getAccountByUserMD5(user_md5)
#        return outSuccess("account", getJsonFromObj(accountDao.account, ACCOUNT_OBJECT_KEY))
#    except Exception as e:
#        LOG.error(str(e))
#        return outError("取得账号失败！")

def delete(account_id):
    '''删除账号'''
    try:
        account = Account()
        account.account_id = account_id
        accountDao = AccountDao(account)
        accountDao.delete()
        return outSuccess("msg", "删除账号成功！")
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("删除账号失败！")  

def getSubAccountSum(account_id, headers=None, **kwargs):
    '''子账户数目统计'''
    try:
        account = Account()
        account.account_id = account_id
        accountDao = AccountDao(account)
        accountDao.detail()
        return outSuccess("subAccountSum", accountDao.getSubAccountComsump(accountDao.account.user_id))
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("取得子账户统计失败！") 

def subAccountList(account_id, condition=None,page_no=1, page_size=15):
    try:
        account = Account()
        account.account_id = account_id
        accountDao = AccountDao(account)
        accountDao.detail()
        result,count=accountDao.subAccountList(accountDao.account.user_id, condition, page_no, page_size)
        return outSuccess("subAccountList", pagePackage("accounts", result, page_no=page_no, page_size=page_size, total=count))
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("取得子账户列表失败！")

# arsene
def ProjectAdminsubAccountList(account_id, condition=None):
    try:
        account=Account()
        account.account_id=account_id
        accountDao=AccountDao(account)
        accountDao.detail()
        result,count=accountDao.ProjectAdminsubAccountList(accountDao.account.user_id, condition)
        print result
        return outSuccess('subAccountList', pagePackage('accounts', result, total=count))
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("取得子账户列表失败！")


def subAccountDetail(account_id):
    try:
        accountDao = AccountDao()
        return outSuccess("subAccountDetail", accountDao.subAccountDetail(account_id))
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("取得子账户列表失败！")  


def subAccountAmountSum(account_id,started_at,ended_at): 
    try:
        account = Account()
        account.account_id = account_id
        accountDao = AccountDao(account)
        accountDao.detail()
        return outSuccess("sunAccountAmountSum", accountDao.subAccountAmountSum(accountDao.account.user_id, started_at,ended_at))
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("取得子账户列表失败！")

def subAccountConsumptionList(account_id,started_at,ended_at,condition,page_no=1,page_size=15):
    '''子账户消费列表'''
    try:
        account = Account()
        account.account_id = account_id
        accountDao = AccountDao(account)
        accountDao.detail()
        rows,count=accountDao.subAccountList(accountDao.account.user_id, condition,page_no,page_size)
        result=[]
        if datetime2Str(started_at)==change2UTC(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m')+'-01',format='%Y-%m-%d') and datetime2Str(datetime2Str(ended_at,outformat='%Y-%m-%d %H'),informat='%Y-%m-%d %H')==change2UTC(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H'),format='%Y-%m-%d %H'):
            if rows:
                accountDao=AccountDao()
                for row in rows:
                    account = Account()
                    account.account_id = row['account_id']
                    accountDao.account=account
                    accountDao.detail()
                    row['amount_total']=accountDao.account.current_month_amount
                    row['standard_amount_total']=accountDao.account.current_month_standard_amount
                    result.append(row)
        else:    
            if rows:
                consumptionDao=ConsumptionDao()
                for row in rows:
                    total=consumptionDao.getAmountSummary(row['account_id'], started_at, ended_at)
                    result.append(dict(row,**total))
        return outSuccess('subAccountConsumptionList', pagePackage("accounts", result, page_no=page_no, page_size=page_size, total=count))
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("取得子账户消费列表失败！")
    

def changeCreditLine(account_id,credit_line):
    '''调整信用额度'''
    try:
        accountDao=AccountDao()
        return outSuccess("account", accountDao.changeCreditLine(account_id, credit_line))
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("调整信用额度失败！") 

def change2Credit(account_id,credit_line):
    '''普通用户升级信用用户'''
    try:
        accountDao=AccountDao()
        return outSuccess("account", accountDao.change2Credit(account_id, credit_line))
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("升级信用用户失败！") 

def checkAdmin(account_id):
    '''校验是否是admin用户'''
    try:
        accountDao=AccountDao()
        return outSuccess("isAdmin", accountDao.checkAdmin(account_id))
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("校验用户失败！")

def lowcashReminder_3():
    accountDao=AccountDao()
    for account in accountDao.list({'status':'normal'}):
        try:
            if accountDao.lowcashReminder_3(account.account_id):
                account.cash_balance=account.cash_balance if account.cash_balance else 0
                account.gift_balance=account.gift_balance if account.gift_balance else 0
                account.credit_line=account.credit_line if account.credit_line else 0
                content=None
                if account.type=='normal':
                    content='账户：'+account.username+'余额不足使用3天，请催款。目前账户现金余额:'+str(account.cash_balance)+',赠送余额:'+str(account.gift_balance)
                else:
                    content='账户：'+account.username+'余额不足使用3天，请催款。目前账户现金余额:'+str(account.cash_balance)+',赠送余额:'+str(account.gift_balance)+',信用额度：'+str(account.credit_line)+',可用额度：'+str(account.credit_line if account.cash_balance>0 else account.credit_line+account.cash_balance)+"。"
                payment_workorder={
                'workordertype':6,
                'workorder_no':generation(),
                'apply_by':'billing',
                'apply_source':'billing',
                'status':'apply',
                'theme':'账户：'+account.username+'余额不足使用3天，请催款',
                'content':content
                }
                workOrderDao=WorkOrderDao()
                
                if workOrderDao.checkPaymentWorkOrder(6, 'billing', 'billing', 'apply', '账户：'+account.username+'余额不足使用3天，请催款', datetime.datetime.utcnow()-datetime.timedelta(days=3)):
                    workOrderDao.create(payment_workorder)
        except Exception as e:
            LOG.error(str(e))
            LOG.error(traceback.format_exc())
def generation():
    import random
    order_id=datetime.datetime.strftime(datetime.datetime.utcnow(),'%y%m')
    for _ in range(10):
        order_id+=str(random.randint(0,9))
    return order_id
# added by zhangaw
def getUserType(account_id):
    pass

def getParentUserByID(user_id):
    '''根据user的ID查找父用户'''
    try:
        accountDao = AccountDao()
        parentUser=accountDao.getParentUserById(user_id)
        return outSuccess("parentUser", parentUser)
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("取得账号失败！")
    
if __name__=='__main__':
    # account = Account()
    # account.account_id = '733b351f-ba89-11e5-9774-fa163ee4b05699'
    # account.user_id = '123456789'
    # account.cash_balance = 2000.30
    # account.type = 'normal'
    # account.status = 'normal'
    # session = sa.get_session()
    # sql = 'select * from keystone.user where id=\'{}\''.format(str(account.user_id))
    # query = session.execute(sql).first()
    # if query.parent_id:
    #     parent_userid = query.parent_id
    #     sql2 = 'select * from billing.account where user_id=\'{}\''.format(str(parent_userid))
    #     query = session.execute(sql2).first()
    #     parent_account = query.account_id
    #     account.parent_account = parent_account
    # session.close()
    # accountDao = AccountDao(account)
    # accountDao.add()
    result = detail('733b351f-ba89-11e5-9774-fa163ee4b056')
    print result
