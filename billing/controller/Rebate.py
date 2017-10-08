# -*- coding:utf-8 -*-
from oslo_utils import strutils
import webob
from billing.api import wsgi
from billing.hander import Account,Rebate
from billing.util.controllerUtil import *

import json
import datetime
from oslo_config import cfg
CONF = cfg.CONF
from billing.util.tzUtil import change2UTC

class Controller(wsgi.Controller):
    def getRebateBillList(self,req,**args):
        temp = req.json_body
        condition = temp['condition'] if (temp.has_key('condition') and temp['condition']) else None
        likecondition = temp['likecondition'] if (temp.has_key('likecondition') and temp['likecondition']) else None
        page_no=int(temp['page_no']) if (temp.has_key('page_no') and temp['page_no']) else 1
        page_size=int(temp['page_size']) if (temp.has_key('page_size') and temp['page_size']) else 10
        return Rebate.getrebatebillList(condition,likecondition,page_no,page_size)

    def getRebateBillItemList(self,req,**args):
        temp = req.json_body
        condition = temp['condition'] if (temp.has_key('condition') and temp['condition']) else None
        likecondition = temp['likecondition'] if (temp.has_key('likecondition') and temp['likecondition']) else None
        page_no=int(temp['page_no']) if (temp.has_key('page_no') and temp['page_no']) else 1
        page_size=int(temp['page_size']) if (temp.has_key('page_size') and temp['page_size']) else 10
        return Rebate.getrebatebillitemList(condition,likecondition,page_no,page_size)

    def getRebateSubBillList(self,req,**args):
        temp = req.json_body
        condition = temp['condition'] if (temp.has_key('condition') and temp['condition']) else None
        likecondition = temp['likecondition'] if (temp.has_key('likecondition') and temp['likecondition']) else None
        page_no=int(temp['page_no']) if (temp.has_key('page_no') and temp['page_no']) else 1
        page_size=int(temp['page_size']) if (temp.has_key('page_size') and temp['page_size']) else 10
        return Rebate.getrebatesubbillList(condition,likecondition,page_no,page_size)

def create_resource():
    return wsgi.Resource(Controller())