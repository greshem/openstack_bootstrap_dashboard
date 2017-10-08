# -*- coding:utf-8 -*-
'''
Created on 2015年9月10日

@author: greshem
'''
from billing.api import wsgi
from billing.hander import CDN

import json 


class Controller(wsgi.Controller):
    
    def create(self, req, **args):
        tenant_id=args.get('tenant_id')
        return CDN.create(tenant_id, json.dumps(req.json_body))
    
    def getDomainList(self, req, **args):
        tenant_id = args.get('tenant_id')

        return CDN.getCDNDomainList(tenant_id)
    
    def updateDomainEnable(self, req, **args):
        domain_id = args.get('domain_id')
        body=req.json_body
        enable = body['enable']if body.has_key('enable') else None
        status=body['status'] if body.has_key('status') else None
        return CDN.updateCdnDomainEnable(domain_id, enable,status)
        

def create_resource():
    return wsgi.Resource(Controller())