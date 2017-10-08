# -*- coding:utf-8 -*-
'''
Created on 2015-11-11

@author: xuyamin
接口测试
'''
import requests
import json
import datetime
base_url="http://192.168.100.11:8080/v1.0"
billing_urls={
    "test_gift_order_create":("/gift/giftamount/","POST"),
    "test_recharge_order_create":("/recharge/create/","POST"),
    "test_instead_recharge_order_create":("/recharge/insteadrecharge","POST"),
    "test_freeze_create":("/notice/freezen/","GET"),
    "test_freeze3_create":("/notice/freezen3","GET"),
    "test_unfreeze_create":("/account/create","GET"),
    "test_del":("/notice/delResource/","GET"),
    "test_del3":("/notice/delResource3/","GET"),
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
def test_gift_order_create():
    '''
    赠送金额
    :return:
    '''
    url_para="fd6f08ae-9cbc-11e5-be79-fa163ee4b056"
    data={
        "gift":
            {
                "gift_by":"xiaow",
                "status":"pay_success",
                "gift_at":datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
                "amount":1.10,
                "remark":"gift 1000"
            }
    }
    response={}
    return data,response,url_para #parameter，和url参数


@create_request
def test_recharge_order_create():
    '''
    充值
    :return:
    '''
    url_para="fd6f08ae-9cbc-11e5-be79-fa163ee4b056"
    data={
        "instead_recharge": {
            "instead_recharge_by": "aaa",
            "instead_recharge_account": "szfdsfdsfgdfg",
            "remark":"........"
        },
        "recharge": {
            "payment_way": "alipay",
            "receive_account": "1234567890",
            "amount": 2000,
            "status": "paying ",
            "is_instead_recharge": True,
            "remark":"......"
        }
    }
    response={}
    return data,response,url_para #parameter，和url参数

@create_request
def test_instead_recharge_order_create():
    '''
    代充值
    :return:
    '''
    url_para=""
    data={
        "instead_recharge": {
            "instead_recharge_by": "aaa",
            "instead_recharge_account": "szfdsfdsfgdfg",
            "remark":"........"
        },
        "recharge": {
            "amount": 2000,
            "account_id": "fd6f08ae-9cbc-11e5-be79-fa163ee4b056"
        }
    }
    response={}
    return data,response,url_para #parameter，和url参数

@create_request
def test_freeze_create():
    '''
    冻结
    :return:
    '''
    url_para="fd6f08ae-9cbc-11e5-be79-fa163ee4b056"
    data={

    }
    response={}
    return data,response,url_para #parameter，和url参数

@create_request
def test_freeze3_create():
    '''
    代充值
    :return:
    '''
    url_para=""
    data={

    }
    response={}
    return data,response,url_para #parameter，和url参数

@create_request
def test_unfreeze_create():
    '''
    代充值
    :return:
    '''
    url_para=""
    data={

    }
    response={}
    return data,response,url_para #parameter，和url参数

@create_request
def test_del():
    '''
    代充值
    :return:
    '''
    url_para="fd6f08ae-9cbc-11e5-be79-fa163ee4b056"
    data={

    }
    response={}
    return data,response,url_para #parameter，和url参数

@create_request
def test_del3():
    '''
    代充值
    :return:
    '''
    url_para="fd6f08ae-9cbc-11e5-be79-fa163ee4b056"
    data={

    }
    response={}
    return data,response,url_para #parameter，和url参数

if __name__ == "__main__":
    #test_gift_order_create()
    #test_recharge_order_create()
    #test_instead_recharge_order_create()
    #test_freeze_create()
    test_freeze3_create()
    #test_unfreeze_create()
    #test_del()
    #test_del3()
