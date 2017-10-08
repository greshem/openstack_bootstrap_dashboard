# -*- coding:utf-8 -*-
'''
Created on 2016年7月1日

@author: greshem
'''
import urllib2
import urllib
from django.conf import settings
import json
class RequestClient(object):
    def __init__(self, request=None, base_url=None):
        self.base_url = base_url if base_url else settings.BILLING_BASE_URL
        self.request = request
#        self.base_url='http://192.168.100.136:8080/sdn_center/openstack/allstats'

    def api_request(self, url, method='GET', headers={}, data=None, isJson=True):
        if isJson:
            headers['Content-Type'] = 'application/json'
        else:
            data = urllib.urlencode(data)
        req = urllib2.Request(self.base_url+url, headers=headers)
        if method in ['PUT', 'DELETE']:
            req.get_method = lambda: method
        response = urllib2.urlopen(req, data)
        return response

def request(url,method='GET', headers={}, data=None, isJson=True):
    requestClient=RequestClient()
    return json.loads(requestClient.api_request(url, method, headers, data, isJson).read())

#print request('?tenant_id=6cfb740b182c41f69c2c3e5bceaf3a3b')