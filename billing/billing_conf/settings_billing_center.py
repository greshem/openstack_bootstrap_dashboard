# -*- coding:utf-8 -*-
BILLING_BASE_URL="http://10.2.10.25:8080/v1.0/"
#BILLING_BASE_URL="http://192.168.100.155:8080/v1.0/"
#BILLING_BASE_URL= 'http://192.168.210.28:8080/v1.0/'
#BILLING_BASE_URL= 'http://192.168.210.35:6888/v1.0/'
#BILLING_BASE_URL= 'http://0.0.0.0:8081/v1.0/'
#BILLING_BASE_URL= 'http://192.168.210.35:6888/v1.0/'
#BILLING_BASE_URL= 'http://127.0.0.1:8080/v1.0/'
#BILLING_BASE_URL= 'http://localhost:8080/v1.0/'
#BILLING_BASE_URL= 'http://192.168.210.29:6888/v1.0/'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': ['10.2.10.11:11211'],
    }
}
PAYMENT_URL="http://192.168.100.11:8000/payment/checkout"
HORIZON_URL="http://192.168.100.135:8090"
OPENSTACK_HOST='10.2.10.10'
NAAS_URL="http://192.168.210.29"
SUBACCOUT_URL="http://192.168.210.29"
HORIZON_HELP_URL="http://www.stcloud.cn/help/html/zhinan/jieshao/"
HORIZON_WO_URL="http://120.131.81.27/otrs/customer.pl"
MD5_KEY="ac092800-fc0"
SECRET_KEY = 'zXUBTIHfHmBEq6oUtWU7ZjagA2dKJuIx6a6ILXC8XIGBuCs050hnuTTB8X2NmuoC'
BASE_URL="/billing"
TIME_ZONE="Asia/Shanghai"
LOG_BASE_URL = 'http://192.168.210.200:6889/v1.0'
GIFT_VALUE=10
#SESSION_COOKIE_DOMAIN='192.168.100.11:8001'
#SESSION_COOKIE_NAME='sessionId'
#SESSION_COOKIE_DOMAIN = '192.168.100.11'
HOSTMANAGE=[
    'www.systest.net',
    'cloud.daily-tech.cn',
    'cloud.ynyun.cn'
]

OPENSTACK_ENDPOINT_TYPE = "publicURL"
OPENSTACK_KEYSTONE_URL = "http://%s:5000/v3" % OPENSTACK_HOST
ADMINUSER={'name':'admin','password':'admin'}

QUOTA_DEFAULT ={
    'nova': {
              "ram": 4096,
               "instances": 4,
               "cores": 4
    },
    'cinder': {
        "volumes": 2,
        "snapshots": 2,
        "volume_gigabytes": 2000,
        "snapshot_gigabytes": 2000
    },
    'neutron': {
        "floatingip": 1,'pool':1, "network": 1, "port": 128, "router": 1, "subnet": 1, "bandwidth": 10
    }
}
DEFAULT_ROLE='user'
PARENT_ID='d43f82c4d4c6441597fc5ad846dad508'
DEFAULT_REGION_ID='RegionOne'
PROJECT_PARENT_ID='63ab084e34b34850852f1c2f98285a93'
#SESSION_COOKIE_NAME = 'business_session_id'

LOGIN_URL=''
LOGIN_REDIRECT_URL=''
CDNLIMIT=1
DEV= True
