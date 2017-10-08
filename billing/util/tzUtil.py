# -*- coding:utf-8 -*-
'''
Created on 2015年11月16日

@author: greshem
'''
import pytz
import datetime
def change2UTC(date,timezone='Asia/Shanghai',format='%Y-%m-%d %H:%M:%S'):
    if date is None:
        return None
    tz = pytz.timezone(timezone)
    utc = pytz.utc
    if isinstance(date, unicode):
        date=date.encode()
    if isinstance(date, str):
        date=datetime.datetime.strptime(date, format)
        date=tz.localize(date)
        date=date.astimezone(utc)
        return datetime.datetime.strftime(date,'%Y-%m-%d %H:%M:%S')
    date=tz.localize(date)
    date=date.astimezone(utc)
    return date

def datetime2Str(date,informat='%Y-%m-%d %H:%M:%S',outformat='%Y-%m-%d %H:%M:%S'):
    if date is None:
        return None
    if isinstance(date, unicode):
        date=date.encode()
    if isinstance(date, str):
        date=datetime.datetime.strptime(date, informat)
    return datetime.datetime.strftime(date,outformat)
    