# -*- coding:utf-8 -*-
'''
Created on 2015年10月14日

@author: greshem
'''
from dashboard.views.base import HomePageView
from django.http.response import HttpResponse
from dashboard.api.requestClient import request as req
import json
import datetime
class Index(HomePageView):
    template_name = "subComsumption/subComsumption.html"
 
    def get_data(self):
        account_id=self.request.session.get('account')['account_id']
        result = req('account/subaccountamountsum/%s'%account_id)
        res = {}
        title_list = [{"name":"子帐号账户管理"}]
        res["title_list"] = title_list
        if result['success'] == 'success':
            res['sunAccountAmountSum'] = result['sunAccountAmountSum']
        return res


class DetailView(HomePageView):
    template_name = "subComsumption/detail.html"
    
    def get_data(self):
        account_id = self.request.GET['sub_account_id']
        name = self.request.GET['name']
        data = {'account_id':account_id, 'name':name}
        started_at = datetime.datetime.strftime(datetime.datetime.utcnow(), '%Y-%m') + '-01'
        result = req('/consumption/getamountsummary/%s?started_at=%s' % (account_id, started_at))
        if result['success'] == 'success':
            data.update(result['amountsummary'])
        data.update({'started_at':started_at})
        title_list = [{"name":"子账号消耗管理", "url":"/center/subComsumption"}, {"name":name}]
        data["title_list"] = title_list
        return data

class ConsumptionHistoryView(HomePageView):
    template_name = "subComsumption/consumption_history.html"
    
    def get_data(self):
        account_id = self.request.GET['sub_account_id']
        name = self.request.GET['name']
        data = {'account_id':account_id, 'name':name}
        result = req('/account/detail/%s' % account_id)
        if result['success'] == 'success':
            data['account'] = result['account']
        title_list = [{"name":"子账号消耗管理", "url":"/center/subComsumption"}, {"name":"历史消耗"}, {"name":name}]
        data["title_list"] = title_list
        return data

class BillDetailView(HomePageView):
    template_name = "subComsumption/bill_detail.html"
    
    def get_data(self):
        bill_id = self.request.GET['bill_id']
        account_id = self.request.GET['account_id']
        no = self.request.GET['no']
        name = self.request.GET['name']
        data = {'bill_id':bill_id, 'account_id':account_id, 'no':no, 'name':name}
        result = req('/bill/detail/%s' % bill_id)
        if result['success'] == 'success':
            data.update(result['bill'])
        title_list = [{"name":"子账号消耗管理", "url":"/center/subComsumption"}, {"name":"历史消费", "url":"/center/subComsumption/consumptionhistory?account_id=" + account_id + "&name=" + name}, {"name":name}, {"name":no}]
        data["title_list"] = title_list
        return data
    
    
def getSubComsumptionList(request):
    pageSize = int(request.GET['limit'])
    pageNo = int(request.GET['offset']) / pageSize + 1
    account_id=request.session.get('account')['account_id']
    url = "/account/subaccountconsumptionlist/"+account_id+"?pageNo=" + str(pageNo) + "&pageSize=" + str(pageSize)
    if request.GET.has_key('name'):
        url += '&name=' + request.GET['name']
    if request.GET.has_key('type'):
        url += '&type=' + request.GET['type']
    result = req(url)
    data = {'total':result['subAccountConsumptionList']['total'], 'rows':result['subAccountConsumptionList']['accounts']}
    return HttpResponse(json.dumps(data))

def getConsumptionSummary(request):
    account_id = request.GET['account_id']
    result = req("/consumption/getconsumptionsummary/%s" % account_id)
    return HttpResponse(json.dumps(result['consumptionsummary']))

def getBillList(request):
    pageSize = int(request.GET['limit'])
    pageNo = int(request.GET['offset']) / pageSize + 1
    account_id = request.GET['account_id']
    url = "/bill/list/%s?pageNo=%s&pageSize=%s" % (account_id, pageNo, pageSize)
    if request.GET.has_key('started_at'):
        url += '&started_at=' + request.GET['started_at'] + '-01'
    if request.GET.has_key('ended_at'):
        url += '&ended_at=' + request.GET['ended_at'] + '-01'
    result = req(url)
    data = {'total':result['billList']['total'], 'rows':result['billList']['bills']}
    return HttpResponse(json.dumps(data))

def getBillDetail(request):
    bill_id = request.GET['bill_id']
    result = req("/bill/billitemlist/%s" % bill_id)
    return HttpResponse(json.dumps(result['billitemList']))
