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
    "test_workorder_create":("/workorder/create/workorder","POST"),
    "test_workordertype_create":("/workorder/create/type","POST"),
    "test_workorderrecord_create":("/workorder/create/record","POST"),
    "test_workorder_update":("/workorder/update","POST"),
    "test_workorder_detail":("/workorder/detail/","GET"),
    "test_workorder_list":("/workorder/list/workorder","GET"),
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
def test_workorder_create():
    '''
    赠送金额
    :return:
    '''
    url_para=""
    # data={
    #     "applicant":"xu",
    #     "type":"故障工单",
    #     "theme":"first",
    #     "content":"good"
    # }
    data={
        "applicant":"xu",
        "type":"商务咨询工单",
        "theme":"second",
        "content":"good"
    }
    response={}
    return data,response,url_para #parameter，和url参数

@create_request
def test_workordertype_create():
    '''
    赠送金额
    :return:
    '''
    url_para=""
    # data={
    #     "name":"故障工单",
    #     "remark":"产生故障",
    # }
    data={
        "name":"商务咨询工单",
        "remark":"客户咨询",
    }
    response={}
    return data,response,url_para #parameter，和url参数

@create_request
def test_workorderrecord_create():
    '''
    赠送金额
    :return:
    '''
    url_para=""
    data={
        "workorderno":"20151222090739",
        "content":"怎么样了",
        "applier":"xu",
    }
    response={}
    return data,response,url_para #parameter，和url参数

@create_request
def test_workorder_update():
    '''
    赠送金额
    :return:
    '''
    url_para=""
    data={
        "workorderno":"20151222090739",
        "status":"处理中",
    }
    response={}
    return data,response,url_para #parameter，和url参数

@create_request
def test_workorder_detail():
    '''
    赠送金额
    :return:
    '''
    url_para="20151222090739"
    data={
    }
    response={}
    return data,response,url_para #parameter，和url参数

@create_request
def test_workorder_list():
    '''
    赠送金额
    :return:
    '''
    url_para=""
    data={
        "pageNo":1,
        "pageSize":10,
        "user":"xu",
        "operate":"me_handle",
        "status":"处理中",
        "type":"故障工单",
        "sno":"739"
    }
    response={}
    return data,response,url_para #parameter，和url参数

if __name__ == "__main__":
    #test_workorder_create()
    #test_workordertype_create()
    #test_workorderrecord_create()
    #test_workorder_list()
    test_workorder_detail()