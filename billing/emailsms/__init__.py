# --*-- coding: utf-8 --*--
__author__ = 'yamin'
from oslo_config import cfg
CONF = cfg.CONF
if_email=[cfg.BoolOpt('if_email',default=True,help=''),]
if_sms=[cfg.BoolOpt('if_sms',default=True,help=''),]

email_user=[
    cfg.DictOpt('email_user',
                default={
                    "username":"stcloud",
                    "email":"notice@stcloud.cn",#邮件地址
                    "smtp_server":"smtp.exmail.qq.com",#邮件服务
                    "sign":"", #签名
                    "password":"stcloud.cn123",
                    "telephone":""
                },
                help=''),
    ]
CONF.register_opts(if_email)
CONF.register_opts(if_sms)
CONF.register_opts(email_user)