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
from django.conf import settings
def index(request):
    result=req("account/list")
    return HttpResponse(json.dumps(result))

class IndexView(classview.TemplateView):
    template_name = "base.html"
    def get(self, request, *args, **kwargs):
        return super(IndexView,self).get(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        pass

class  BillDetailsView(BillReqMixin,classview.TemplateView):
    '''
    账户详情
    '''
    template_name= "billdetails/details_ajax.html"
    def get(self, request, *args, **kwargs):
        return super(BillDetailsView,self).get(request, *args, **kwargs)

    def get_data(self):
        account_id=self.request.session.get("account")["account_id"]
        # account_id="3fcf0bba-1c52-4dc8-9b59-2f78b3691943"
        account_info={}


        for key,value in billing_req("/account/detail/"+account_id)["account"].items():
            if key =="cash_balance" or key=="credit_line" or key=="gift_balance":
                account_info[key]=string.atof(value)
        account_info["available"]=account_info["credit_line"] if account_info["cash_balance"]>0 else account_info["cash_balance"]+account_info["credit_line"]
        account_info["account_id"]=account_id
        title_list=[{"name":"账户详情","url":"/center/bill_details"}]
        parentUser=billing_req('/account/getparentuserbyid/'+self.request.session.get("account")["user_id"])['parentUser']
        isSubAccount=False
        if parentUser and parentUser['name'] not in('admin','register'):
            isSubAccount=True
        return {"account_info":account_info,'amount':account_info['cash_balance']+account_info['gift_balance'],"title_list":title_list,'isSubAccount':isSubAccount}


def pay_redirect(request):
    '''
    支付请求
    :param request:
    :return:
    '''
    from hashlib import md5
    from billing_center import settings
    try:
        from urllib import urlencode
    except ImportError:
        from urllib.parse import urlencode
    MD5_KEY=settings.MD5_KEY

    def _generate_md5_sign(params):
        #md5加密生成签名
        src = '&'.join(['%s=%s' % (key, value) for key,value in sorted(params.items())]) + MD5_KEY
        return md5(src.encode('utf-8')).hexdigest()

    def _generate_payment_url(params_signed):
        return '%s?%s' % (settings.PAYMENT_URL, urlencode(params_signed))

    account_id=request.GET.get("account_id")
    agented_id=request.GET.get("agented_id")
    #account_id="5689sfshfhsdhiojfdsjofi"

    if agented_id:
        params={"account":account_id,"agented":agented_id}
    else:
        params={"account":account_id}

    sign=_generate_md5_sign(params)
    params.update({"sign":sign})
    payment_url=_generate_payment_url(params)
    return HttpResponseRedirect(payment_url)

class  RecentCostView(BillReqMixin,classview.TemplateView):
    '''
    近期消费记录
    '''

    template_name= "recentcost/recentcost_ajax.html"
    def get(self, request, *args, **kwargs):
        return super(RecentCostView,self).get(request, *args, **kwargs)
    def get_data(self):
        resource_type_list=(
            ('instance','实例'),
            ('ip','浮动IP'),
            ('router','路由'),
            ('disk','云硬盘'),
            ('bandwidth','带宽'),
            ('snapshot','快照'),
            ('vpn','VPN'),
        )
        account_id=self.request.session.get("account")["account_id"]
        #account_id="5689sfshfhsdhiojfdsjofi"
        title_list=[{"name":"近期消费记录","url":"/center/recent_cost"}]
        return_info=billing_req("/consumption/getamountsummary/"+account_id)["amountsummary"]
        return_info["title_list"]=title_list
        return_info["region_list"]=billing_req("/common/getregionlist")["regionList"]
        return_info["resource_type_list"]=resource_type_list
        return return_info

def consumption_data(request):
    account_id=request.session.get("account")["account_id"]
    #account_id="5689sfshfhsdhiojfdsjofi"
    pageSize=int(request.GET['limit'])
    pageNo=int((float(request.GET['offset'])+1)/float(request.GET['limit'])+1)
    product_type=request.GET['product_type']
    region=request.GET['region']
    period=request.GET['period']
    import datetime
    import calendar as cal
    current_year=datetime.date.today().year
    current_month=datetime.date.today().month
    current_range=("%s-%s-01"%(current_year,current_month),"%s-%s-01"%(month_add(current_year,current_month,1)))
    last_range=("%s-%s-01"%(month_add(current_year,current_month,-1)),"%s-%s-01"%(current_year,current_month))
    forelast_range=("%s-%s-01"%(month_add(current_year,current_month,-2)),"%s-%s-01"%(month_add(current_year,current_month,-1)))

    if period=="current":
        started_at,ended_at=current_range
    elif period=="last":
        started_at,ended_at=last_range
    else: #period=="forelast":
        started_at,ended_at=forelast_range
    request_url="/consumption/list/%s?pageNo=%s&pageSize=%s&started_at=%s&ended_at=%s"%(account_id,pageNo,pageSize,started_at,ended_at)
    if product_type!="all":
        request_url+="&resource_type=%s"%product_type
    if region!="all":
        request_url+="&region_id=%s"%region
    result = billing_req(request_url)['consumptionList']
    #result = billing_req("/consumption/list/%s"%account_id,data={"pageNo":pageNo,"pageSize":pageSize})
    return_data={}
    return_data["rows"]=result.pop('consumptions')
    #return_data["rows"]=filter(lambda x:if_true(product_type,region,period,x),result.pop('consumptions'))
    return_data["total"]=result.pop('total')
    return HttpResponse(json.dumps(return_data))

def data_def_map(request):
    '''
    数据展示用于定义格式
    :param request:
    :return:
    '''
    return_info={}
    resource_type_list=(
        ('instance','实例'),
        ('ip','浮动IP'),
        ('router','路由'),
        ('disk','云硬盘'),
        ('bandwidth','带宽'),
        ('snapshotdisk','快照'),
        ('vpn','VPN'),
    )
    return_info["region_list"]={item["region_id"]:item["region_desc"] for item in billing_req("/common/getregionlist")["regionList"]}
    return_info["resource_type_list"]=resource_type_list
    return HttpResponse(json.dumps(return_info))

def cost_forecast(request):
    account_id=request.session.get("account")["account_id"]
    #account_id="5689sfshfhsdhiojfdsjofi"
    return_list=billing_req("/consumption/forecast/"+account_id)["forecast"]
    return HttpResponse(json.dumps(return_list))

def child_account(request):
    account_id=request.session.get("account")["account_id"]
    #account_id="asdasdadasfftgerr"
    pageSize = int(request.GET['limit'])
    pageNo = int(request.GET['offset'])/pageSize + 1
    url="/account/subaccountlist/%s?pageNo=%s&pageSize=%s"%(account_id,pageNo,pageSize)
    if request.GET.has_key('name'):
        url+='&name='+request.GET['name']
    if request.GET.has_key('type'):
        url+='&type='+request.GET['type']
    if request.GET.has_key('max_cash'):
        url+='&max_cash='+request.GET['max_cash']
    if request.GET.has_key('min_cash'):
        url+='&min_cash='+request.GET['min_cash']
    if request.GET.has_key('max_gift'):
        url+='&max_gift='+request.GET['max_gift']
    if request.GET.has_key('min_gift'):
        url+='&min_gift='+request.GET['min_gift']
    if request.GET.has_key('max_credit'):
        url+='&max_credit='+request.GET['max_credit']
    if request.GET.has_key('min_credit'):
        url+='&min_credit='+request.GET['min_credit']
    result=billing_req(url)
    data = {'total':result['subAccountList']['total'], 'rows':result['subAccountList']['accounts']}
    return HttpResponse(json.dumps(data))

def getDiscountList(request):
    account_id=request.GET['account_id']
    data=[]
    regions=req('/common/getregionlist')['regionList']
    for region in regions:
        discount={"region_id":region['region_id'],"region_desc":region["region_desc"]}
        for billing_type in const().billing_item:
            billing_type=billing_type.split('_')[0]
            discount[billing_type+'_discount']=1
        discountItems=req('/discount/list/%s?region_id=%s'%(account_id,region['region_id']))['discountList']
        for discountItem in discountItems:
            discount[discountItem['billing_item']['billing_item'].split('_')[0]+"_discount"]=discountItem['discount_ratio']
        discountItems=req('/discount/list/%s?region_id=%s'%(account_id,'RegionCdn'))['discountList']
        for discountItem in discountItems:
            discount[discountItem['billing_item']['billing_item'].split('_')[0]+"_discount"]=discountItem['discount_ratio']
        data.append(discount)
    return HttpResponse(json.dumps(data))

def getDiscountByRegionId(request):
    account_id=request.GET['account_id']
    region_id=request.GET['region_id']
    discount={"region_id":region_id}
    for billing_type in const().billing_item:
        billing_type=billing_type.split('_')[0]
        discount[billing_type+'_discount']=1
    discountItems=req('/discount/list/%s?region_id=%s'%(account_id,region_id))['discountList']
    for discountItem in discountItems:
        discount[discountItem['billing_item']['billing_item'].split('_')[0]+"_discount"]=discountItem['discount_ratio']
    discountItems=req('/discount/list/%s?region_id=%s'%(account_id,'RegionCdn'))['discountList']
    for discountItem in discountItems:
        discount[discountItem['billing_item']['billing_item'].split('_')[0]+"_discount"]=discountItem['discount_ratio']
    return HttpResponse(json.dumps(discount))


def get_billing_item(billing_items,type_billing):
    if billing_items:
        for billing_item in billing_items:
            if type_billing==billing_item['billing_item']:
                return billing_item
    return None

def get_discount(region_discounts,type_billing):
    if region_discounts:
        for region_discount in region_discounts:
            if type_billing==region_discount['billing_item']['billing_item']:
                return region_discount
    return None

def editDiscountByRegionId(request):
    try:
        post_data_req=request.POST
        post_data=post_data_req.copy()
        account_id=post_data.pop('account_id')[0]
        region_id=post_data.pop('region_id')[0]
        cdnflow_discount=post_data.pop('cdn_discount')[0]
        cdnbandwidth_discount=cdnflow_discount
        
        
        cdn_billing_items=req('/billingItem/list?region_id=RegionCdn')['billing_itemList']
        billing_items=req('/billingItem/list?region_id=%s'%region_id)['billing_itemList']
        cdn_region_discounts=req('/discount/list/%s?region_id=%s'%(account_id,'RegionCdn'))['discountList']
        region_discounts=req('/discount/list/%s?region_id=%s'%(account_id,region_id))['discountList']
        
        
        '''cdnflow 折扣'''
#        cdnflow=req('/discount/detail/%s?region_id=%s&billing_item=%s'%(account_id,'RegionCdn','cdnflow_1_G'))
        cdnflow=get_discount(cdn_region_discounts,'cdnflow_1_G')
        if cdnflow:
            data_req={'discount_id':cdnflow['discount_id'],'discount_ratio':cdnflow_discount}
            req('/discount/update/%s'%account_id,method="PUT",data=json.dumps({'discount':data_req}))
        else:
            billing_item=get_billing_item(cdn_billing_items,'cdnflow_1_G')
            data_req={'billing_item_id':billing_item['billing_item_id'],'discount_ratio':cdnflow_discount}
            req('/discount/create/%s'%account_id,method="POST",data=json.dumps({'discount':data_req}))

        '''cdnbandwidth 折扣'''
        cdnbandwidth=get_discount(cdn_region_discounts,'cdnbandwidth_1_M')
        if cdnbandwidth:
            data_req={'discount_id':cdnbandwidth['discount_id'],'discount_ratio':cdnbandwidth_discount}
            req('/discount/update/%s'%account_id,method="PUT",data=json.dumps({'discount':data_req}))
        else:
            billing_item=get_billing_item(cdn_billing_items,'cdnbandwidth_1_M')
            data_req={'billing_item_id':billing_item['billing_item_id'],'discount_ratio':cdnbandwidth_discount}
            req('/discount/create/%s'%account_id,method="POST",data=json.dumps({'discount':data_req}))

        for billing_item in const().billing_item:
            if post_data.has_key(billing_item.split('_')[0]+'_discount'):
                discount_ratio=post_data[billing_item.split('_')[0]+'_discount']
                discount_req=get_discount(region_discounts, billing_item)
                if discount_req:
                    data_req={'discount_id':discount_req['discount_id'],'discount_ratio':discount_ratio}
                    req('/discount/update/%s'%account_id,method="PUT",data=json.dumps({'discount':data_req}))
                else:
                    billing_item_req=get_billing_item(billing_items,billing_item)
                    data_req={'billing_item_id':billing_item_req['billing_item_id'],'discount_ratio':discount_ratio}
                    req('/discount/create/%s'%account_id,method="POST",data=json.dumps({'discount':data_req}))
        Logger(request).create(resource_type="discount", action_name="Update discount", resource_name="discount", config=outJson(post_data_req), status="Success", region_id="Billing", project_id=request.session.get('account')['project_id'],project_name=request.session.get('account')['project_id'], user_id=request.session.get('account')['user_id'], user_name=request.session.get('account')['username'])
        return HttpResponse(json.dumps({'success':'success'}))
    except Exception :
        return HttpResponse(json.dumps({'success':'error','msg':'服务器报错'}))


class  ChildAccountView(BillReqMixin,HomePageView):
    '''
    子帐号账户管理
    '''
    template_name= "childaccount/childaccount_ajax.html"
    def get(self, request, *args, **kwargs):
        return super(ChildAccountView,self).get(request, *args, **kwargs)

    def get_data(self):
        account_id=self.request.session.get("account")["account_id"]
        #account_id="asdasdadasfftgerr"
        return_info={}
        temp=billing_req("/account/getsubaccountsum/"+account_id)["subAccountSum"]
        return_info["credit_child_num"]=temp["credit_sum"]
        return_info["general_child_num"]=temp["sum"]-temp["credit_sum"]
        return_info["account_info"]=billing_req("/account/detail/"+account_id)["account"]
        title_list=[{"name":"子帐号账户管理","url":"/center/account_manage"}]
        return_info["title_list"]=title_list
        return_info["gift_value"]=settings.GIFT_VALUE
        return return_info

class SubAccountDetailView(HomePageView):
    '''子账户详情界面'''
    template_name= "childaccount/childaccount_detail_ajax.html"
    def get_data(self):
        request=self.request
        account_id=request.GET["account_id"]
        account=req('/account/subaccountdetail/%s'%account_id)['subAccountDetail']
        data={"childaccount":account,"account_id":account_id}
        title_list=[{"name":"子账号管理","url":"/center/account_manage"},{"name":account['name']}]
        data["title_list"]=title_list
        return data

class DiscountFormView(HomePageView):
    template_name="childaccount/discount_form.html"
    def get_data(self):
        return {}

# Add by arsene -2015-10-13
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
        result=req("invoice/list/2e7d7572a02e4a13852d675973c3e8bf")
        result1 = HttpResponse(json.dumps(result))
        invoices_list=result[u'invoiceList']['invoices']

        return {'invoices': invoices_list}
# Add end

# Add by arsene -2015-12-02
def collect_instead_recharge_log(request):
    get_para=request.GET
    api_query_para=''
    account_id=request.session.get('account')['account_id']

    print account_id

    #获取query 参数
    for k in get_para:
        if k=='amount_to_search':
            if get_para[k]=='all':
                continue
            else:
                tem=get_para[k].split('-')
                api_query_para+='&min_amount=%s' % tem[0].rstrip('+')
                if len(tem)==2:
                    api_query_para+='&max_amount=%s' % tem[1]
        elif k=='order':
            continue
        else:
            if get_para[k] :
                if k=='started_at' or k=='ended_at':
                    api_query_para += '&%s=%s' % (k, get_para[k][0:10])
                else:
                    api_query_para += '&%s=%s' % (k, get_para[k])
    api_query_para=api_query_para.lstrip('&')

    result=req('recharge/getinsteadrechargelist/%s?%s' % (account_id, api_query_para))
    data = {'rows': result['insteadRechargeList'], 'total': result['count']}
    return HttpResponse(json.dumps(data))

def instead_recharge_view(request):
    account_id=request.session.get('account')['account_id']
    totalamount=req('recharge/getinsteadamount/%s' % account_id)['totalamount']
    return render(request, 'insteadrecharge/insteadrecharge.html', {'totalamount':totalamount})



