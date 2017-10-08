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
from dashboard.util import billingUtil
import logging

LOG = logging.getLogger(__name__)
LIMIT=10

class indexView(HomePageView):
    template_name = "floatingip/floatingipManage.html"

#    def get(self, request, *args, **kwargs):
        # if request.session.get('account',default=None) is None:
        #     return HttpResponseRedirect(settings.HORIZON_URL+'/auth/logout')
#        from dashboard.project.views1 import BillDetailsView
#        from django.core.urlresolvers import reverse
#        return HttpResponseRedirect(reverse('bill_details',args=args,kwargs=kwargs))

    def get_data(self):
        return {}

def floatingip_list(request):
#    {u'router_id': None, u'status': u'DOWN', u'description': u'', u'dns_name': u'', 
# 'fixed_ip': None, 'instance_id': None, u'dns_domain': u'', u'floating_network_id': u'0ebe2af2-9d81-4964-
# ae0d-bbe918620839', 'instance_type': None, 'ip': u'2.2.2.15', u'fixed_ip_address': None, 
# u'floating_ip_address': u'2.2.2.15', u'tenant_id': u'b8de93e20148470dbc45e802240c3d10', u'port_id': 
# None, u'id': u'17f586ac-690c-49e2-856a-b3d9fb815273', 'pool': u'0ebe2af2-9d81-4964-ae0d-
# bbe918620839'}
    try:
        floating_ip_address=request.GET.get('floating_ip_address')
        if floating_ip_address:
            floatingips,total=api.network.tenant_floating_ip_list(request,floating_ip_address=floating_ip_address)
        else:
            floatingips,total=api.network.tenant_floating_ip_list(request)
        result={'total':total}
        rows=[]
        floating_ip_pools = api.network.floating_ip_pools_list(request)
        pool_dict = dict([(obj.id, obj.name) for obj in floating_ip_pools])
        instances = api.nova.server_list(request, search_opts={})
        total = len(instances)
        instance_dict=dict([(obj.id,obj.name)for obj in instances])
        for floatingip in floatingips:
            rows.append({'floating_network_id':floatingip.floating_network_id,'instance_id':floatingip.instance_id,'fixed_ip_info':_getFixedIpInfo(request, floatingip, instance_dict, total),'pool_name':pool_dict[floatingip.pool],'pool_id':floatingip.pool,'instance_type':floatingip.instance_type,'fixed_ip_address':floatingip.fixed_ip_address,'status':floatingip.status,'id':floatingip.id,'floating_ip_address':floatingip.floating_ip_address})
        result['rows']=rows
    except Exception:
        result = []
        exceptions.handle(request, _("Unable to retrieve images."))
    return HttpResponse(json.dumps(result))

def floatingip_noassociate_list(request):
#    {u'router_id': None, u'status': u'DOWN', u'description': u'', u'dns_name': u'', 
# 'fixed_ip': None, 'instance_id': None, u'dns_domain': u'', u'floating_network_id': u'0ebe2af2-9d81-4964-
# ae0d-bbe918620839', 'instance_type': None, 'ip': u'2.2.2.15', u'fixed_ip_address': None, 
# u'floating_ip_address': u'2.2.2.15', u'tenant_id': u'b8de93e20148470dbc45e802240c3d10', u'port_id': 
# None, u'id': u'17f586ac-690c-49e2-856a-b3d9fb815273', 'pool': u'0ebe2af2-9d81-4964-ae0d-
# bbe918620839'}
    try:
        floatingips, total=api.network.tenant_floating_ip_list(request, search_opts={})
        rows=[]
        floating_ip_pools = api.network.floating_ip_pools_list(request)
        pool_dict = dict([(obj.id, obj.name) for obj in floating_ip_pools])
        instances = api.nova.server_list(request, search_opts={})
        total = len(instances)
        instance_dict=dict([(obj.id,obj.name)for obj in instances])
        for floatingip in floatingips:
            rows.append({'fixed_ip_info':_getFixedIpInfo(request, floatingip, instance_dict, total),'pool_name':pool_dict[floatingip.pool],'status':floatingip.status,'id':floatingip.id,'floating_ip_address':floatingip.floating_ip_address})
        rows=[row for row in rows if row['fixed_ip_info'] is None]
    except Exception:
        rows = []
        exceptions.handle(request, _("Unable to retrieve images."))
    return HttpResponse(json.dumps(rows))

def floatingip_associate(request):
    try:
        floatingip_id=request.POST.get('floatingip_id')
        port_id=request.POST.get('port_id')
        fixed_ip_address=request.POST.get('fixed_ip_address')
        api.network.floating_ip_associate(request, floatingip_id,port_id+'_'+fixed_ip_address)
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse('success')

def floatingip_disassociate(request):
    try:
        floatingip_id=request.GET.get('floatingip_id')
        api.network.floating_ip_disassociate(request, floatingip_id)
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse('success')

def floatingip_pools_list(request):
    try:
        floating_ip_pools=api.network.floating_ip_pools_list(request)
        result = []
        for floating_ip_pool in floating_ip_pools:
            result.append({'id':floating_ip_pool.id,'name':floating_ip_pool.name})
    except Exception:
        result = []
        exceptions.handle(request, _("Unable to retrieve images."))
    return HttpResponse(json.dumps(result))

def getPriceDiscount(request):
    try:
        account = request.session.get('account')
        billingItems = ('ip_1',)
        result=billingUtil.getPriceDiscount('RegionOne', account, billingItems)
    except Exception:
        result = []
        exceptions.handle(request, _("Unable to retrieve images."))
    return HttpResponse(json.dumps(result))

def floatingip_allocate(request):
    try:
        pool_id=request.POST.get('pool_id')
        api.network.tenant_floating_ip_allocate(request, pool_id)
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse('success')

def floatingip_delete(request):
    fip_ids = request.POST.get('floatingip_ids')
    try:
        for fip_id in fip_ids.split(','):
            api.network.tenant_floating_ip_release(request,fip_id)
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse('success')


def port_list(request):
#    dict: {u'allowed_address_pairs': [], u'extra_dhcp_opts': [], u'binding__vif_details': {u'port_filter': True, u'ovs_hybrid_plug': True}, u'updated_at': u'2016-09-21T08:09:26', u'device_owner': u'compute:nova', u'binding__host_id': u'cns-1', u'binding__vif_type': u'ovs', u'port_security_enabled': True, u'binding:profile': {}, u'fixed_ips': [{u'subnet_id': u'b2baf502-efd6-49b5-ac74-dcfa73d8a864', u'ip_address': u'11.1.1.45'}], u'id': u'0e86d185-558b-4fe5-8375-090694504a11', u'security_groups': [u'8becc904-c781-4ffd-8376-ea70b9dcc38e'], u'binding:vif_details': {u'port_filter': True, u'ovs_hybrid_plug': True}, u'binding__profile': {}, u'binding:vif_type': u'ovs', u'qos_policy_id': None, u'mac_address': u'fa:16:3e:53:84:8d', u'status': u'ACTIVE', u'binding:host_id': u'cns-1', u'description': u'', 'admin_state': 'UP', u'device_id': u'9f3d725d-f22c-48b9-ad85-05e82ef27530', u'name': u'', u'admin_state_up': True, u'network_id': u'8c3a96c7-bfde-4e1c-96c6-8d68ccc12568', u'dns_name': None, u'create...
    try:
        limit=request.GET.get('limit')
        offset=request.GET.get('offset')
        floating_ip_ports,total=api.neutron.port_list(request,tenant_id = request.user.tenant_id,marker=str(offset)+'_'+str(limit),page=True)
        result = {'total':total}
        rows=[]
        floatingips,floatingip_total=api.network.tenant_floating_ip_list(request,marker='0_'+str(LIMIT))
#        floatingip_dict=dict([(obj.floating_ip_address, obj.port_id) for obj in floatingips])
        instances = api.nova.server_list(request, search_opts={})
        instance_dict=dict([(obj.id,obj.name)for obj in instances])
        instance_total = len(instances)
        for floating_ip_port in floating_ip_ports:
            rows.append({'status':floating_ip_port.status,'device_owner':floating_ip_port.device_owner,'fixed_ip_address':_getFix(floating_ip_port),'device_name':_getDeviceInfo(request,floating_ip_port,instance_dict,instance_total),'device_id':floating_ip_port.device_id,'id':floating_ip_port.id,'name':floating_ip_port.name,'floating_ip_address':_getFloatingIpInfo(request,floating_ip_port.id,floatingips,floatingip_total)})
        result['rows']=rows
    except Exception:
        result = []
        exceptions.handle(request, _("Unable to retrieve images."))
    return HttpResponse(json.dumps(result))

def _getFix(floating_ip_port):
    if floating_ip_port and floating_ip_port.fixed_ips:
        fixed_ip_address=''
        for fixed_ip in floating_ip_port.fixed_ips:
            if fixed_ip_address:
                fixed_ip_address=fixed_ip_address+'</br>'+fixed_ip['ip_address']
            else:
                fixed_ip_address=fixed_ip['ip_address']
        return fixed_ip_address
    return None
        

def _getDeviceInfo(request,floating_ip_port,instance_dict,total):
    if floating_ip_port.device_owner not in('compute:nova','neutron:LOADBALANCERV2'):
        return None
    elif floating_ip_port.device_owner=='compute:nova':
        if instance_dict.has_key(floating_ip_port.device_id):
            return instance_dict[floating_ip_port.device_id] 
        while True:
            if len(instance_dict.keys())==total:
                return None
            instances,total = api.nova.server_list(request,search_opts={'limit':LIMIT,'marker':len(instance_dict.keys()),'paginate': True})
            instance_dict=dict(instance_dict,**dict([(obj.id,obj.name)for obj in instances]))
            if instance_dict.has_key(floating_ip_port.device_id):
                return instance_dict[floating_ip_port.device_id]
    return None
    

def _getFixedIpInfo(request,floatingip,instance_dict,total):
    if floatingip.instance_type is None:
        return None
    if floatingip.instance_type=='loadbalancer':
        return '负载均衡 VIP'
    elif floatingip.instance_type=='compute':
        if instance_dict.has_key(floatingip.instance_id):
            return instance_dict[floatingip.instance_id]
        if len(instance_dict.keys())==total:
            return None
        while True:
            if len(instance_dict.keys())==total:
                return None
            instances = api.nova.server_list(request)
            instance_dict=dict(instance_dict,**dict([(obj.id,obj.name)for obj in instances]))
            if instance_dict.has_key(floatingip.instance_id):
                return instance_dict[floatingip.instance_id]

def _getFloatingIpInfo(request,port_id,floatingips,floatingip_total):
    for floatingip in floatingips:
        if port_id==floatingip.port_id:
            return floatingip.floating_ip_address
    while True:
        if len(floatingips)==floatingip_total:
            return None
        floatingips_add,floatingip_total=api.network.tenant_floating_ip_list(request,marker=str(len(floatingips))+'_'+str(LIMIT))
        floatingips[len(floatingips):len(floatingips)]=floatingips_add
        for floatingip in floatingips:
            if port_id==floatingip.port_id:
                return floatingip.floating_ip_address   
                

            