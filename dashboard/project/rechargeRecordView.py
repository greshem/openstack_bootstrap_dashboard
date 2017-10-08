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
import datetime

class RechargeRecordView(HomePageView):
    '''
    充值记录
    '''
    template_name = "rechargeRecord/rechargeRecord_ajax.html"
    def get(self, request, *args, **kwargs):
        return super(RechargeRecordView,self).get(request,*args,**kwargs)
    def post(self,request,*args,**kwargs):
        pass
    def get_data(self):
        title_list=[{"name":"充值记录","url":"/center/rechargeRecord"}]
        return {'r':1,"title_list":title_list}

def getformatdate(datetime):
    date=datetime.split()[0]
    # datelist=date.split('-')
    # formattime=datelist[0]+'-'+datelist[1]
    return date

def getrechargeRecordList(request):
    account_id=request.session.get('account')['account_id']
    payment_type=request.GET['payment_type']
    dateFrom=request.GET['dateFrom']
    dateTo=request.GET['dateTo']
    pageSize=int(request.GET['limit'])
    pageNo=int(request.GET['offset'])/pageSize+1
    url="/recharge/getorderrechargelist/%s?pageSize=%s&pageNo=%s"%(account_id,pageSize,pageNo)
    if payment_type=='all':
        if (len(dateFrom)==0) or (len(dateTo)==0):
            if(len(dateFrom)!=0) and (len(dateTo)==0):
                started_at=getformatdate(dateFrom)
                url+='&started_at='+started_at
            elif(len(dateFrom)==0) and (len(dateTo)!=0):
                ended_at=getformatdate(dateTo)
                url+='&ended_at='+ended_at
        else:
            started_at=getformatdate(dateFrom)
            ended_at=getformatdate(dateTo)
            url+='&started_at='+started_at+'&ended_at='+ended_at
    else:
        if (len(dateFrom)==0) or (len(dateTo)==0):
            if(len(dateFrom)!=0) and (len(dateTo)==0):
                started_at=getformatdate(dateFrom)
                url+='&started_at='+started_at+'&payment_type='+payment_type
            elif(len(dateFrom)==0) and (len(dateTo)!=0):
                ended_at=getformatdate(dateTo)
                url+='&ended_at='+ended_at+'&payment_type='+payment_type
            else:
                url+='&payment_type='+payment_type
        else:
            started_at=getformatdate(dateFrom)
            ended_at=getformatdate(dateTo)
            url+='&started_at='+started_at+'&ended_at='+ended_at+'&payment_type='+payment_type
    result=req(url)
    if result['success']=='success':
        total=result['billList']['total']
        data=result['billList']['bills']
        for i in range(len(data)):
            if data[i]['payment_type']=='gift':
                data[i]['payment_type']='赠送'
            else :
                data[i]['payment_type']='充值'
        return HttpResponse(json.dumps({'total':total,'rows':data}))
    else:
        return HttpResponse(json.dumps({'total':0,'rows':[]}))


