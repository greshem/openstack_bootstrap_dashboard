# -*- coding:utf-8 -*-
'''
Created on 2014-7-18

@author: greshem
'''
# import const
#
# #""" 用户状态 """
# #const.user_state = {'activity':'activity', 'suspend':'suspend', 'delete':'delete', 'creating':'creating'}
# #const.token_header = "token_auth"
# #const.searchCenterUrl = "http://localhost:8080/solr/rest"
#
# const.account_type=["credit","normal"]
# const.account_status=['normal','frozen','deleted']
# const.address_status=["using","deleted"]
# const.alipay_info_status=["pay_success","pay_error"]
# const.gift_status=["pay_success","pay_error","paying"]
# const.recharge_status=["pay_success","pay_error","paying"]
# const.order_status=["ordered","pay_success","pay_error"]

class constVar(object):
    billingItemToName={
        'cdnflow_1_G':'CDN流量',
        'cdnbandwidth_1_M':'CDN带宽',
        'instance_1':'实例',
        'cpu_1_core':'CPU',
        'memory_1024_M':'内存',
        'disk_1_G':'云硬盘',
        'sanpshot_1_G':'快照',
        'router_1':'路由器',
        'ip_1':'浮动IP',
        'bandwidth_1_M':'带宽',
        'image_1':'镜像',
        'vpn_1':'VPN'
    }
    discountEdit={
        0:'memory_1024_M',
        1:'router_1',
        2:'bandwidth_1_M',
        3:'cpu_1_core',
        4:'ip_1',
        5:'cdnflow_1_G',
        6:'cdnbandwidth_1_M',
        7:'snapshot_1_G',
        8:'disk_1_G',
    }