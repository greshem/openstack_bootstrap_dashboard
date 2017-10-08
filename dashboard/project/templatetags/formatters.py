#coding:utf-8
'''
Created on 2012-12-19
@author: yamin_xu@163.com
界面的格式转换
'''
from django.conf import settings
from django import template
from django.template.base import resolve_variable, Node, TemplateSyntaxError
import datetime
import time
import pytz
register = template.Library()

@register.filter(name="todate")
def todate(value):
    if type(value) in [str,unicode]:
        try:
            temp= datetime.datetime.strptime(value,"%Y-%m-%d")
            return temp.replace(tzinfo=pytz.UTC)
        except:
            try:
                temp=datetime.datetime.strptime(value,"%Y-%m-%d %H:%M:%S")
                return  temp.replace(tzinfo=pytz.UTC)#tzinfo=pytz.timezone('Asia/Shanghai')
            except:
                return value

if __name__=="__main__":
    temp_time=datetime.datetime.strptime("2015-11-08 13:05:35","%Y-%m-%d %H:%M:%S")
    temp_time=temp_time.replace(tzinfo=pytz.timezone('Asia/Shanghai'))
    temp_time.astimezone(pytz.UTC)