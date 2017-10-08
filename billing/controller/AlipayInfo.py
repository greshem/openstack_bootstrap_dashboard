# -*- coding:utf-8 -*-
'''
Created on 2015年9月10日

@author: greshem
'''
from billing.api import wsgi
from billing.hander import AlipayInfo

import json 

class Controller(wsgi.Controller):
    
    def rechargeAmount(self,req, **args):
        '''充值金额'''
        return AlipayInfo.rechargeAmount(json.dumps(req.json_body))
        

def create_resource():
    return wsgi.Resource(Controller())