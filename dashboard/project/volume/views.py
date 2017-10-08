# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from dashboard.api.requestClient import request as req
from dashboard.views.base import HomePageView
import json
from dashboard.api.nova import server_list
from collections import OrderedDict
from dashboard import api
from horizon import exceptions
from dashboard.api import billing
import logging

LOG = logging.getLogger(__name__)

class indexView(HomePageView):
    template_name = "volumn/Volumnmanage.html"

#    def get(self, request, *args, **kwargs):
        # if request.session.get('account',default=None) is None:
        #     return HttpResponseRedirect(settings.HORIZON_URL+'/auth/logout')
#        from dashboard.project.views1 import BillDetailsView
#        from django.core.urlresolvers import reverse
#        return HttpResponseRedirect(reverse('bill_details',args=args,kwargs=kwargs))

    def get_data(self):
        return {}

def volume_availability_zone_list(request):
#    {u'zoneState': {u'available': True}, u'hosts': None, u'zoneName': u'nova'}
    try:
        result=[]
        zones=api.cinder.availability_zone_list(request)
        if zones:
            for zone in zones:
                result.append({'zoneName':zone.zoneName,'zoneState':zone.zoneState})
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse(json.dumps(result))


def volumn_list(request):
#    {'status': u'available', 'description': None, 'availability_zone': u'nova', 'bootable': u'false', 'encrypted': False, 'created_at': u'2016-08-10T00:55:43.000000', 'os-vol-tenant-attr:tenant_id': u'b8de93e20148470dbc45e802240c3d10', 'transfer': None, 'volume_type': None, 'name': u'disk1', 'attachments': [], 'os-vol-host-attr:host': u'control@lvm#lvm', 'consistencygroup_id': None, 'source_volid': None, 'snapshot_id': None, 'metadata': {}, 'id': u'7acbf9bc-bc58-49c3-885c-467e2adf1894', 'size': 1}
    try:
        search_opts = {}
        volumes = \
            api.cinder.volume_list_paged(request, marker=None,limit=None,
                                         search_opts=search_opts,
                                         sort_dir=None, paginate=False)

        result = {'total':len(volumes)}
        rows = []
        for volume in volumes:
            attachments=''
            volume_name = None
            if volume.attachments:
                for attachment in volume.attachments:
                    instance=api.nova.server_get(request, attachment['server_id'])
                    if attachments:
                        attachments=attachments+u'<br/>云主机：'+instance.name+u'，分区：'+attachment['device']
                    else:
                        attachments=u'云主机：'+instance.name+u'，分区：'+attachment['device']
                    volume_name = instance.name
            if not volume_name:
                volume_name = volume.name
            rows.append({'status':volume.status,'availability_zone':volume.availability_zone,'description':volume.description,'created_at':volume.created_at, 'name':volume_name, 'attachments':attachments, 'id':volume.id, 'size':volume.size})
        result['rows'] = rows
        return HttpResponse(json.dumps(result))
    except Exception:
        exceptions.handle(request,
                          ('Unable to retrieve volume list.'))
        return HttpResponse(json.dumps({}))

def volume_create(request):
    try:
        post_data = request.POST
        name = post_data.get('name')
        size=int(post_data.get('size'))
        description= post_data.get('description')
        az= post_data.get('availability_zone')
        if az=='':
            az="nova";
        volume = api.cinder.volume_create(request,
                                          size,
                                          name,
                                          description,
                                          None,
                                          availability_zone=az)       
        if volume:
            return HttpResponse('success')
        else:
            HttpResponse('error')
    except Exception as e :
        #print "INFO: error %s"%e;
        LOG.exception('E2234:  volume_creat exception  %s '%e );
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
def getPriceDiscount(request):
    try:
        region_id = 'RegionOne'
        #    region_id=request.GET.get('region_id')
        account = request.session.get('account')
        billingItems = ('disk_1_G',)
        #    result={'cpu_1_core':{'price':0.23,'discount_ratio':0.95}}
        result = {}
        for billingItem in billingItems:
            url = '/billingItem/getBillingItem?billing_item=' + billingItem + '&region_id=' + region_id
            billingIt = billing.request(url)
            result[billingItem] = {'price':billingIt['billing_item']['price']}
            url = '/discount/detail/' + account['account_id'] + '?billing_item_id=' + str(billingIt['billing_item']['billing_item_id'])
            discount = billing.request(url)
            result[billingItem]['discount_ratio'] = discount['discount']['discount_ratio'] if discount['discount'] and discount['discount'].has_key('discount_ratio') else 1
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse(json.dumps(result))

def volume_extend(request):
    try:
        post_data = request.POST
        volume_id = post_data.get('id')
        new_size=int(post_data.get('size'))
        volume=api.cinder.volume_extend(request, volume_id, new_size)
        if volume:
            return HttpResponse('success')
        else:
            HttpResponse('error')
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')

def volume_delete(request):
    try:
        volume_ids=request.POST.get("volume_ids")
        for volume_id in volume_ids.split(','):
            api.cinder.volume_delete(request, volume_id)
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse('success')

def volume_update(request):
    try:
        post_data=request.POST
        volume_id=post_data.get('volume_id')
        name=post_data.get('name')
        description=post_data.get('description')
        api.cinder.volume_update(request, volume_id, name, description)
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse('success')

def volume_detach(request):
    try:
        volume_id=request.POST.get("volume_id")
        volume=api.cinder.volume_get(request, volume_id)
        instance_id=volume.attachments[0]['server_id']
        attachment_id=volume.attachments[0]['id']
        api.nova.instance_volume_detach(request, instance_id, attachment_id)
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse('success')

def volume_attach(request):
    try:
        volume_id=request.POST.get("volume_id")
        instance_id=request.POST.get("instance_id")
        api.nova.instance_volume_attach(request, volume_id, instance_id, None)
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse('success')

