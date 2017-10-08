# -*- coding:utf-8 -*-
'''
Created on 2015-11-11

@author: xuyamin
接口测试
'''
import requests
import json

base_url="http://192.168.100.11:8081/v1.0"
billing_urls={
    "test_account_create":("/account/create","POST"),
    "test_account_update":("/account/update/","PUT"),
    "test_account_listByPage":("/account/list","GET"),
    "test_account_detail":("/account/detail/","GET"),
    #"test_account_getAccountByUserID":("",""),
    #"test_account_getAccountByProjectId":("",""),
    "test_account_delete":("/account/delete/","DELETE"),
    "test_account_getSubAccountSum":("/account/getsubaccountsum/","GET"),
    "test_account_subAccountList":("/account/subaccountlist/","GET"),
    "test_account_subAccountDetail":("/account/subaccountdetail/","GET"),
    "test_account_subAccountAmountSum":("/account/subaccountamountsum/","GET"),
    "test_account_subAccountConsumptionList":("/account/subaccountconsumptionlist/","GET"),
    }
def create_request(func):
    try:
        request_url=billing_urls[func.__name__][0]
        method=billing_urls[func.__name__][1]
    except:
        pass
    def is_success(data):
        if data["success"]=="success":
            return True
        else:
            return False
    def request_func():
        data,assert_response,url_para=func()
        headers={'content-type':'application/json'}
        if method=="GET":
            response=requests.get(url=base_url+request_url+url_para,params=data,headers=headers)
        elif method=="POST":
            response=requests.post(url=base_url+request_url+url_para,data=json.dumps(data),headers=headers)
        else:
            response=requests.request(method=method,url=base_url+request_url+url_para,data=json.dumps(data),headers=headers)
        return is_success(json.loads(response.text))
    return request_func

@create_request
def test_account_create():
    url_para=""
    data={
        "account":{
            "account_id":"baby004",
            "username":"test1@test.com",
            "cash_balance":10000.00,
            "gift_balance":5000.00,
            "type":"credit",
            "credit_line":5000.00,
            "status":"good",
            "frozen_status":"frozen",
        }
    }
    response={}
    return data,response,url_para #parameter，和url参数

@create_request
def test_account_update():
    url_para="baby003"
    data={
        "account":{
            "username":"greshem123",
            "cash_balance":"10001.00",
            "gift_balance":5001.00,
            "type":"credit",
            "credit_line":5000.00,
            "status":"normal",
            "frozen_status":"normal"
            }
    }
    response={}

    return data,response,url_para

@create_request
def test_account_listByPage():
    url_para=""
    data={
        "pageSize":10,
        "pageNo":1,
        #"type":"",
        "status":"normal",  #   账户状态(normal, frozen,deleted)
        "frozen_status":"normal"
        #"username": ""#    用户名模糊查找)
    }
    response={}
    return data,response,url_para

@create_request
def test_account_detail():
    url_para="52669b25-86b8-11e5-be79-fa163ee4b056" #account_id
    data={}
    response={}
    return data,response,url_para

@create_request
def test_account_getAccountByUserID():
    url_para=""
    data={}
    response={}
    return data,response,url_para

@create_request
def test_account_getAccountByProjectId():
    url_para=""
    data={}
    response={}
    return data,response,url_para

@create_request
def test_account_delete():
    url_para="ashajha"
    data={}
    response={}
    return data,response,url_para

@create_request
def test_account_getSubAccountSum():
    url_para="account_id"
    data={}
    response={}
    return data,response,url_para

@create_request
def test_account_subAccountList():
    url_para="account_id"
    data={}
    response={}
    return data,response,url_para

@create_request
def test_account_subAccountDetail():
    url_para="account_id"
    data={}
    response={}
    return data,response,url_para

@create_request
def test_account_subAccountAmountSum():
    url_para="account_id"
    data={}
    response={}
    return data,response,url_para

@create_request
def test_account_subAccountConsumptionList():
    url_para="account_id"
    data={}
    response={}
    return data,response,url_para


if __name__ == "__main__":
    #test_account_listByPage()
    #test_account_delete()
    #test_account_create()
    test_account_update()