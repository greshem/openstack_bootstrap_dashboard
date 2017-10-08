# -*- coding:utf-8 -*-
from billing.api import wsgi
from billing.util.controllerUtil import *
from billing.hander.Finance import getinvoiceList,getinvoiceDetail,getrechargeList,getbillList,getbilldetailInfo,getrechargeDetail,getrechargeDetail2,invoiceHandle,getrechargeAmount
from billing.hander.Invoice import updateRecords
from billing.hander.Bill import getBillDetail
import json
class Controller(wsgi.Controller):
    def getInvoiceList(self,req,**args):
        '''发票管理列表获取'''
        condition=getDictFromReq(req)
        page_no=int(condition['page_no']) if (condition.has_key('page_no') and condition['page_no']) else 1
        page_size=int(condition['page_size']) if (condition.has_key('page_size') and condition['page_size']) else 10
        return getinvoiceList(page_no,page_size,condition)
    def getInvoiceDetail(self,req,**args):
        invoice_id=args.get('invoice_id')
        return getinvoiceDetail(invoice_id)
    def untreatedInvoiceHandle(self,req,**args):
        '''发票处理'''
        jsonParams=req.json_body
        return invoiceHandle(jsonParams)
    def getRechargeList(self,req,**args):
        condition=getDictFromReq(req)
        page_no=int(condition['page_no']) if (condition.has_key('page_no') and condition['page_no']) else 1
        page_size=int(condition['page_size']) if (condition.has_key('page_size') and condition['page_size']) else 50
        return getrechargeList(page_no,page_size,condition)
    def getRechargeDetail(self,req,**args):
        order_no=args.get('order_no')
        tempdict=getDictFromReq(req)
        return getrechargeDetail2(order_no,tempdict)
    def getRechargeAmount(self,req,**args):
        return getrechargeAmount()
    def getBillList(self,req,**args):
        condition=getDictFromReq(req)
        page_no=int(condition['page_no']) if (condition.has_key('page_no') and condition['page_no']) else 1
        page_size=int(condition['page_size']) if (condition.has_key('page_size') and condition['page_size']) else 10
        return getbillList(page_no,page_size,condition)
    def getBillDetailInfo(self,req,**args):
        bill_id=args.get('bill_id')
        return getbilldetailInfo(bill_id)


def create_resource():
    return wsgi.Resource(Controller())

