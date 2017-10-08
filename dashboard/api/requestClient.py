# -*- coding:utf-8 -*-
'''
Created on 2014-7-7

@author: greshem
'''
import urllib2
import urllib
from django.conf import settings
import json


class RequestClient():
    def __init__(self, base_url=None):
        self.base_url = base_url if base_url else settings.BILLING_BASE_URL
        # self.base_url='http://localhost:8081/v1.0/'


    def request(self, url,method='GET', headers={}, params=None, data=None, isJson=True):
        if isJson:
            headers['Content-Type'] = 'application/json'
        else:
            data = urllib.urlencode(data)
        if params:
            params = urllib.urlencode(params)
            url=url+"?%s"%params
        req = urllib2.Request(self.base_url+url, headers=headers)
        if method in ['PUT', 'DELETE']:
            req.get_method = lambda:method
        response = urllib2.urlopen(req, data)
        return response

def request(url,method='GET', headers={}, data=None, isJson=True):
    requestClient=RequestClient()
    return json.loads(requestClient.request(url, method, headers, None, data, isJson).read())

def getAccount(request):
    return json.loads(request.session['account'])

def request_billing(url,method='GET', headers={}, params=None, data=None, isJson=True):
    base_url=settings.BILLING_BASE_URL
    # base_url = 'http://localhost:8080/v1.0/'
    requestClient=RequestClient(base_url)
    return json.loads(requestClient.request(url, method, headers,params,data, isJson).read())

# if __name__=="__main__1":
#    url="http://localhost:8080/spch"
#    response=request(url)
#    print response.read()
#    print response.getcode()
#    print response.geturl()
#    print response.info()
# import sys
# print '======================'+sys.getdefaultencoding()
# url="http://localhost:8080/solr/rest/query/doc"
# data="searchTerm=outdoor&start=0&pageSize=15"
# req = urllib2.Request(url,data=data)
# req.get_method=lambda:"PUT"
# response = urllib2.urlopen(req)
# method="DELETE"
# print method in ['PUT','DELETE']


# for i in range(29, 46):
#     dict_acquire= {
#                     "invoice_id":i,
#                     "address_id":40,
#                     "type": "special",
#                     "title": "STcloud",
#                     "amount":1,
#                     "prove": "jjjj",
#                     "status": "apply",
#                     }
#
#     data_json=json.dumps({"invoice":dict_acquire})
#     #
#     result=request("/invoice/update/123hdfsfbsdf7uuieruiteb", method='PUT', data=data_json)
#
#     # data_json=json.dumps({'invoice':dict_acquire})
#     #
#     # result=request('/invoice/list/123hdfsfbsdf7uuieruiteb')
#     print result