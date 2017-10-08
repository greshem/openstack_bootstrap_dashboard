# -*- coding:utf-8 -*-
from billing.db.sqlalchemy import session as sa
from billing.db.dao.advertDao import AdvertDao
from billing.db.object.models import Advert
from oslo_log import log as logging
import traceback
import json
from billing.util.handlerUtil import *
import datetime

LOG=logging.getLogger(__name__)

def advertAdd(exitcontent):
    try:
        advert_temp=Advert()
        advert_temp.title = exitcontent['title']
        advert_temp.url = exitcontent['url']
        advert_temp.started_at = exitcontent['started_at']
        advert_temp.ended_at = exitcontent['ended_at']
        advertdao_temp=AdvertDao(advert_temp)
        advertdao_temp.add()
        return outSuccess('result','增加公告成功')
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError('增加公告失败')

def advertDelete(advert_id_list):
    try:
        session=sa.get_session()
        if advert_id_list:
            for item in advert_id_list:
                advert_temp=Advert()
                advert_temp.advert_id = int(item)
                advertdao_temp=AdvertDao(advert_temp)
                advertdao_temp.delete(session)
        return outSuccess('result','删除公告成功')
    except Exception as e:
        session.close()
        LOG.error(traceback.format_exc())
        LOG.error(str(e))
        raise e

def advertUpdate(value,advert_id):
    try:
        if value:
            advert_temp=Advert()
            advert_temp.advert_id = advert_id
            advertdao_temp=AdvertDao(advert_temp)
            advertdao_temp.update(value)
        return outSuccess('result','公告更新成功')
    except Exception as e:
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError('更新公告失败')

def getadvertList(condition=None,page_no=1,page_size=15,edge_size=0):
    def func(a):
        if a['advert_status'] == condition['advert_status']:
            return 1
        else:
            return 0
    try:
        templist=[]
        session = sa.get_session()
        advertdao_temp=AdvertDao()
        result=advertdao_temp.list(condition,session)
        time_now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if result:
            for item in result:
                tempdict={}
                tempdict['title']=item.title
                tempdict['url']=item.url
                tempdict['started_at']=item.started_at
                tempdict['ended_at']=item.ended_at
                tempdict['created_at']=item.created_at
                tempdict['advert_id']=item.advert_id
                if time_now >= str(item.ended_at):
                    tempdict['advert_status']='invalid'
                else:
                    tempdict['advert_status']='effective'
                templist.append(tempdict)
            if condition.has_key('advert_status') and condition['advert_status']:
                templist=filter(func,templist)
        count=len(templist)
        templist=templist[(page_no-1)*page_size:(page_no*page_size)]
        return json.dumps({'count':count,'advert_list':templist,'success':'success'},cls=CJsonEncoder, ensure_ascii=False)
    except Exception as e:
        session.close()
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("获取公告列表失败!")

def getadvertInfo(advert_id):
    advert_temp=Advert()
    advert_temp.advert_id = advert_id
    advertdao_temp = AdvertDao(advert_temp)
    result = advertdao_temp.getadvertinfo()
    content={}
    if result:
        content['title']=result.title
        content['url'] = result.url
        content['started_at'] = str(result.started_at)
        content['ended_at'] = str(result.ended_at)
    return json.dumps(content)

def getvalidAdertList():
    try:
        session = sa.get_session()
        temp = AdvertDao()
        advert_list_temp = temp.getvalidadvert()
        advert_list=[]
        if advert_list_temp:
            for item in advert_list_temp:
                tempdict={}
                tempdict['advert_id'] = item.advert_id
                tempdict['title'] = item.title
                tempdict['url'] = item.url
                tempdict['started_at'] = item.started_at
                tempdict['ended_at'] = item.ended_at
                tempdict['created_at'] = item.created_at
                tempdict['updated_at'] = item.updated_at
                advert_list.append(tempdict)
        count=len(advert_list)
        return json.dumps({'count':count,'valid_advert_list':advert_list,'success':'success'},cls=CJsonEncoder, ensure_ascii=False)
    except Exception as e:
        session.close()
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("获取有效公告失败!")



if __name__=='__main__':
    temp=getvalidAdertList()
    print temp
