"""billing_center URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns

from views import abc
from django.views.generic import TemplateView
import views1
from views1 import BillDetailsView,RecentCostView,ChildAccountView,SubAccountDetailView,data_def_map,pay_redirect
from views1 import BillDetailsView,RecentCostView,ChildAccountView,DiscountFormView
from view_invoice import InvoiceManageView, Sub_InvoiceAccountView, Sub_InvoiceApplyView
from views1 import BillDetailsView,RecentCostView,ChildAccountView
from billView import BillView,BillDetailView
from rechargeRecordView import RechargeRecordView
#from views1 import IndexView,BillDetailsView,RecentCostView,ChildAccountView
from dashboard.project import sunComsumptinViews,billView,rechargeRecordView
from views import indexView
from business import BusinessView,CreditLineFormView,changeCreditLine
from views import testView
urlpatterns = patterns('',
   url(r'^$',abc.as_view() ),
   url(r'^index$', indexView.as_view(),name="project_index"),
   url(r'^test$', testView.as_view(),name="test"),
   url(r'^bill_details/$', BillDetailsView.as_view(),name="bill_details"),
   url(r'^bill_details$', BillDetailsView.as_view(),name="bill_details"),
   url(r'^index$', TemplateView.as_view(template_name="base.html"),name="index"),
   url(r'^recent_cost$', RecentCostView.as_view(),name="recent_cost"),
   url(r'^datarequest', data_def_map,name="data_request"),
   url(r'^payment_redirect', pay_redirect,name="payment_redirect"),
   url(r'^account_manage$', ChildAccountView.as_view(),name="account_manage"),
   url(r'^account_manage/detail$', SubAccountDetailView.as_view(),name="account_manage"),
   url(r'^account_manage/discount/edit$', DiscountFormView.as_view(),name="account_manage"),
   url(r'^invoice_manange$', InvoiceManageView.as_view(),name="invoice_manage"),
   url(r'^invoice_getAccountAddr$', Sub_InvoiceAccountView.as_view(),  name='invoice_account_addr'),
   url(r'^invoice_do_apply$', Sub_InvoiceApplyView.as_view(), name='invoice_do_apply'),
   url(r'^invoice_NewAddrForm$', 'dashboard.project.view_invoice.get_new_address_form'),
   url(r'^invoice_queryAddrDetail$', 'dashboard.project.view_invoice.get_address_detail_by_addr_id'),
   url(r'^invoice_querySummary$', 'dashboard.project.view_invoice.get_invoice_summary'),
   url(r'^prepareInvoiceData$', 'dashboard.project.view_invoice.prepareInvoiceData'),
   url(r'^subComsumption$', sunComsumptinViews.Index.as_view()),
   url(r'^subComsumption/detail$', sunComsumptinViews.DetailView.as_view()),
   url(r'^subComsumption/consumptionhistory$', sunComsumptinViews.ConsumptionHistoryView.as_view()),
   url(r'^subComsumption/billdetail$', sunComsumptinViews.BillDetailView.as_view()),
   url(r'^subComsumptionList$', 'dashboard.project.sunComsumptinViews.getSubComsumptionList'),
   url(r'^getConsumptionSummary$', 'dashboard.project.sunComsumptinViews.getConsumptionSummary'),
   url(r'^billlist$', 'dashboard.project.sunComsumptinViews.getBillList'),
   url(r'^billdetailsum$', 'dashboard.project.sunComsumptinViews.getBillDetail'),
   url(r'^comsumptionlist$', views1.consumption_data),
   url(r'^forecast$',views1.cost_forecast,name='forecast'),
   url(r'^childaccountdata$',views1.child_account,name='childaccountlist'),
   url(r'^bill$',BillView.as_view(),name='bill'),
   url(r'^getbillList$','dashboard.project.billView.getbillList'),
   url(r'^rechargeRecord$',RechargeRecordView.as_view(),name='bill'),
   url(r'getrechargeRecordList$','dashboard.project.rechargeRecordView.getrechargeRecordList'),
   url(r'^bill/detail',BillDetailView.as_view()),
   url(r'^getbillDetail$','dashboard.project.billView.getbillDetail'),
   url(r'^common/regionlist$','dashboard.project.views.getRegions'),
   url(r'^getdiscountlist$','dashboard.project.views1.getDiscountList'),
   url(r'^getdiscountbyregionid$','dashboard.project.views1.getDiscountByRegionId'),
   url(r'^editdiscountbyregionid','dashboard.project.views1.editDiscountByRegionId'),
   url(r'^iebrowsers',TemplateView.as_view(template_name="browsers.html")),
   url(r'insteadrechargeview', 'dashboard.project.views1.instead_recharge_view'),
   url(r'prepareRechargeData','dashboard.project.views1.collect_instead_recharge_log'),
   url(r'insteadRecharge','dashboard.project.business.insteadRecharge'),
   url(r'giftRecharge/(?P<account_id>.+)$','dashboard.project.business.giftRecharge'),
   url(r'firstGift/(?P<account_id>.+)$','dashboard.project.business.firstGift'),
   url(r'^business_manage$', BusinessView.as_view(),name="business_manage"),
   url(r'^credit_line$', CreditLineFormView.as_view(),name="business_manage"),
   url(r'^changecreditline$', changeCreditLine,name="business_manage"),
   url(r'^instance/', include('dashboard.project.instance.urls')),
   url(r'^volume/', include('dashboard.project.volume.urls')),
   url(r'^image/', include('dashboard.project.image.urls')),
   url(r'^securitygroup/', include('dashboard.project.securitygroup.urls')),
   url(r'^floatingip/', include('dashboard.project.floatingip.urls')),
   url(r'^network/', include('dashboard.project.network.urls')),
   url(r'^router/', include('dashboard.project.router.urls')),
   url(r'^networktopology/', include('dashboard.project.networktopology.urls')),
   url(r'^tenant/', include('dashboard.project.tenant.urls')),
   url(r'^user/', include('dashboard.project.user.urls')),
)
