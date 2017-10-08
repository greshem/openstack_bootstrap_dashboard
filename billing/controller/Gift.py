# -*- coding:utf-8 -*-
'''
Created on 2015年9月10日

@author: greshem
'''
from billing.api import wsgi
from billing.hander import Gift

import json 

class Controller(wsgi.Controller):
    
    def giftAmount(self,req, **args):
        '''赠送金额'''
        account_id=args.get('account_id')
        return Gift.giftAmount(account_id,json.dumps(req.json_body))
    def firstamount(self,req,**args):
        '''
        第一次赠送，必须是原子性的数据库操作
        :param req:
        :param args:
        :return:
        '''
        account_id=args.get("account_id")
        return Gift.firstAmount(account_id,json.dumps(req.json_body))

def create_resource():
    return wsgi.Resource(Controller())