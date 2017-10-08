# -*- coding:utf-8 -*-
'''
Created on 2014-7-7

@author: greshem
'''
import urllib2
import urllib
def request(url,method='GET',headers={},data=None,isJson=False):
    if isJson:
        headers['Content-Type']='application/json'
    else:
        data=urllib.urlencode(data)
    req = urllib2.Request(url,headers=headers)
    if method in ['PUT','DELETE']:
        req.get_method=lambda:method
    response = urllib2.urlopen(req,data)
    return response


#if __name__=="__main__1":
#    url="http://localhost:8080/spch"
#    response=request(url)
#    print response.read()
#    print response.getcode()
#    print response.geturl()
#    print response.info()
#import sys
#print '======================'+sys.getdefaultencoding()
#url="http://localhost:8080/solr/rest/query/doc"
#data="searchTerm=outdoor&start=0&pageSize=15"
#req = urllib2.Request(url,data=data)
#req.get_method=lambda:"PUT"
#response = urllib2.urlopen(req)
#method="DELETE"
#print method in ['PUT','DELETE']