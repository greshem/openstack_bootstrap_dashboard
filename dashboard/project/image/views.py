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
    template_name = "image/Imagemanage.html"

#    def get(self, request, *args, **kwargs):
        # if request.session.get('account',default=None) is None:
        #     return HttpResponseRedirect(settings.HORIZON_URL+'/auth/logout')
#        from dashboard.project.views1 import BillDetailsView
#        from django.core.urlresolvers import reverse
#        return HttpResponseRedirect(reverse('bill_details',args=args,kwargs=kwargs))

    def get_data(self):
        return {}

def image_list(request):
#    {u'status': u'active', u'virtual_size': None, u'name': u'CentOS6.5', u'deleted': False, u'container_format': u'bare', u'created_at': u'2016-08-31T08:31:50.000000', u'disk_format': u'qcow2', u'updated_at': u'2016-09-01T08:54:46.000000', u'properties': {u'os_distro': u'CentOS', u'os_version': u'CentOS6.5_x64', u'description': None, u'architecture': u'x86_64'}, u'owner': u'b8de93e20148470dbc45e802240c3d10', u'protected': False, u'min_ram': 1024, u'checksum': u'27f3d7458a306294905556051b65f6ad', u'min_disk': 20, u'is_public': True, u'deleted_at': None, u'id': u'8ee7cf40-59b7-4821-9adf-db1047ef49f2', u'size': 349437952}
#    {u'status': u'active', u'virtual_size': None, u'name': u'snapshot_centos', u'deleted': False, u'container_format': u'bare', u'created_at': u'2016-09-02T03:35:43.000000', u'disk_format': u'qcow2', u'updated_at': u'2016-09-02T03:36:23.000000', u'properties': {u'instance_uuid': u'5c09388e-b384-45d1-9fb6-5232840e21a6', u'image_location': u'snapshot', u'image_state': u'available', u'user_id': u'6944c1de6f96421b8d182d05702a37e7', u'os_distro': u'CentOS', u'image_type': u'snapshot', u'ramdisk_id': None, u'os_version': u'CentOS6.5_x64', u'kernel_id': None, u'architecture': u'x86_64', u'base_image_ref': u'3c26f6ba-d224-4c0f-b6ca-d69ce0b9ee01', u'owner_id': u'b8de93e20148470dbc45e802240c3d10'}, u'owner': u'b8de93e20148470dbc45e802240c3d10', u'protected': False, u'min_ram': 0, u'checksum': u'fbc2f3cab6e896b7ffa43efd7d438223', u'min_disk': 40, u'is_public': False, u'deleted_at': None, u'id': u'd46619e2-ed8f-4d94-864b-3ad893c728fa', u'size': 963575808}
    try:
        filters={}
        for item in request.GET.keys():
            if item not in ('limit','offset', 'order'):
                filters[item] = request.GET.get(item)
            elif item == 'offset':
                marker=request.GET.get(item)
            elif item=='limit':
                limit=request.GET.get(item)
            else:
                pass
        images = api.glance.image_list_detailed(
            request,
            marker=marker,
            paginate=False,
            filters=filters,
            limit=limit,
            sort_dir='asc',
            sort_key='name')
        result={'total':len(images)}
        rows=[]
        if images:
            for image in images:
                if image:
                    image_type=image.properties['image_type']if image.properties.has_key('image_type') else 'image'
                    is_owner=True if image.owner==request.user.project_id else False
                    description=image.properties['description'] if image.properties.has_key('description') else ''
                    rows.append({'description':description,'is_owner':is_owner,'min_ram':image.min_ram,'min_disk':image.min_disk,'protected':image.protected,'image_type':image_type,'status':image.status,'name':image.name,'created_at':image.created_at,'id':image.id,'size':int(image.size)/(1024*1024),'is_public':image.is_public})
        result['rows']=rows
    except Exception:
        result={'error':"exception"}
        images = []
        exceptions.handle(request, "Unable to retrieve images.")
    return HttpResponse(json.dumps(result))

def image_update(request):
    try:
        post_data=request.POST
        post_data=json.loads(post_data.get('root'))
        image_id=post_data['image_id']
        meta=post_data['data']
        api.glance.image_update(request, image_id,**meta)
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse('success')

def image_delete(request):
    try:
        image_ids=request.POST.get("image_ids")
        for image_id in image_ids.split(','):
            api.glance.image_delete(request, image_id)
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse('success')
    
    
def get_image(request):
    try:
        image_id=request.GET.get('image_id')
        image = api.glance.image_get(request, image_id)
        rows = []
        rows.append({
            'id':image.id,
            'name':image.name,
            'status':image.status,
            })
    except Exception:
        return HttpResponse('error')
        exceptions.handle(request,
                          _('Unable to get instance.'))
    return HttpResponse(json.dumps(rows))    
    
