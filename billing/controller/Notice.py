# -*- coding:utf-8 -*-
'''
Created on 2015-12-10

@author: yamin_xu@163.com,xuym
'''
from billing.api import wsgi
import json
from oslo_config import cfg
CONF = cfg.CONF
from billing.db.dao.accountDao import AccountDao
from billing.emailsms.email_hand.email_handle import EmailHandle
from billing.emailsms.customer_communication import info_center
from billing.db.sqlalchemy import session as sa
from billing.db.object.models import *
import datetime
from billing.constant.sql import SQL
from billing.emailsms.customer_communication import info_center
import threading

class Controller(info_center,wsgi.Controller):
    '''
    信息中心,单session
    '''
    def req_paySuccess(self,req, **args):
        order_no=args.get('orderNo')
        info = json.loads(req.json_body)
        self.paySuccess(order_no,info)
        return json.dumps({"success":"success"})

    def req_lowcashReminder_3(self,req, **args):
#        account_id=args.get('account_id')
        self.lowcashReminder_3()
        return json.dumps({"success":"success"})

    def req_freezen(self,req, **args):
        account_id=args.get('account_id')
        self.freezen(account_id)
        return json.dumps({"success":"success"})

    def req_unfreezen(self,req, **args):
        account_id=args.get('account_id')
        self.unfreezen(account_id)
        return json.dumps({"success":"success"})

    def req_credit_adjust(self,req, **args):
        account_id=args.get('account_id')
        self.credit_adjust(account_id)
        return json.dumps({"success":"success"})

    def req_update_credit(self,req, **args):
        account_id=args.get('account_id')
        self.update_credit(account_id)
        return json.dumps({"success":"success"})

    def req_del_resource_3(self,req, **args):
        account_id=args.get('account_id')
        freeze_days=req.params.get('freeze_days')
        self.del_resource_3(account_id)
        return json.dumps({"success":"success"})

    def req_del_resource(self,req, **args):
        account_id=args.get('account_id')
        self.del_resource(account_id)
        return json.dumps({"success":"success"})

#    def getAccountByUserMD5(self, req, **args):
#        user_md5=args.get('user_md5')
#        return Account.getAccountByUserMD5(user_md5)

def create_resource():
    return wsgi.Resource(Controller())
