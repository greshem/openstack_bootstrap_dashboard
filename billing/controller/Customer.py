# -*- coding:utf-8 -*-
from billing.api import wsgi
import json
from billing.util.controllerUtil import *
from billing.hander.Customer import getcustomerList,getaccountInfo,accountinfoEdit, getcustomercount, updatebasicinfo, becomecredit, \
    assignsales, getcontactlist, addcontact, updatecontact, deletecontact,editdiscount, becomeprojectadmin, getminorinfo, getallsales, \
    getksuserinfo, getuserrole, getaccountidbyprojectid, getnaasdiscount, setnaasdiscount, getcustomerdetails


class Controller(wsgi.Controller):
    '''客户列表'''
    def getCustomerList(self,req,**args):
        condition=getDictFromReq(req)
        return getcustomerList(condition=condition)

    def getAccountInfo(self,req,**args):
        account_id = req.params.get('account_id')
        return getaccountInfo(account_id=account_id)

    def accountInfoEdit(self,req,**args):
        account_id=args.get('account_id')
        jsonParams=req.json_body
        return accountinfoEdit(account_id,jsonParams)

    def getCustomerCount(self, req,**args):
        condition=getDictFromReq(req)
        if condition.get('parent_id'):
            return getcustomercount(condition.get('parent_id'))
        return getcustomercount()

    def updateBasicInfo(self,req,**args):
        account_id=args.get('account_id')
        jsonParams=req.json_body
        return updatebasicinfo(account_id, jsonParams)

    def becomeCredit(self,req,**args):
        jsonParams=req.json_body
        return becomecredit(jsonParams)

    def becomeProjectAdmin(self,req, **arge):
        jsonParams=req.json_body
        return becomeprojectadmin(jsonParams)

    def assignSales(self,req,**args):
        jsonParams=req.json_body
        return assignsales(jsonParams)

    def getContactList(self,req,**args):
        account_id=args.get('account_id')
        return getcontactlist(account_id)

    def addContact(self,req,**args):
        account_id=args.get('account_id')
        jsonParams=req.json_body
        return addcontact(account_id,jsonParams)

    def updateContact(self,req,**args):
        contact_id=args.get('contact_id')
        jsonParams=req.json_body
        return updatecontact(contact_id,jsonParams)

    def deleteContact(self, req,**args):
        contact_id=args.get('contact_id')
        return deletecontact(contact_id)

    def editDiscount(self, req, **args):
        account_id=args.get('account_id')
        jsonParams=req.json_body
        return editdiscount(account_id, jsonParams)

    def getMinorInfo(self, req, **args):
        account_id=args.get('account_id')
        return getminorinfo(account_id)

    def getAllSales(self, req):
        return getallsales()

    def getksUserInfo(self, req, **args):
        account_id=args.get('account_id')
        return getksuserinfo(account_id)

    def getUserRole(self, req, **args):
        jsonParams=req.json_body
        return getuserrole(jsonParams)

    def getaccountidByprojectid(self, req, **args):
        jsonParams=req.json_body
        return getaccountidbyprojectid(jsonParams)

    def getNaasDiscount(self, req, **args):
        account_id = args.get('account_id')
        return getnaasdiscount(account_id)

    def updateNaasDiscount(self, req, **args):
        account_id = args.get('account_id')
        jsonParams=req.json_body
        return setnaasdiscount(account_id, jsonParams)

    def getdetails(self, req, **args):
        account_id = args.get('account_id')
        return getcustomerdetails(account_id)


def create_resource():
    return wsgi.Resource(Controller())