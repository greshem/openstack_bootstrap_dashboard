# -*- coding:utf-8 -*-
'''
Created on 2015-8-28

@author: greshem
'''

def getDictFromReq(req,inKeys=None,notInKeys=None):
    if inKeys:
        return {key:value for (key,value) in req.params.items() if key in inKeys}
    if notInKeys:
        return {key:value for (key,value) in req.params.items() if key not in inKeys}
    return {key:value for (key,value) in req.params.items()}