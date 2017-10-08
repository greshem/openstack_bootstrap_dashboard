# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http.response import HttpResponse
from dashboard.api.requestClient import request as req
from dashboard.views.base import HomePageView
import json
import django.views.generic as classview
from dashboard.views.base import BillReqMixin
from dashboard.api.requestClient import request as billing_req
from .utils import *
from django.http import HttpResponse,HttpResponseRedirect
from dashboard.constant.constant import const
import string
from dashboard.logaction.logger import Logger
from dashboard.util.jsonUtil import outJson
from dashboard.api.requestClient import request as billing_req
from django.conf import settings
class  BusinessView(BillReqMixin,HomePageView):
    '''
    子帐号账户管理
    '''
    template_name= "business/instead_recharge.html"
    def get(self, request, *args, **kwargs):
        return super(BusinessView,self).get(request, *args, **kwargs)

    def get_data(self):
        account_id=self.request.session.get("account")["account_id"]
        #account_id="asdasdadasfftgerr"
        return_info={}
        temp=billing_req("/account/getsubaccountsum/"+account_id)["subAccountSum"]
        return_info["credit_child_num"]=temp["credit_sum"]
        return_info["general_child_num"]=temp["sum"]-temp["credit_sum"]
        return_info["account_info"]=billing_req("/account/detail/"+account_id)["account"]
        title_list=[{"name":"子帐号账户管理","url":"/center/account_manage"}]
        return_info["title_list"]=[]
        return return_info


def  insteadRecharge(request):
    '''
    近期消费记录
    '''
    recharge_data=json.loads(request.POST["recharge"])
    recharge_data["recharge"]["amount"]=float(recharge_data["recharge"]["amount"])
    request_url="/recharge/insteadrecharge"
    response=billing_req(request_url,data=json.dumps(recharge_data),method="POST")
    if response['success']=="success":
        return_data="success"
    else:
        return_data="fail"
    return HttpResponse(return_data)

def  giftRecharge(request,*args,**kwargs):
    '''
    一般赠送
    '''
    account_id=kwargs["account_id"]
    recharge_data=json.loads(request.POST["recharge"])
    recharge_data["gift"]["amount"]=float(recharge_data["gift"]["amount"])
    request_url="/gift/giftamount/"+account_id
    if recharge_data["gift"]["amount"]>0:
        response=billing_req(request_url,data=json.dumps(recharge_data),method="POST")
        if response['success']=="success":
            return_data="success"
        else:
            return_data="fail"
    else:
        return_data="fail"
    return HttpResponse(return_data)

def  firstGift(request,*args,**kwargs):
    '''
    首次赠送
    '''
    account_id=kwargs["account_id"]
    recharge_data=json.loads(request.POST["recharge"])
    recharge_data["gift"]["amount"]=float(recharge_data["gift"]["amount"])
    request_url="/gift/firstamount/"+account_id
    if recharge_data["gift"]["amount"]>0 and  recharge_data["gift"]["amount"]<=settings.GIFT_VALUE:
        response=billing_req(request_url,data=json.dumps(recharge_data),method="POST")
        if response['success']=="success":
            return_data="success"
        else:
            return_data="fail1"
    else:
        return_data="fail2"
    return HttpResponse(return_data)

class CreditLineFormView(HomePageView):
    template_name="business/credit_line.html"
    def get_data(self):
        account_id = self.request.GET['account_id']
        response = billing_req('account/detail/%s'%account_id)
        if response['success']=="success":
            type={'key':'normal','value':'普通账户'}if response['account']['type']=='normal' else {'key':'credit','value':'信用账户'}
            return {'account_id':account_id,'type':type,'credit_line':response['account']['credit_line']}
        return {}
def changeCreditLine(request,*args,**kwargs):
    '''
    修改信用额度
    '''
    if request.GET.has_key('account_id') and request.GET.has_key('credit_line'):
        account_id = request.GET['account_id']
        credit_line= request.GET['credit_line']
        response = billing_req('account/detail/%s'%account_id)
        result=None
        if response['account']['type']=='normal':
            result=billing_req('account/change2credit/%s?credit_line=%s'%(account_id,credit_line))
        else:
            result=billing_req('account/changecreditline/%s?credit_line=%s'%(account_id,credit_line))
        if result['success']=='success':
            return HttpResponse(json.dumps({'success':'success'}))
        else:
            return HttpResponse(json.dumps({'success':'error','msg':'修改信用额度失败'}))
    else:
        return HttpResponse(json.dumps({'success':'error','msg':'参数不对'}))
    
    
    
    