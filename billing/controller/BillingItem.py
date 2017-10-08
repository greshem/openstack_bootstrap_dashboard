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
from billing.hander import BillingItem as bi
import json

class Controller(wsgi.Controller):
    """计费项管理"""
    def list(self, req, **args):
        region_id = req.params.get('region_id')
        return bi.list(region_id)
    
    def getBillingItem(self, req, **args):
        billing_item_id = req.params.get('billing_item_id')
        region_id = req.params.get('region_id')
        billing_item = req.params.get('billing_item')
        return bi.getBillingItem(billing_item_id, region_id, billing_item)
    
    def update(self,req,**args):
        billing_item_id = args.get('billing_item_id')
        jsonParams=req.json_body
        jsonParams['billing_item']['billing_item_id']=billing_item_id
        return bi.update(json.dumps(jsonParams))

    def get_price_for_nass(self, req):
        network_type = req.GET.get('network_type')
        bandwidth = float(req.GET.get('bandwidth'))
        distance = float(req.GET.get('distance'))
        return bi.get_price_for_nass(network_type, bandwidth, distance)


def create_resource():
    return wsgi.Resource(Controller())
