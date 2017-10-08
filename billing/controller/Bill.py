# -*- coding:utf-8 -*-
'''
Created on 2015-8-24

@author: greshem
'''
from oslo_utils import strutils
import webob

from billing.api import wsgi
from billing import exception
from billing.i18n import _
from billing import utils
from billing.hander import Bill
from billing.util.controllerUtil import *
from oslo_config import cfg
CONF = cfg.CONF
from billing.util.tzUtil import change2UTC

class Controller(wsgi.Controller):
    """账单管理"""
    def list(self, req, **args):
        page_no = req.params.get('pageNo')
        page_size = req.params.get('pageSize')
        page_no = int(page_no) if page_no else 1
        page_size = int(page_size) if page_size else 15
        account_id = args.get('account_id')
        started_at = req.params.get('started_at')
        started_at=change2UTC(started_at,timezone=CONF.timezone_local,format='%Y-%m-%d')
        ended_at = req.params.get('ended_at')
        ended_at=change2UTC(ended_at,timezone=CONF.timezone_local,format='%Y-%m-%d')
        bill_type = req.params.get('bill_type')
        return Bill.list(account_id, started_at, ended_at, page_no, page_size, bill_type=bill_type)
    def detail(self, req, **args):
        bill_id = args.get('bill_id')
        return Bill.getBillDetail(bill_id)
    
    def billitemlist(self,req, **args):
        bill_id = args.get('bill_id')
        return Bill.billItemList(bill_id)
        


def create_resource():
    return wsgi.Resource(Controller())
