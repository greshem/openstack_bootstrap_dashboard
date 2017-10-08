# -*- coding:utf-8 -*-
'''
Created on 2015-8-27

@author: greshem
'''
from billing.db.dao.InvoiceDao import InvoiceDao
from billing.db.object.models import Invoice
from billing.util.handlerUtil import *
from billing.db.object.models import Bill
from billing.db.Pagination import Pagination
from oslo_log import log as logging
from billing.util.pagePackage import *
import traceback
LOG = logging.getLogger(__name__)

def listByPage(conditionJson, page_no=1, page_size=15, headers=None, **kwargs):
    try:
        conditionJson=json.loads(conditionJson)
        invoiceDao = InvoiceDao()
        result = invoiceDao.getInvoiceByPage(conditionJson, page_no, page_size)
        dataResult = []
        if result:
            for invoice in result:
                dataResult.append(getJsonFromObj(invoice))
        return outSuccess("invoiceList", pagePackage("invoices", dataResult, page_no=result.no, page_size=result.page_size, total=result.total))
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("取得发票列表失败！")


def add(invoiceJson,headers=None, **kwargs):
    try:
        if isinstance(invoiceJson,str):
            invoiceJson = json.loads(invoiceJson)
        invoiceDict = invoiceJson['invoice']
        invoice = Invoice()
        getObjFromJson(invoice, invoiceDict)
        invoiceDao = InvoiceDao(invoice)
        invoiceDao.add()
        return outSuccess("invoice", getJsonFromObj(invoiceDao.invoice))
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("申请发票失败！")

def update(invoiceJson,headers=None, **kwargs):
    try:
        if isinstance(invoiceJson,str):
            invoiceJson = json.loads(invoiceJson)
        invoiceDict = invoiceJson['invoice']
        invoice = Invoice()
        invoice.invoice_id=invoiceDict['invoice_id']
        invoiceDao = InvoiceDao(invoice)
        invoiceDao.update(invoiceDict)
        return outSuccess("invoice", getJsonFromObj(invoiceDao.invoice))
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("更新发票失败！")

def detail(invoice_id,headers=None, **kwargs):
    try:
        invoice = Invoice()
        invoice.invoice_id = invoice_id
        invoiceDao = InvoiceDao(invoice)
        invoiceDao.detail()
        return outSuccess("invoice", getJsonFromObj(invoiceDao.invoice))
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("取得发票详情失败！")

# arsene add
def summary(account_id, headers=None, **kwargs):
    try:
        invoiceDao = InvoiceDao()
        result = invoiceDao.getBillAmountSummary(account_id)
        return outSuccess('summary', result)
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("获取汇总失败！")
# end edit

# added by zhangaw
def updateRecords(invoiceJson,headers=None, **kwargs):
    try:
        if isinstance(invoiceJson,str):
            invoiceJson = json.loads(invoiceJson)
        for record in invoiceJson:
            invoiceDict = record['invoice']
            invoice = Invoice()
            invoice.invoice_id=invoiceDict['invoice_id']
            invoiceDao = InvoiceDao(invoice)
            invoiceDao.update(invoiceDict)
        return outSuccess("msg","更新发票成功" )
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("更新发票失败！")
# end edit

if __name__=="__main__":
    exitcontent={'invoice':{'invoice_id':30,'post_by':'圆通','express_no':'1234567','invoice_no':'0000000'}}
    print update(exitcontent)



