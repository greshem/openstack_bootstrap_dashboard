# -*- coding:utf-8 -*-
from billing.db.sqlalchemy import session as sa
from billing.constant.sql import SQL
from oslo_log import log as logging
from billing.util.handlerUtil import *
from billing.db.dao.InvoiceDao import InvoiceDao
from billing.db.dao.ConsumptionDao import ConsumptionDao
from billing.hander.Bill import getBillDetail
from billing.hander.Invoice import detail
from billing.db.object.models import Invoice
import json
from re import search
import traceback
import calendar
from datetime import datetime,timedelta
import re
from billing.constant.constant import constVar


LOG=logging.getLogger(__name__)

#  ----Invoice Begin----
def getinvoiceList(page_no,page_size,condition=None,**args):
    try:
        session=sa.get_session()
        accountsql=SQL.accountInfoSql_2
        invoicesql=SQL.invoiceListSql
        if condition:
            for key,value in condition.items():
                if key=='type':
                    accountsql += ' and type=\'%s\''%value
                if key=='role':
                    if value=='user':
                        accountsql += ' and role in(\'user\',\'_member_\') and parent_role=\'admin\''
                    if value=='project_admin':
                        accountsql += ' and role=\'project_admin\''
                    if value=='project_sub':
                        accountsql += ' and role in(\'user\',\'_member_\') and parent_role=\'project_admin\''
                    if value=='admin':
                        accountsql += ' and role=\'admin\''
                if key=='companylike':
                    value1='%'
                    value2='%'
                    if '_' in value:
                        value=value.replace('_','\_')
                    accountsql += ' and company like \'%s%s%s\''%(value1,value,value2)
                if key=='usernamelike':
                    value1='%'
                    value2='%'
                    if '_' in value:
                        value=value.replace('_','\_')
                    accountsql += ' and username like \'%s%s%s\''%(value1,value,value2)
                if key=='invoicelike':
                    value1='%'
                    value2='%'
                    invoicesql += ' and invoice_no like \'%s%s%s\''%(value1,value,value2)
                if key=='process_by':
                    invoicesql += ' and process_by=\'%s\''%value
                if key=='invoice_status':
                    if value=='apply':
                        invoicesql += ' and status= \'%s\''%value
                    else:
                        invoicesql += ' and status!=\'apply\''
                if key=='process_started':
                    invoicesql += ' and process_at >= \'%s\''%value
                if key=='process_ended':
                    invoicesql += ' and process_at <= \'%s\''%value
                if key=='apply_started':
                    invoicesql += ' and apply_at >= \'%s\''%value
                if key=='apply_ended':
                    invoicesql += ' and apply_at <= \'%s\''%value
        invoicesql += ' order by status,apply_at desc'
        invoiceList=session.execute(invoicesql).fetchall()
        account_temp=session.execute(accountsql).fetchall()
        result=[]
        for item in invoiceList:
            tempdict={}
            tempdict['account_id']=item.account_id
            tempdict['invoice_no']=item.invoice_no
            tempdict['invoice_id']=item.invoice_id
            tempdict['invoice_status']=item.status
            tempdict['amount']=item.amount
            tempdict['apply_at']=item.apply_at
            tempdict['process_at']=item.process_at
            tempdict['process_by']=item.process_by
            accountinfo=None
            for item in account_temp:
                if item.account_id==tempdict['account_id']:
                    accountinfo=item
            if accountinfo:
                tempdict['account_id']= accountinfo.account_id
                tempdict['username']  = accountinfo.username
                tempdict['type']      = accountinfo.type
                tempdict['company']   = accountinfo.company
                if accountinfo.role=='user' or accountinfo.role=='_member_':
                    if accountinfo.parent_role=='admin':
                        tempdict['finally_role']='common_user'
                    elif accountinfo.parent_role=='project_admin':
                        tempdict['finally_role']='project_subaccount'
                    else:
                        tempdict['finally_role']=None
                elif accountinfo.role=='project_admin':
                    tempdict['finally_role']='project_admin'
                elif accountinfo.role=='admin':
                    tempdict['finally_role']='admin'
                else:
                    tempdict['finally_role']=None
                result.append(tempdict)
        count=len(result)
        treated_amount=0
        untreated_amount=0
        for item in result:
            amount=item['amount'] if item['amount'] else 0
            if item['invoice_status']=='apply':
                untreated_amount += amount
            if item['invoice_status']=='treated':
                treated_amount += amount
        result=result[(page_no-1)*page_size:(page_no*page_size)]
        return json.dumps({'count':count,'treated_amount':treated_amount,'untreated_amount':untreated_amount,'invoice_list':result,'success':'success'},cls=CJsonEncoder, ensure_ascii=False)
    except Exception as e:
        session.close()
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("获取发票管理列表失败!")

def getinvoiceDetail(invoice_id,headers=None, **kwargs):
    try:
        session=sa.get_session()
        resultjson=detail(invoice_id,headers,**kwargs)
        result=json.loads(resultjson)
        account_id=result['invoice']['account_id']
        company=None
        username=None
        companyquery=session.execute(SQL.getCompanyInfoByAccount,dict({'account_id':account_id})).first()
        if companyquery:
            company=companyquery.company
            username=companyquery.username
        result['company']=company
        result['username']=username
        return json.dumps(result,ensure_ascii=False)
    except Exception as e:
        session.close()
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("获取发票详情失败!")

def invoiceHandle(exitcontent):
    try:
        session=sa.get_session()
        invoice_id=exitcontent['invoice_id']
        updateitem=['invoice_no','post_by','express_no','process_by','status']
        for item in updateitem:
            if exitcontent.has_key(item):
                pass
            else:
                exitcontent[item]=None
        process_at=datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        exitcontent['process_at']=process_at
        exitcontent['invoice_id']=invoice_id
        session.execute(SQL.invoiceHandleSql,exitcontent)
        return outSuccess('result',"发票处理成功")
    except Exception as e:
        session.close()
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("发票处理失败!")


#  ----Bill Begin----
def getbillList(page_no,page_size,condition=None,**args):
    try:
        session=sa.get_session()
        billsql='select * from bill having 1=1'
        accountsql=SQL.accountInfoSql_2
        if condition:
            for key,value in condition.items():
                if key=='started_at':
                    value += ' 00:00:00'
                    billsql += '  and started_at >= \'%s\''%value
                if key=='ended_at':
                    value += ' 23:59:59'
                    billsql += ' and ended_at <= \'%s\''%value
                if key=='billnolike':
                    value1='%'
                    value2='%'
                    billsql += ' and no like \'%s%s%s\''%(value1,value,value2)
                if key=='companylike':
                    value1='%'
                    value2='%'
                    if '_' in value:
                        value=value.replace('_','\_')
                    accountsql += ' and company like \'%s%s%s\''%(value1,value,value2)
                if key=='usernamelike':
                    value1='%'
                    value2='%'
                    if '_' in value:
                        value=value.replace('_','\_')
                    accountsql += ' and username like \'%s%s%s\''%(value1,value,value2)
                if key=='type':
                    accountsql += ' and type=\'%s\''%value
                if key=='status':
                    accountsql += ' and status =\'%s\''%value
                if key=='role':
                    if value=='user':
                        accountsql += ' and role in(\'user\',\'_member_\') and parent_role=\'admin\''
                    if value=='project_admin':
                        accountsql += ' and role=\'project_admin\''
                    if value=='project_sub':
                        accountsql += ' and role in(\'user\',\'_member_\') and parent_role=\'project_admin\''
                    if value=='admin':
                        accountsql += ' and role=\'admin\''
        billsql += ' order by started_at desc'
        bill_result=session.execute(billsql).fetchall()
        account_result=session.execute(accountsql).fetchall()
        result=[]
        bill_amount=0
        if bill_result:
            for item in bill_result:
                tempdict={}
                tempdict['no']=item.no
                tempdict['account_id']=item.account_id
                tempdict['started_at']=item.started_at
                tempdict['ended_at']=item.ended_at
                tempdict['amount']=item.amount
                tempdict['bill_id']=item.bill_id
                accountinfo=None
                for item in account_result:
                    if item.account_id==tempdict['account_id']:
                        accountinfo=item
                if accountinfo:
                    tempdict['company']=accountinfo.company
                    tempdict['type']=accountinfo.type
                    tempdict['username']=accountinfo.username
                    tempdict['status']=accountinfo.status
                    if accountinfo.role=='user' or accountinfo.role=='_member_':
                        if accountinfo.parent_role=='admin':
                            tempdict['finally_role']='common_user'
                        elif accountinfo.parent_role=='project_admin':
                            tempdict['finally_role']='project_subaccount'
                        else:
                            tempdict['finally_role']=None
                    elif accountinfo.role=='project_admin':
                        tempdict['finally_role']='project_admin'
                    elif accountinfo.role=='admin':
                        tempdict['finally_role']='admin'
                    else:
                        tempdict['finally_role']=None
                    result.append(tempdict)
        count=len(result)
        if result:
            for item in range(len(result)):
                bill_amount += result[item]['amount'] if result[item]['amount'] else 0
        result=result[(page_no-1)*page_size:(page_no*page_size)]
        return json.dumps({'count':count,'bill_amount':bill_amount,'billlist':result,'success':'success'},cls=CJsonEncoder, ensure_ascii=False)
    except Exception as e:
        session.close()
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("获取消费管理列表失败!")

def getbilldetailInfo(bill_id):
    return getBillDetail(bill_id)


# ----Recharge Begin----
def local2utc(date,time):
    date_list=date.split('-')
    time_list=time.split(':')
    year=int(date_list[0])
    month=int(date_list[1])
    day=int(date_list[2])
    hour=int(time_list[0])
    minute=int(time_list[1])
    second=int(time_list[2])
    utc_time=datetime(year,month,day,hour,minute,second)-timedelta(hours=8)
    return utc_time.strftime('%Y-%m-%d %H:%M:%S')

def getaccountinfobyid(accountlist,account_id):
    for item in accountlist:
        if item.account_id==account_id:
            return item

def getrechargeList(page_no,page_size,condition=None,**args):
    try:
        session=sa.get_session()
        rechargelist=SQL.rechargeListSql
        giftrechargelist=SQL.giftRechargeListSql
        accountsql=SQL.accountInfoSql_2
        if condition:
            for key,value in condition.items():
                if key=='type':
                    accountsql += ' and type=\'%s\''%value
                if key=='role':
                    if value=='user':
                        accountsql += ' and role in (\'user\',\'_member_\') and parent_role=\'admin\''
                    if value=='project_admin':
                        accountsql += ' and role=\'project_admin\''
                    if value=='project_sub':
                        accountsql += ' and role in(\'user\',\'_member_\') and parent_role=\'project_admin\''
                    if value=='admin':
                        accountsql += ' and role=\'admin\''
                if key=='companylike':
                    value1='%'
                    value2='%'
                    if '_' in value:
                        value=value.replace('_','\_')
                    accountsql += ' and company like \'%s%s%s\''%(value1,value,value2)
                if key=='usernamelike':
                    value1='%'
                    value2='%'
                    if '_' in value:
                        value=value.replace('_','\_')
                    accountsql += ' and username like \'%s%s%s\''%(value1,value,value2)
                if key=='min_amount':
                    rechargelist += ' and amount >= %f'%float(value)
                    giftrechargelist += ' and amount >= %f'%float(value)
                if key=='max_amount':
                    rechargelist += ' and amount <= %f'%float(value)
                    giftrechargelist += ' and amount <= %f'%float(value)
                if key=='pay_started':
                    value = local2utc(value,'00:00:00')
                    rechargelist += ' and pay_at >=\'%s\''%value
                    giftrechargelist += ' and pay_at >=\'%s\''%value
                if key=='pay_ended':
                    value = local2utc(value,'23:59:59')
                    rechargelist += ' and pay_at <=\'%s\''%value
                    giftrechargelist += ' and pay_at <=\'%s\''%value
                if key=='ordernolike':
                    value1='%'
                    value2='%'
                    if '_' in value:
                        value=value.replace('_','\_')
                    value=str(value)
                    rechargelist += ' and order_no like \'%s%s%s\''%(value1,value,value2)
                    giftrechargelist += ' and order_no like \'%s%s%s\''%(value1,value,value2)
                if key=='recharge_type':
                    if value=='recharge':
                        rechargelist += ' and (recharge_id is not null) and (instead_recharge_id is null)'
                    if value=='instead_recharge':
                        rechargelist += ' and ((recharge_id + instead_recharge_id)is not null)'
                if key=='recharge_way':
                    if value=='offline_pay':
                        rechargelist += ' and payment_way in (\'transfer_pay\',\'offline_pay\')'
                        giftrechargelist += ' and payment_way in (\'transfer_pay\',\'offline_pay\')'
                    if value=='alipay':
                        rechargelist += ' and payment_way like \'alipay%\''
                        giftrechargelist += ' and payment_way like \'alipay%\''
        rechargelist1=rechargelist
        giftrechargelist1=giftrechargelist
        rechargelist += ' order by pay_at desc'
        giftrechargelist += ' order by pay_at desc'
        recharge_temp=session.execute(rechargelist).fetchall()
        gift_temp=session.execute(giftrechargelist).fetchall()
        account_temp=session.execute(accountsql).fetchall()
        recharge_result=[]
        gift_result=[]
        if recharge_temp:
            for item in recharge_temp:
                tempdict={}
                tempdict['order_no']=item.order_no
                tempdict['amount']=item.amount
                tempdict['account_id']=item.account_id
                tempdict['pay_at']=item.pay_at
                tempdict['operate_by']=item.operate_by
                tempdict['recharge_id']=item.recharge_id
                tempdict['instead_recharge_id']=item.instead_recharge_id
                tempdict['payment_way']=item.payment_way
                tempaccount=None
                for item in account_temp:
                    if item.account_id==tempdict['account_id']:
                        tempaccount=item
                if tempaccount:
                    tempdict['company']=tempaccount.company
                    tempdict['username']=tempaccount.username
                    tempdict['type']=tempaccount.type
                    if tempaccount.role=='user' or tempaccount.role=='_member_':
                        if tempaccount.parent_role=='admin':
                            tempdict['finally_role']='common_user'
                        elif tempaccount.parent_role=='project_admin':
                            tempdict['finally_role']='project_subaccount'
                        else:
                            tempdict['finally_role']=None
                    elif tempaccount.role=='project_admin':
                        tempdict['finally_role']='project_admin'
                    elif tempaccount.role=='admin':
                        tempdict['finally_role']='admin'
                    else:
                        tempdict['finally_role']=None
                    recharge_result.append(tempdict)
        if gift_temp:
            for item in gift_temp:
                tempdict={}
                tempdict['order_no']=item.order_no
                tempdict['amount']=item.amount
                tempdict['account_id']=item.account_id
                tempdict['pay_at']=item.pay_at
                tempdict['operate_by']=item.operate_by
                tempdict['payment_type']=item.payment_type
                tempaccount=None
                for item in account_temp:
                    if item.account_id==tempdict['account_id']:
                        tempaccount=item
                if tempaccount:
                    tempdict['company']=tempaccount.company
                    tempdict['username']=tempaccount.username
                    tempdict['type']=tempaccount.type
                    if tempaccount.role=='user' or tempaccount.role=='_member_':
                        if tempaccount.parent_role=='admin':
                            tempdict['finally_role']='common_user'
                        elif tempaccount.parent_role=='project_admin':
                            tempdict['finally_role']='project_subaccount'
                        else:
                            tempdict['finally_role']=None
                    elif tempaccount.role=='project_admin':
                        tempdict['finally_role']='project_admin'
                    elif tempaccount.role=='admin':
                        tempdict['finally_role']='admin'
                    else:
                        tempdict['finally_role']=None
                    gift_result.append(tempdict)
        recharge_amount=0
        gift_amount=0
        if condition is not None and condition.has_key('recharge_type'):
            if condition['recharge_type']=='recharge':
                if recharge_result:
                    for item in range(len(recharge_result)):
                        recharge_result[item]['payment_type']='recharge'
                        recharge_amount += recharge_result[item]['amount']
                count=len(recharge_result)
                recharge_result=recharge_result[(page_no-1)*page_size:(page_no*page_size)]
                return json.dumps({'count':count,'recharge_amount':recharge_amount,'gift_amount':gift_amount,'rechargelist':recharge_result,'success':'success'},cls=CJsonEncoder, ensure_ascii=False)
            if  condition['recharge_type']=='instead_recharge':
                if recharge_result:
                    for item in range(len(recharge_result)):
                        recharge_result[item]['payment_type']='instead_recharge'
                        recharge_amount += recharge_result[item]['amount']
                count=len(recharge_result)
                recharge_result=recharge_result[(page_no-1)*page_size:(page_no*page_size)]
                return json.dumps({'count':count,'recharge_amount':recharge_amount,'gift_amount':gift_amount,'rechargelist':recharge_result,'success':'success'},cls=CJsonEncoder, ensure_ascii=False)
            if  condition['recharge_type']=='gift':
                if gift_result:
                    for item in range(len(gift_result)):
                        gift_amount += gift_result[item]['amount']
                count=len(gift_result)
                gift_result=gift_result[(page_no-1)*page_size:(page_no*page_size)]
                return json.dumps({'count':count,'recharge_amount':recharge_amount,'gift_amount':gift_amount,'rechargelist':gift_result,'success':'success'},cls=CJsonEncoder, ensure_ascii=False)
        else:
            total_result_sql=rechargelist1+' union all '+giftrechargelist1+' order by pay_at desc'
            total_temp=session.execute(total_result_sql).fetchall()
            total_result=[]
            recharge_amount,gift_amount=0,0
            if total_temp:
                for item in total_temp:
                    tempdict={}
                    tempdict['order_no']=item.order_no
                    tempdict['amount']=item.amount
                    tempdict['account_id']=item.account_id
                    tempdict['pay_at']=item.pay_at
                    tempdict['operate_by']=item.operate_by
                    tempdict['payment_way']=item.payment_way
                    if item.payment_type=='recharge':
                        if item.instead_recharge_id is not None:
                            tempdict['payment_type']='instead_recharge'
                        else:
                            tempdict['payment_type']='recharge'
                        recharge_amount += item.amount
                    else:
                        tempdict['payment_type']='gift'
                        gift_amount += item.amount
                    tempaccount=None
                    for item2 in account_temp:
                        if item2.account_id==tempdict['account_id']:
                            tempaccount=item2
                    if tempaccount:
                        tempdict['company']=tempaccount.company
                        tempdict['username']=tempaccount.username
                        tempdict['type']=tempaccount.type
                        if tempaccount.role=='user' or tempaccount.role=='_member_':
                            if tempaccount.parent_role=='admin':
                                tempdict['finally_role']='common_user'
                            elif tempaccount.parent_role=='project_admin':
                                tempdict['finally_role']='project_subaccount'
                            else:
                                tempdict['finally_role']=None
                        elif tempaccount.role=='project_admin':
                            tempdict['finally_role']='project_admin'
                        elif tempaccount.role=='admin':
                            tempdict['finally_role']='admin'
                        else:
                            tempdict['finally_role']=None
                        total_result.append(tempdict)
            count=len(total_result)
            total_result=total_result[(page_no-1)*page_size:(page_no*page_size)]
            return json.dumps({'count':count,'recharge_amount':recharge_amount,'gift_amount':gift_amount,'rechargelist':total_result,'success':'success'},cls=CJsonEncoder, ensure_ascii=False)
# #******************************************
#             if recharge_result:
#                 for item in range(len(recharge_result)):
#                     if recharge_result[item]['instead_recharge_id'] is None:
#                         recharge_result[item]['payment_type']='recharge'
#                     else:
#                         recharge_result[item]['payment_type']='instead_recharge'
#                     recharge_amount += recharge_result[item]['amount']
#             if gift_result:
#                 for item in range(len(gift_result)):
#                     gift_amount += gift_result[item]['amount']
#             result=recharge_result+gift_result
#             count=len(result)
#             result=result[(page_no-1)*page_size:(page_no*page_size)]
#             return json.dumps({'count':count,'recharge_amount':recharge_amount,'gift_amount':gift_amount,'rechargelist':result,'success':'success'},cls=CJsonEncoder, ensure_ascii=False)
    except Exception as e:
        session.close()
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("获取充值列表失败!")

def getrechargeAmount():
    try:
        amount={}
        session=sa.get_session()
        result1=session.execute(SQL.rechargeAmountSql).first()
        result2=session.execute(SQL.giftAmountSql).first()
        recharge_amount=result1['recharge_amount'] if result1 else 0
        gift_amount=result2['gift_amount'] if result2 else 0
        amount['recharge_amount']=recharge_amount
        amount['gift_amount']=gift_amount
        return outSuccess('amount',amount)
    except Exception as e:
        session.close()
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("获取充值总额失败!")

def getrechargeDetail(order_no,headers=None,**kwargs):
    try:
        session=sa.get_session()
        account_id=session.execute('select account_id from `order` where order_no=\'%s\''%order_no).first().account_id
        alipay_info=session.execute('select pay_account,trade_no,pay_at from alipay_info where order_no=\'%s\''%order_no).first()
        recharge_info=session.execute('select created_at,amount,remark from recharge where order_no=\'%s\''%order_no).first()
        account_info=session.execute(SQL.getCompanyInfoByAccount,dict({'account_id':account_id})).first()
        detaildict={}
        detaildict['trade_no']=alipay_info.trade_no if alipay_info else None
        detaildict['pay_at']=alipay_info.pay_at if alipay_info else None
        detaildict['pay_account']=alipay_info.pay_account if alipay_info else None
        detaildict['created_at']=recharge_info.created_at if recharge_info else None
        detaildict['amount']=recharge_info.amount if recharge_info else None
        detaildict['remark']=recharge_info.remark if recharge_info else None
        detaildict['company']=account_info.company if account_info else None
        detaildict['phone']=account_info.telephone if account_info else None
        detaildict['username']=account_info.username if account_info else None
        return outSuccess('rechargedetail',detaildict)
    except Exception as e:
        session.close()
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("获取充值列表失败!")
#××××××××××充值详情改进××××××××××
def getrechargeDetail2(order_no,tempdict,headers=None,**kwargs):
    try:
        session=sa.get_session()
        recharge_detail={}
        detail_info={}
        other_info={}
        abstract_info=tempdict
        if abstract_info.has_key('pay_type') and abstract_info['pay_type']=='gift':
            pay_query=session.execute('select * from gift where order_no=\'%s\''%order_no).first()
            pay_at=pay_query.gift_at if pay_query else None
        else:
            pay_query=session.execute('select * from recharge where order_no=\'%s\''%order_no).first()
            pay_at=pay_query.pay_at if pay_query else None
        abstract_info['pay_date']=pay_at
        recharge_detail['abstract_info']=abstract_info
        order_info=session.execute('select * from `order` where order_no=\'%s\''%order_no).first()
        account_id=order_info.account_id
        payment_type=order_info.payment_type
        if payment_type=='gift':
            gift_query=session.execute('select * from gift where order_no=\'%s\''%order_no).first()
            gift_id=gift_query.gift_id
            remark=gift_query.remark
            detail_info['serial_number']=gift_id
            other_info['remark']=remark
            recharge_detail['detail_info']=detail_info
            recharge_detail['other_info']=other_info
            return outSuccess('rechargedetail',recharge_detail)
        else:
            if abstract_info['pay_way']=='transfer_pay' or abstract_info['pay_way']=='offline_pay':
                recharge_info=session.execute('select recharge_id,remark from recharge where order_no=\'%s\''%order_no).first()
                recharge_id=recharge_info.recharge_id
                transfer_info=session.execute('select * from transfer_info where recharge_id=\'%s\''%recharge_id).first()
                detail_info['serial_number']=transfer_info.trade_no if transfer_info else None
                detail_info['company_out']=transfer_info.remittance_corporation if transfer_info else None
                detail_info['company_in']=transfer_info.inward_corporation if transfer_info else None
                detail_info['account_out']=transfer_info.remittance_account if transfer_info else None
                detail_info['pay_date']=transfer_info.inward_at if transfer_info else None
                detail_info['bank_out']=transfer_info.remittance_bank if transfer_info else None
                detail_info['account_in']=transfer_info.inward_account if transfer_info else None
                detail_info['amount']=transfer_info.amount if transfer_info else None
                detail_info['bank_in']=transfer_info.inward_bank if transfer_info else None
                other_info['remark']=recharge_info.remark
                recharge_detail['detail_info']=detail_info
                recharge_detail['other_info']=other_info
                return outSuccess('rechargedetail',recharge_detail)
            else:
                alipay_info=session.execute('select * from alipay_info where order_no=\'%s\''%order_no).first()
                detail_info['serial_number']=alipay_info.trade_no if alipay_info else None
                detail_info['company_out']=None
                detail_info['company_in']=None
                detail_info['account_out']=alipay_info.pay_account if alipay_info else None
                detail_info['pay_date']=alipay_info.pay_at if alipay_info else None
                detail_info['bank_out']=None
                detail_info['account_in']=None
                detail_info['amount']=alipay_info.amount if alipay_info else None
                detail_info['bank_in']=None
                recharge_detail['detail_info']=detail_info
                other_info['remark']=alipay_info.remark if alipay_info else None
                recharge_detail['other_info']=other_info
                prin=r'^alipay.*'
                if re.match(prin,abstract_info['pay_way']):
                    distri_info={}
                    account_info=session.execute(SQL.getCompanyInfoByAccount,dict({'account_id':account_id})).first()
                    distri_info['company']=account_info.company
                    distri_info['username']=account_info.username
                    distri_info['usertype']=tempdict['user_type']
                    distri_info['account_type']=tempdict['account_type']
                    recharge_detail['distri_info']=distri_info
                    return outSuccess('rechargedetail',recharge_detail)
                else:
                    return outSuccess('rechargedetail',recharge_detail)
    except Exception as e:
        session.close()
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("获取充值详情失败!")

if __name__ =='__main__':
    temp=getrechargeDetail2('16031432167790',{'account_type':'account','pay_way':'offline_pay','user_type':'normal'})
    print temp
