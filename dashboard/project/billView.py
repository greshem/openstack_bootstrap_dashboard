# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http.response import HttpResponse
import datetime
from dashboard.api.requestClient import request as req
from dashboard.views.base import HomePageView
import json
import django.views.generic as classview
from dashboard.views.base import BillReqMixin
from dashboard.api.requestClient import request as billing_req
from .utils import *
from django.http import HttpResponse,HttpResponseRedirect

class BillView(HomePageView):
    '''
    账单
    '''
    template_name = "bill/bill_ajax.html"
    def get(self, request, *args, **kwargs):
        return super(BillView,self).get(request,*args,**kwargs)
    def post(self,request,*args,**kwargs):
        pass
    def get_data(self):
        title_list=[{"name":"账单","url":"/center/bill"}]
        return {'b':1,"title_list":title_list}

class BillDetailView(HomePageView):
    '''
    账单详情
    '''
    template_name = "bill/details_ajax.html"

    def get_data(self):
        bill_id=self.request.GET['bill_id']
        result=req("bill/detail/%s"%bill_id)
        amount=result['bill']['amount']
        bill_no=result['bill']['no']
        title_list=[{"name":"账单","url":"/center/bill"},{"name":bill_no,"url":"/center/bill/detail?bill_id="+bill_id}]
        dateFrom=result['bill']['started_at']
        dateTo=result['bill']['ended_at']
        return {'bill_id':bill_id,'amount':amount,'dateFrom':dateFrom,'dateTo':dateTo,"title_list":title_list}

def getformatdate(datetime):
    date=datetime.split()[0]
    datelist=date.split('-')
    formattime=datelist[0]+'-'+datelist[1]
    return formattime

def getbillList(request):
     account_id=request.session.get('account')['account_id']
     # account_id='123hdfsfbsdf7uuieruiteb'
     pageSize=int(request.GET['limit'])
     pageNo=int(request.GET['offset'])/pageSize+1
     dateFrom=request.GET['dateFrom']
     dateTo=request.GET['dateTo']
     bill_type=request.GET.get('type')
     url="/bill/list/%s?pageNo=%s&pageSize=%s" %(account_id,pageNo,pageSize)
     if (len(dateFrom)==0) or (len(dateTo)==0):
         if(len(dateFrom)==0) and (len(dateTo)!=0):
             ended_at=getformatdate(dateTo)+'-01'
             url+='&ended_at='+ended_at
         elif (len(dateFrom)!=0) and (len(dateTo)==0):
             started_at=getformatdate(dateFrom)+'-01'
             url+='&started_at='+started_at
     else:
         started_at=getformatdate(dateFrom)+'-01'
         ended_at=getformatdate(dateTo)+'-01'
         url+='&started_at='+started_at+'&ended_at='+ended_at
     if bill_type:
        url += '&bill_type=%s' % bill_type
     result=req(url)
     data=result['billList']['bills']
     #for i in range(len(data)):
     #    if len(data[i]['ended_at'])!=0:
     #        data[i]['ended_at']=data[i]['ended_at'].split()[0]
     #    if len(data[i]['started_at'])!=0:
     #        data[i]['started_at']=data[i]['started_at'].split()[0]
     data2 = {'total':result['billList']['total'], 'rows':data}
     return HttpResponse(json.dumps(data2))

def getbillDetail(request):
    bill_id = request.GET['bill_id']
    result = req("/bill/detail/%s" % bill_id)
    return HttpResponse(json.dumps(result['bill']['bill_items']))


