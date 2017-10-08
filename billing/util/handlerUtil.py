# -*- coding:utf-8 -*-
'''
Created on 2015-8-24

@author: greshem
'''
import json
from datetime import datetime
from datetime import date
from decimal import Decimal

#def encoder():  
#    _visited_objs = []  
#    class Encoder(json.JSONEncoder):  
#        def default(self, obj):  
##            if isinstance(obj.__class__, DeclarativeMeta):  
#            if obj in _visited_objs:  
#                return None  
#            _visited_objs.append(obj)  
#            fields = {}  
#            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:  
#                data = obj.__getattribute__(field)  
#                try:  
#                    if isinstance(data, datetime):   
#                        data = data.strftime('%Y-%m-%d %H:%M:%S')   
#                    json.dumps(data)  # this will fail on non-encodable values, like other classes   
#                    fields[field] = data  
#                except TypeError:  
#                    fields[field] = None  
#            return fields  
#  
#            return json.JSONEncoder.default(self, obj)  
#    return Encoder  
#
#def new_encoder():
#    _visited_objs = []  
#    class Encoder(json.JSONEncoder):  
#        def default(self, obj):  
##            if isinstance(obj.__class__, DeclarativeMeta):  
#            if obj in _visited_objs:  
#                return None  
#            _visited_objs.append(obj)  
#            fields = {}  
#            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:  
#                data = obj.__getattribute__(field)  
#                try:  
#                    if isinstance(data, datetime):   
#                        data = data.strftime('%Y-%m-%d %H:%M:%S')   
#                    json.dumps(data)  # this will fail on non-encodable values, like other classes   
#                    fields[field] = data  
#                except TypeError:  
#                    fields[field] = None  
#            return fields  
#  
#            return json.JSONEncoder.default(self, obj)  
#    return Encoder


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


""" 成功返回结果 """
def outSuccess(key, data):
    return json.dumps({key:data,"success":"success"},cls=CJsonEncoder, ensure_ascii=False)

'''返回数据库查询某一行的字典'''
def row2dict(row):
    '''
    如果包含字段json，则将其解析为json数据
    :param row:
    :return:
    '''
    return_info={}
    if row:
        for key in row._parent.keys:
            if "_json" in key:
                return_info[key.replace("_json","")]=json.loads(getattr(row,key))
            else:
                return_info[key]=getattr(row,key)
        return return_info
    else:
        return row

""" 错误返回结果 """
def outError(data):
    return json.dumps({"msg":data, "success":"error"}, ensure_ascii=False)

"""将JSON字典赋值给对象 """
def getObjFromJson(obj, jsonDict):
    if jsonDict:
        for (key, value) in jsonDict.items():
            if hasattr(obj, key):
                obj[key] = value

"""将对象转化为json的字典"""
def getJsonFromObj(obj, notInDict=[]):
    if obj:
        jsonstr = {}
        for key in [x for x in dir(obj) if not x.startswith('_') and x not in ["get", "iteritems", "metadata", "next", "save", "update"] and x not in notInDict]:
            jsonstr[key] = getattr(obj, key)
        return jsonstr
    return None


if __name__ == "__main__":
    jsonstr = {"account_id":"asdadsad"}
    from billing.db.object.models import Account
    account = Account()
    print dir(account)
    getObjFromJson(account, jsonstr)
    print account.account_id
