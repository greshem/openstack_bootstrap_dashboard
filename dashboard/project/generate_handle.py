# -*- coding: utf-8 -*-
#######################################################################################
# 处理session过期
#######################################################################################
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.conf import settings
from dashboard.project.utils import getMD5
from dashboard.api.requestClient import request as req
from django.views.defaults import *


import datetime
#from  ipdb  import set_trace;
class Session_Check(object):
    def process_request(self, request):
        #set_trace();
        if request.path in ('/auth/login/','/auth/login', '/auth/logout/', '/auth/logout'):
            return None
        if request.is_ajax():
            return None

        if(hasattr(request,"user")):
            if  request.user.is_anonymous():
		return;
            assert(  request.user.id is not None);
        else:
            return None;
	    
        if request.session.get("account") is None:
            print "BILLING_info usre=%s"%request.user.id;
            request.session['account']=req('/account/getaccountbyuserid/'+request.user.id)['account']
            print "BILLING_info %s"% request.session['account'];
        else:
            print "BILLING_info account data as follow %s"% request.session.get("account");

        change_account=False
        if settings.DEV:
            account_id=request.GET.get('account_id')
            if account_id:
                #检查url传入的account_id与sign的有效性
                # sign=request.GET['sign']
                # md5_key=settings.MD5_KEY
                # if getMD5(account_id+md5_key) !=sign:
                #     return HttpResponseRedirect(settings.HORIZON_URL+"/auth/logout")
    
                #account_id有效，检查session中账户信息，不一致则进行更新
                #     print request.session.get("account")
                if request.session.get("account") is None or request.session.get("account").get("account_id")!=account_id:
                    request.session['account']=req('/account/detail/%s'%account_id)['account']
                    change_account=True
            else:
                account_id=request.session.get("account") and request.session.get("account").get("account_id")
        else:
            #如果url没有账户信息，则从session中获取
            #print '---------------'+str(request.session.get("account"))
            account_id=request.session.get("account") and request.session.get("account").get("account_id")

       
        #如果不存在账户信息,则跳转到登录页面
        if not account_id:
            print("ERROR: billing, account_id not exists , may be  django  auth   should append   account billing  patch ");
            print("FIX:   cp /root/CI/django_openstack_auth/openstack_auth/views_billing.py  /usr/lib/python2.7/site-packages/openstack_auth/views.py ");
            print("FIX2:   clear chrome cookies ");
            return HttpResponseRedirect("/auth/login/")
            #return HttpResponseRedirect(settings.HORIZON_URL+"/auth/logout")

        request.session["isProjectAdmin"]=False
        #检查isProjectAdmin，isAdmin信号
#        if request.session.get("isProjectAdmin")==None or change_account:
#            try:
#                request.session["isProjectAdmin"]=req("/common/checkprojectadmin/%s"%account_id)['isProjectAdmin']
#            except Exception as e:
#                return server_error(request)
#
#        if request.session.get("isAdmin")==None or change_account:
#            try:
#                request.session["isAdmin"]=req("/account/checkadmin/%s"%account_id)['isAdmin']
#            except Exception as e:
#                return server_error(request)

        return None
