# -*- coding: utf-8 -*-
__author__ = 'arsene'
from django.shortcuts import render, render_to_response
from django.http.response import HttpResponse
from dashboard.api.requestClient import request as req
from dashboard.views.base import HomePageView
import json
import django.views.generic as classview
from dashboard.views.base import BillReqMixin
from dashboard.api.requestClient import request as billing_req
from .utils import *
from django.http import HttpResponse,HttpResponseRedirect
from dashboard.logaction.logger import Logger


class InvoiceManageView(HomePageView):
    """
    发票管理
    """

    template_name = "invoicemanage/invoicemanage_ajax.html"
    def get(self, request, *args, **kwargs):
        return super(InvoiceManageView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pass

    def get_data(self):
        account_id=self.request.session.get('account')['account_id']
        result=req("invoice/list/%s" % account_id)
        result1=req("invoice/summary/%s" % account_id)['summary']
        invoices_list=result[u'invoiceList']['invoices']
        title_list=[{"name":"发票管理", "url":"/center/invoice_manange"}]
        return {'invoices': invoices_list, "title_list":title_list, 'summary': result1}


def prepareInvoiceData(request):
    account_id=request.session.get('account')['account_id']
    limit = request.GET['limit']
    page_no = int(request.GET['offset'])/(int(limit))+1
    result = req("invoice/list/%s?page_no=%s&page_size=%s" % (account_id, page_no, limit))
    data = {"total": result[u'invoiceList']["total"], 'rows':result[u'invoiceList']['invoices']}
    return HttpResponse(json.dumps(data))

def get_address_detail_by_addr_id(request):
    account_id=request.session.get('account')['account_id']
    address_id = request.GET['address_id']
    result = req('address/list/%s' % account_id)
    addr_list = result[u"addresses"]
    m=[i for i in addr_list if i[u'address_id']==int(address_id)][0]
    return HttpResponse(json.dumps(m))

def get_new_address_form(request):
    template1 = 'invoicemanage/add_new_addr.html'
    return render_to_response(template1, {'abc':'blank'})

def get_invoice_summary(request):
     account_id=request.session.get('account')['account_id']
     result=req("invoice/summary/%s" % account_id)['summary']
     if not result['bill_amount']:
         result['bill_amount']=0.00
     if not result['invoice_amount']:
         result['invoice_amount']=0.00

     result['bill_amount']=float(result['bill_amount'])
     result['invoice_amount']=float(result['invoice_amount'])

     result['invoice_amount_avail']=result['bill_amount']-result['invoice_amount']

     result['bill_amount']='%.2f' % (result['bill_amount'])
     result['invoice_amount']= '%.2f' % (result['invoice_amount'])
     result['invoice_amount_avail'] = '%.2f' % result['invoice_amount_avail']

     print result
     return HttpResponse(json.dumps(result))

class Sub_InvoiceAccountView(HomePageView):
    """
    用于响应发票账户地址列表请求
    """
    template_name = "invoicemanage/address_ajax.html"

    def get(self, request, *args, **kwargs):
        return super(Sub_InvoiceAccountView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        post_data=request.POST
        account_id=request.session.get('account')['account_id']

        if 'delete' in post_data:
            req("/address/delete/%s" % post_data['account_id'], method="DELETE")
            Logger(request).create(resource_type="address", action_name="Delete address", resource_name="address", config="address_id :"+post_data['account_id'], status="Success", region_id="Billing", project_id=request.session.get('account')['project_id'],project_name=request.session.get('account')['project_id'], user_id=request.session.get('account')['user_id'], user_name=request.session.get('account')['username'])
            return HttpResponse('received account delete request')
        elif 'update' in post_data:
            dict_acquire={'name': post_data['name'],
                          'post_code':post_data['zip'],
                          "address":post_data['addr'],
                          'status':'using',
                          'phone':post_data["phone"],
                          'mobile':post_data["mobile"],
                          'address_id': int(post_data['address_id'])}
            data_json=json.dumps({"address":dict_acquire})
            result=req("/address/update/%s" % account_id, method='PUT', data=data_json)
            Logger(request).create(resource_type="address", action_name="Update address", resource_name="address", config="address_id :"+post_data['address_id']+"; address:"+post_data['addr'], status="Success", region_id="Billing", project_id=request.session.get('account')['project_id'],project_name=request.session.get('account')['project_id'], user_id=request.session.get('account')['user_id'], user_name=request.session.get('account')['username'])
            return HttpResponse('success')
        else:
            dict_acquire={'name': post_data['name'],
                          'post_code':post_data['zip'],
                          "address":post_data['addr'],
                          'status':'using',
                          'phone':post_data["phone"],
                          'mobile':post_data["mobile"]}
            data_json=json.dumps({"address":dict_acquire})
            result=req("/address/create/%s" % account_id, method='POST', data=data_json)
            Logger(request).create(resource_type="address", action_name="Create address", resource_name="address", config="address:"+post_data['addr']+";name:"+post_data['name'], status="Success", region_id="Billing", project_id=request.session.get('account')['project_id'], project_name=request.session.get('account')['project_id'],user_id=request.session.get('account')['user_id'], user_name=request.session.get('account')['username'])
            return HttpResponse('success')

    def get_data(self):
        account_id=self.request.session.get('account')['account_id']
        result=req("address/list/%s" % account_id)
        result1=result['addresses']
        length_limit=24
        #将其中的'-'号抽取出来
        for m in result1:
            addr_fraglist = m['address'].split('|')
            m['address']=''.join(addr_fraglist)
        for i in result1:
            if len(i['address'])>length_limit:
                k=i['address'][0:length_limit]+'...'
                i['address_1']=k
                i['display1']='none'
                i['display2']='inline'
            else:
                i['display1']='inline'
                i['display2']='none'
        return {'result1': result1}


class Sub_InvoiceApplyView(HomePageView):
    """
    动作：向数据库中添加用户新填的
    """
    template_name = "invoicemanage/address_ajax.html"

    def get(self, request, *args, **kwargs):
        return super(Sub_InvoiceApplyView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        account_id=request.session.get('account')['account_id']
        post_data=request.POST

        dict_acquire={'address_id': post_data['address_id'],
                      'type': post_data['type'],
                      'title': post_data['title'],
                      'amount': post_data['amount'],
                      'prove':post_data['prove'],
                      'status': 'apply'}
        data_json=json.dumps({'invoice':dict_acquire})
        result=req('/invoice/create/%s' % account_id, method='POST', data=data_json)
        Logger(request).create(resource_type="invoice", action_name="Create invoice", resource_name="invoice", config="type:"+post_data['type']+";title :"+post_data['title']+"; amount:"+post_data['amount'], status="Success", region_id="Billing", project_id=request.session.get('account')['project_id'],project_name=request.session.get('account')['project_id'], user_id=request.session.get('account')['user_id'], user_name=request.session.get('account')['username'])
        return HttpResponse(result)

    def get_data(self):
        pass
