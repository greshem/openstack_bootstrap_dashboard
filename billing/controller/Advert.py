# -*- coding:utf-8 -*-
from billing.api import wsgi
from billing.util.controllerUtil import *
from billing.hander.Advert import getadvertList,advertUpdate,advertDelete,advertAdd,getadvertInfo,getvalidAdertList

class Controller(wsgi.Controller):
    '''公告管理'''
    def getAdvertList(self,req,**args):
        condition=req.json_body
        page_no=int(condition['page_no']) if (condition.has_key('page_no') and condition['page_no']) else 1
        page_size=int(condition['page_size']) if (condition.has_key('page_size') and condition['page_size']) else 10
        return getadvertList(condition,page_no,page_size)
    def advertAddHandle(self,req,**args):
        jsonParams = req.json_body
        return advertAdd(jsonParams)
    def advertDeleteHandle(self,req,**args):
        advert_id_list=req.json_body
        return advertDelete(advert_id_list)
    def advertUpdateHandle(self,req,**args):
        jsonParams = req.json_body
        advert_id = jsonParams['advert_id']
        updatecontent = jsonParams['content']
        return advertUpdate(updatecontent,advert_id)
    def getAdvertInfo(self,req,**args):
        advert_id=args.get('advert_id')
        return getadvertInfo(advert_id)
    def getValidAdvert(self,req,**args):
        return getvalidAdertList()
def create_resource():
    return wsgi.Resource(Controller())

