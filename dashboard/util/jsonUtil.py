# -*- coding:utf-8 -*-
'''
Created on 2015年11月24日

@author: greshem
'''
import json
from datetime import datetime
from datetime import date
from decimal import Decimal
class CJsonEncoder(json.JSONEncoder):    
    def default(self, obj):        
        if isinstance(obj, datetime):            
            return obj.strftime('%Y-%m-%d %H:%M:%S')        
        elif isinstance(obj, date):            
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj,Decimal):
            return str(obj)       
        else:
            try:            
                return json.JSONEncoder.default(self, obj)
            except Exception as e:
                d = {} 
#                print type(obj)
                d.update(obj.__dict__)
                return {key:d[key] for key in d.keys() if not key.startswith('_') }

def outJson(data):
    return json.dumps(data,cls=CJsonEncoder, ensure_ascii=False)