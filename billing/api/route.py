# -*- coding:utf-8 -*-
'''
Created on 2015-8-20

@author: kevin
'''

"""
WSGI middleware
"""

from oslo_config import cfg
from oslo_log import log as logging
import routes
import six
import stevedore
import webob.dec
import webob.exc

from billing.api import wsgi
from billing import wsgi as base_wsgi
from billing.i18n import _LC,_LE,_LI,_LW


CONF = cfg.CONF
LOG = logging.getLogger(__name__)

class APIMapper(routes.Mapper):
    def routematch(self, url=None, environ=None):
        if url == "":
            result = self._match("", environ)
            return result[0], result[1]
        return routes.Mapper.routematch(self, url, environ)

    def connect(self, *args, **kargs):
        # NOTE(vish): Default the format part of a route to only accept json
        #             and xml so it doesn't eat all characters after a '.'
        #             in the url.
        kargs.setdefault('requirements', {})
        if not kargs['requirements'].get('format'):
            kargs['requirements']['format'] = 'json|xml'
        return routes.Mapper.connect(self, *args, **kargs)


class ProjectMapper(APIMapper):
    def resource(self, member_name, collection_name, **kwargs):
        if 'parent_resource' not in kwargs:
            kwargs['path_prefix'] = '{project_id}/'
        else:
            parent_resource = kwargs['parent_resource']
            p_collection = parent_resource['collection_name']
            p_member = parent_resource['member_name']
            kwargs['path_prefix'] = '{project_id}/%s/:%s_id' % (p_collection,
                                                                p_member)
        routes.Mapper.resource(self, member_name,
                                     collection_name,
                                     **kwargs)

class BaseRouter(base_wsgi.Router):
    """Routes requests on the OpenStack API to the appropriate controller
    and method.
    """
    ExtensionManager = None  # override in subclasses

    @classmethod
    def factory(cls, global_config, **local_config):
        """Simple paste factory, :class:`nova.wsgi.Router` doesn't have one."""
        return cls()

    def __init__(self, ext_mgr=None, init_only=None):

        mapper = APIMapper()
        self.resources = {}
        self._setup_routes(mapper)
        super(BaseRouter, self).__init__(mapper)

    def _setup_routes(self, mapper):
        raise NotImplementedError()


class APIRouter(BaseRouter):
    """Routes requests on the OpenStack API to the appropriate controller
    and method.
    """
    def _setup_routes(self, mapper):
#        if init_only is None or 'versions' in init_only:
#            self.resources['versions'] = versions.create_resource()
#            mapper.connect("versions", "/",
#                        controller=self.resources['versions'],
#                        action='show',
#                        conditions={"method": ['GET']})
#
#        mapper.redirect("", "/")

#        if init_only is None or 'test' in init_only:
        from billing.controller import Common
        self.resources['common'] = Common.create_resource()
        mapper.connect("/common/getregionlist",
                    controller=self.resources['common'],
                    action="getRegionList",
                    conditions={"method": ['GET']})
        mapper.connect("/common/checkprojectadmin/{account_id}",
                    controller=self.resources['common'],
                    action="checkProjectAdmin",
                    conditions={"method": ['GET']})
        
        
        from billing.controller import Account
        self.resources['account'] = Account.create_resource()
        mapper.connect("/account/lowcashworkorder_payment",
                    controller=self.resources['account'],
                    action="lowCashWorkOrder_3",
                    conditions={"method": ['GET']})
        mapper.connect("/account/{action}",
                    controller=self.resources['account'],
                    action="{action}",
                    conditions={"method": ['GET','POST']})
        mapper.connect("/account/getaccountbyuserid/{user_id}",
                    controller=self.resources['account'],
                    action="getAccountByUserID",
                    conditions={"method": ['GET']})
        mapper.connect("/account/getparentuserbyid/{user_id}",
                    controller=self.resources['account'],
                    action="getParentUserById",
                    conditions={"method": ['GET']})
        mapper.connect("/account/getaccountbyprojectid/{tenant_id}",
                    controller=self.resources['account'],
                    action="getAccountByProjectId",
                    conditions={"method": ['GET']})
        mapper.connect("/account/getsubaccountsum/{account_id}",
                    controller=self.resources['account'],
                    action="getSubAccountSum",
                    conditions={"method": ['GET']})
        mapper.connect("/account/subaccountlist/{account_id}",
                    controller=self.resources['account'],
                    action="subAccountList",
                    conditions={"method": ['GET']})
        mapper.connect("/account/projectadminsubaccount/{account_id}",
                    controller=self.resources['account'],
                    action="getProAdmSubAccount",
                    conditions={"method": ['GET']})
        mapper.connect("/account/subaccountdetail/{account_id}",
                    controller=self.resources['account'],
                    action="subAccountDetail",
                    conditions={"method": ['GET']})
        
        mapper.connect("/account/subaccountamountsum/{account_id}",
                    controller=self.resources['account'],
                    action="subAccountAmountSum",
                    conditions={"method": ['GET']})
        mapper.connect("/account/subaccountconsumptionlist/{account_id}",
                    controller=self.resources['account'],
                    action="subAccountConsumptionList",
                    conditions={"method": ['GET']})
        
        
        mapper.connect("/account/changecreditline/{account_id}",
                    controller=self.resources['account'],
                    action="changeCreditLine",
                    conditions={"method": ['GET']})
        mapper.connect("/account/change2credit/{account_id}",
                    controller=self.resources['account'],
                    action="change2Credit",
                    conditions={"method": ['GET']})
        
        mapper.connect("/account/checkadmin/{account_id}",
                    controller=self.resources['account'],
                    action="checkAdmin",
                    conditions={"method": ['GET']})
        
#        mapper.connect("/account/getaccountbyusermd5/{user_md5}",
#                    controller=self.resources['account'],
#                    action="getAccountByUserMD5",
#                    conditions={"method": ['GET']})
        mapper.connect("/account/{action}/{account_id}",
                    controller=self.resources['account'],
                    action="{action}",
                    conditions={"method": ['GET','PUT','DELETE']})
        
        mapper.connect("/account/{action}/{account_id}",
                    controller=self.resources['account'],
                    action="{action}",
                    conditions={"method": ['GET','PUT','DELETE']})

        
        
        from billing.controller import Address
        self.resources['address'] = Address.create_resource()
        mapper.connect("/address/{action}/{account_id}",
                    controller=self.resources['address'],
                    action="{action}",
                    conditions={"method": ['GET','POST','PUT']})
        mapper.connect("/address/delete/{address_id}",
                    controller=self.resources['address'],
                    action="delete",
                    conditions={"method": ['DELETE']})
        
        from billing.controller import Bill
        self.resources['bill'] = Bill.create_resource()
        mapper.connect("/bill/list/{account_id}",
                    controller=self.resources['bill'],
                    action="list",
                    conditions={"method": ['GET']})
        mapper.connect("/bill/detail/{bill_id}",
                    controller=self.resources['bill'],
                    action="detail",
                    conditions={"method": ['GET']})
        mapper.connect("/bill/billitemlist/{bill_id}",
                    controller=self.resources['bill'],
                    action="billitemlist",
                    conditions={"method": ['GET']})
        
        
        from billing.controller import Consumption
        self.resources['consumption'] = Consumption.create_resource()
        mapper.connect("/consumption/list/{account_id}",
                    controller=self.resources['consumption'],
                    action="list",
                    conditions={"method": ['GET']})
        mapper.connect("/consumption/forecast/{account_id}",
                    controller=self.resources['consumption'],
                    action="forecast",
                    conditions={"method": ['GET']})
        mapper.connect("/consumption/getamountsummary/{account_id}",
                    controller=self.resources['consumption'],
                    action="getAmountSummary",
                    conditions={"method": ['GET']})
        mapper.connect("/consumption/getconsumptionsummary/{account_id}",
                    controller=self.resources['consumption'],
                    action="getConsumptionSummary",
                    conditions={"method": ['GET']})
        
        
        from billing.controller import BillingItem
        self.resources['billingItem']=BillingItem.create_resource()
        mapper.connect("/billingItem/{action}",
                    controller=self.resources['billingItem'],
                    action="{action}",
                    conditions={"method": ['GET']})
        mapper.connect("/billingItem/update/{billing_item_id}",
                    controller=self.resources['billingItem'],
                    action="update",
                    conditions={"method": ['PUT']})
        
        from billing.controller import Discount
        self.resources['discount']=Discount.create_resource()
        mapper.connect("/discount/{action}/{account_id}",
                    controller=self.resources['discount'],
                    action="{action}",
                    conditions={"method": ['GET','PUT','POST','DELETE']})
        
        from billing.controller import Invoice
        self.resources['invoice']=Invoice.create_resource()
        mapper.connect("/invoice/detail/{invoice_id}",
                    controller=self.resources['invoice'],
                    action="detail",
                    conditions={"method": ['GET']})
        mapper.connect("/invoice/{action}/{account_id}",
                    controller=self.resources['invoice'],
                    action="{action}",
                    conditions={"method": ['GET','PUT','POST']})
        
        from billing.controller import AlipayInfo
        self.resources['alipayInfo']=AlipayInfo.create_resource()
        mapper.connect("/alipayinfo/rechargeamount",
                    controller=self.resources['alipayInfo'],
                    action="rechargeAmount",
                    conditions={"method": ['POST']})
        
        from billing.controller import Gift
        self.resources['gift']=Gift.create_resource()
        mapper.connect("/gift/giftamount/{account_id}",
                    controller=self.resources['gift'],
                    action="giftAmount",
                    conditions={"method": ['POST']})
        mapper.connect("/gift/firstamount/{account_id}",
                    controller=self.resources['gift'],
                    action="firstamount",
                    conditions={"method": ['POST']})
        from billing.controller import Recharge
        self.resources["recharge"]=Recharge.create_resource()
        mapper.connect("/recharge/create/{account_id}",
                    controller=self.resources['recharge'],
                    action="create",
                    conditions={"method": ['POST']})
        mapper.connect("/recharge/getorderrechargelist/{account_id}",
                    controller=self.resources['recharge'],
                    action="getOrderRechargeList",
                    conditions={"method": ['GET']})
        mapper.connect("/recharge/insteadrecharge",
                    controller=self.resources['recharge'],
                    action="insteadRecharge",
                    conditions={"method": ['POST']})
        mapper.connect("/recharge/getinsteadrechargelist/{instead_recharge_account}",
                    controller=self.resources['recharge'],
                    action="getInsteadRecharge",
                    condition={"method":['GET']})
        mapper.connect("/recharge/getinsteadamount/{instead_recharge_account}",
                    controller=self.resources['recharge'],
                    action="getInsteadAmount",
                    condition={"method":['GET']})

        from billing.controller import Customer
        self.resources["customer"]=Customer.create_resource()
        mapper.connect("/customer/getcustomerlist",
                    controller=self.resources['customer'],
                    action="getCustomerList",
                    conditions={"method":['GET']})
        mapper.connect("/customer/getuserrole",
                    controller=self.resources['customer'],
                    action="getUserRole",
                    conditions={"method":['POST']})
        mapper.connect("/customer/getaccountinfo",
                    controller=self.resources['customer'],
                    action='getAccountInfo',
                    conditions={"method":['GET']})
        mapper.connect("/customer/accountinfoedit/{account_id}",
                    controller=self.resources['customer'],
                    action='accountInfoEdit',
                    conditions={"method":['PUT']})
        mapper.connect("/customer/getcustomercount",
                    controller=self.resources['customer'],
                    action='getCustomerCount')
        mapper.connect("/customer/basicinfoedit/{account_id}",
                    controller=self.resources['customer'],
                    action='updateBasicInfo',
                    conditions={"method":['POST']})
        mapper.connect("/customer/becomecredit",
                    controller=self.resources['customer'],
                    action='becomeCredit',
                    conditions={'method':['POST']})
        mapper.connect("/customer/becomeprojectadmin",
                    controller=self.resources['customer'],
                    action='becomeProjectAdmin',
                    conditions={'method': ['POST']})
        mapper.connect("/customer/assignsales",
                    controller=self.resources['customer'],
                    action='assignSales',
                    conditions={"method":['POST']})
        mapper.connect("/customer/getcontactlist/{account_id}",
                    controller=self.resources['customer'],
                    action='getContactList',
                    conditions={'method':['GET']})
        mapper.connect("/customer/addcontact/{account_id}",
                    controller=self.resources['customer'],
                    action='addContact',
                    conditions={'method':['POST']})
        mapper.connect("/customer/updatecontact/{contact_id}",
                    controller=self.resources['customer'],
                    action='updateContact',
                    conditions={'method':['POST']})
        mapper.connect("/customer/deletecontact/{contact_id}",
                    controller=self.resources['customer'],
                    action='deleteContact',
                    conditions={'method': ['POST']})
        mapper.connect('/customer/editdiscount/{account_id}',
                    controller=self.resources['customer'],
                    action='editDiscount',
                    conditions={'method':['POST']})
        mapper.connect('/customer/getnaasdiscount/{account_id}',
                    controller=self.resources['customer'],
                    action='getNaasDiscount',
                    condition={'method':['GET']})
        mapper.connect('/customer/updatenaasdiscount/{account_id}',
                    controller=self.resources['customer'],
                    action='updateNaasDiscount',
                    conditions={'method':['POST']})
        mapper.connect('/customer/getminorinfo/{account_id}',
                    controller=self.resources['customer'],
                    action='getMinorInfo',
                    conditions={'method':['GET']})
        mapper.connect('/customer/getallsales',
                    controller=self.resources['customer'],
                    action='getAllSales',
                    conditions={'method':['GET']})
        mapper.connect('/customer/getksuserinfo/{account_id}',
                    controller=self.resources['customer'],
                    action='getksUserInfo',
                    conditions={'method':['GET']})
        mapper.connect('/customer/getaccountidbyprojectid',
                    controller=self.resources['customer'],
                    action = 'getaccountidByprojectid',
                    conditions={'method':['POST']})
        mapper.connect('/customer/details/{account_id}',
                    controller = self.resources['customer'],
                    action = 'getdetails',
                    condition={'method':['GET']})


        from billing.controller import Fianace
        self.resources["finance"]=Fianace.create_resource()
        mapper.connect("/finance/getinvoicelist",
                       controller=self.resources['finance'],
                       action="getInvoiceList",
                       conditons={"method":['GET']})
        mapper.connect("/finance/getinvoicedetail/{invoice_id}",
                       controller=self.resources['finance'],
                       action='getInvoiceDetail',
                       conditions={"method":['GET']})
        mapper.connect("/finance/getinvoicehandleidetail/{invoice_id}",
                       controller=self.resources['finance'],
                       action='getInvoiceHandleDetail',
                       conditions={"method":['GET']})
        mapper.connect("/finance/untreatedinvoicehandle",
                       controller=self.resources['finance'],
                       action="untreatedInvoiceHandle",
                       condition={"method":['PUT']})
        mapper.connect("/finance/getbilllist",
                       controller=self.resources['finance'],
                       action="getBillList",
                       condition={"method":['GET']})
        mapper.connect("/finance/getbilldetailinfo/{bill_id}",
                       controller=self.resources['finance'],
                       action="getBillDetailInfo",
                       condition={"method":['GET']})
        mapper.connect("/finance/getrechargelist",
                       controller=self.resources['finance'],
                       action="getRechargeList",
                       condition={"method":['GET']}),
        mapper.connect("/finance/getrechargedetail/{order_no}",
                       controller=self.resources['finance'],
                       action="getRechargeDetail",
                       condition={"method":['GET']}),
        mapper.connect("/finance/getrechargeamount/",
                       controller=self.resources['finance'],
                       action="getRechargeAmount",
                       condition={"method":['GET']})
        #CDN
        from billing.controller import CDN
        self.resources["cdn"]=CDN.create_resource()

        mapper.connect("/cdn/domainList/{tenant_id}",
                    controller=self.resources['cdn'],
                    action="getDomainList",
                    conditions={"method": ['GET']})
        mapper.connect("/cdn/updatedomainenable/{domain_id}",
                    controller=self.resources['cdn'],
                    action="updateDomainEnable",
                    conditions={"method": ['PUT']})

        #短信与邮件
        from billing.controller import Notice
        self.resources["notice"]=Notice.create_resource()
        mapper.connect("/notice/freezen3",
                    controller=self.resources['notice'],
                    action="req_lowcashReminder_3",
                    conditions={"method": ['GET']})

        mapper.connect("/notice/freezen/{account_id}",
                    controller=self.resources['notice'],
                    action="req_freezen",
                    conditions={"method": ['GET']})

        mapper.connect("/notice/delResource3/{account_id}",
                    controller=self.resources['notice'],
                    action="req_del_resource_3",
                    conditions={"method": ['GET']})

        mapper.connect("/notice/delResource/{account_id}",
                    controller=self.resources['notice'],
                    action="req_del_resource",
                    conditions={"method": ['GET']})
        #工单
        from billing.controller import WorkOrder
        self.resources["workorder"]=WorkOrder.create_resource()
        mapper.connect("/workorder/create/workorder",
                    controller=self.resources['workorder'],
                    action="create_workorder",
                    conditions={"method": ['POST']})

        mapper.connect("/workorder/create/type",
                    controller=self.resources['workorder'],
                    action="create_workorder_type",
                    conditions={"method": ['POST']})
        mapper.connect("/workorder/create/record",
                    controller=self.resources['workorder'],
                    action="create_workorder_record",
                    conditions={"method": ['POST']})
        mapper.connect("/workorder/update",
                    controller=self.resources['workorder'],
                    action="update_workorder",
                    conditions={"method": ['POST']})
        mapper.connect("/workorder/detail/{workorderno}",
                    controller=self.resources['workorder'],
                    action="workorder_detail",
                    conditions={"method": ['GET']})
        mapper.connect("/workorder/list/workorder",
                    controller=self.resources['workorder'],
                    action="workorder_list",
                    conditions={"method": ['GET']})
        mapper.connect("/workorder/list/record/{workorderno}",
                    controller=self.resources['workorder'],
                    action="workorder_record_list",
                    conditions={"method": ['GET']})
        mapper.connect("/workorder/list/type",
                    controller=self.resources['workorder'],
                    action="workorder_type_list",
                    conditions={"method": ['GET']})
        mapper.connect("/workorder/statics",
                    controller=self.resources['workorder'],
                    action="workorder_statics",
                    conditions={"method": ['GET']})

        from billing.controller import ActionLog
        self.resources["actionlog"]=ActionLog.create_resource()
        mapper.connect("/actionlog/list",
                    controller=self.resources['actionlog'],
                    action="actionlog_list",
                    conditions={"method": ['GET']})

        from billing.controller import Advert
        self.resources["advert"]=Advert.create_resource()
        mapper.connect("/advert/getadvertlist",
                    controller=self.resources['advert'],
                    action="getAdvertList",
                    contidions={"method":['POST']})
        mapper.connect("/advert/createadvert",
                    controller=self.resources['advert'],
                    action="advertAddHandle",
                    condition={"method":['POST']})
        mapper.connect("/advert/getadvertinfo/{advert_id}",
                    controller=self.resources['advert'],
                    action="getAdvertInfo",
                    contidion={"method":['GET']})
        mapper.connect("/advert/editadvert",
                    controller=self.resources['advert'],
                    action="advertUpdateHandle",
                    condition={"method":['POST']})
        mapper.connect("/advert/deleteadvert",
                    controller=self.resources['advert'],
                    action="advertDeleteHandle",
                    condition={"method":['POST']})
        mapper.connect("/advert/getvalidadvert",
                    controller=self.resources['advert'],
                    action="getValidAdvert",
                    condition={"method":['GET']})

        from billing.controller import BossUser
        self.resources["bossuser"]=BossUser.create_resource()
        mapper.connect("/bossuser/salesman",
                    controller=self.resources['bossuser'],
                    action="saler_list",
                    contidions={"method":['GET']})

# *** add by zhangaw
        from billing.controller import Rebate
        self.resources['rebate'] = Rebate.create_resource()
        mapper.connect("/rebate/getrebatebilllist",
                       controller = self.resources['rebate'],
                       action = 'getRebateBillList',
                       contidion={"method":['POST']})
        mapper.connect("/rebate/getrebatesubbilllist",
                       controller = self.resources['rebate'],
                       action = 'getRebateSubBillList',
                       contidion={"method":['POST']})
        mapper.connect("/rebate/getrebatebillitemlist",
                       controller = self.resources['rebate'],
                       action = 'getRebateBillItemList',
                       contidion={"method":['POST']})