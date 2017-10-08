# -*- coding: utf-8 -*-
from django.http.response import HttpResponse
from dashboard.views.base import HomePageView
import json
from dashboard import api
from horizon import exceptions
from dashboard.util import billingUtil
from dashboard.util.portUtil import getDeviceInfo,getFix,getFloatingIpInfo
import logging

LOG = logging.getLogger(__name__)
LIMIT = 10

class indexView(HomePageView):
    template_name = "router/routerManage.html"
    def get_data(self):
        return {}

class portView(HomePageView):
    template_name = "router/portManage.html"
    def get_data(self):
        return {'router_id':self.request.GET.get('router_id'),'router_name':self.request.GET.get('router_name')}

class routeView(HomePageView):
    template_name = "router/routeManage.html"
    def get_data(self):
        return {'router_id':self.request.GET.get('router_id'),'router_name':self.request.GET.get('router_name')}


def router_list(request):
    try:
        name = request.GET.get('name')
        param = {}
        if name:
            param['name'] = name
        tenant_id = request.user.tenant_id
        routers,total = api.neutron.router_list(request,
                                          tenant_id=tenant_id,page=False,**param)
        search_opts = {'router:external': True}
        ext_nets = api.neutron.network_list(request,
                                            **search_opts)[0]
        ext_net_dict = dict([(n['id'], n.name_or_id)
                                   for n in ext_nets])
        result = {'total':total}
        rows = []
        for router in routers:
            rows.append({'id':router.id,'name':router.name_or_id,'status':router.status,'admin_state':router.admin_state,'ext_net':_get_ext_net(router, ext_net_dict)})
        result['rows'] = rows
    except Exception:
        result = []
        msg = _('Network list can not be retrieved.')
        exceptions.handle(request, msg)
    return HttpResponse(json.dumps(result))

def get_ext_net(request):
    try:
        search_opts = {'router:external': True}
        ext_nets = api.neutron.network_list(request,
                                            **search_opts)[0]
        result = [{'id':n['id'], 'name':n.name_or_id}
                                   for n in ext_nets]
    except Exception:
        result = []
        msg = _('Network list can not be retrieved.')
        exceptions.handle(request, msg)
    return HttpResponse(json.dumps(result))


def _get_ext_net(router,ext_net_dict):
    if router:
        gateway_info = router.external_gateway_info
        if gateway_info:
            ext_net_id = gateway_info['network_id']
            if ext_net_id in ext_net_dict:
                return ext_net_dict[ext_net_id]
    return None

def router_create(request):
    try:
        data=request.POST
        params = {'name': data.get('name')}
        if 'admin_state' in data and data.get('admin_state'):
            params['admin_state_up'] = data.get('admin_state')=='UP'
        router = api.neutron.router_create(request, **params)
        if not router:
            raise
        if ('router_ext_net_id' in data and
                    data.get('router_ext_net_id')):
            api.neutron.router_add_gateway(request,
                                           router.id,
                                           data.get('router_ext_net_id'))
    except Exception:
        _router_delete(router)
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse('success')

def _router_delete(request,router):
    if router:
        api.neutron.router_delete(request, router.id)

def router_delete(request):
    router_ids = request.POST.get('router_ids')
    try:
        for router_id in router_ids.split(','):
            search_opts = {'device_owner': 'network:router_interface',
                           'device_id': router_id}
            ports = api.neutron.port_list(request, **search_opts)[0]
            for port in ports:
                api.neutron.router_remove_interface(request, router_id,
                                                    port_id=port.id)
            api.neutron.router_delete(request, router_id)
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse('success')

def router_update(request):
    try:
        router_id=request.POST.get('router_id')
        name=request.POST.get("name")
        admin_state=request.POST.get("admin_state")
        admin_state_up=admin_state=='UP'
        params={'name':name,'admin_state_up':admin_state_up}
        api.neutron.router_update(request, router_id,**params)
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse('success')

def getPriceDiscount(request):
    try:
        account = request.session.get('account')
        billingItems = ('router_1',)
        result=billingUtil.getPriceDiscount(request.GET.get('region_id'), account, billingItems)
    except Exception:
        result = []
        exceptions.handle(request, _("Unable to retrieve images."))
    return HttpResponse(json.dumps(result))

def port_list(request):
    try:
        router_id=request.GET.get('router_id')
        limit=request.GET.get('limit')
        offset=request.GET.get('offset')
        params={}
        if request.GET.has_key('device_owner'):
            params['device_owner']=request.GET.get('device_owner')
        floating_ip_ports,total=api.neutron.port_list(request,marker=str(offset)+'_'+str(limit),page=True,device_id=router_id,**params)
        result = {'total':total}
        rows=[]
        floatingips,floatingip_total=api.network.tenant_floating_ip_list(request,marker='0_'+str(LIMIT))
#        floatingip_dict=dict([(obj.floating_ip_address, obj.port_id) for obj in floatingips])
        instances,instance_total = api.nova.server_list(
            request,
            search_opts={'limit':LIMIT,'marker':0,'paginate': True})
        instance_dict=dict([(obj.id,obj.name)for obj in instances])
        for floating_ip_port in floating_ip_ports:
            rows.append({'id':floating_ip_port.id,'admin_state':floating_ip_port.admin_state,'status':floating_ip_port.status,'device_owner':floating_ip_port.device_owner,'fixed_ip_address':getFix(floating_ip_port),'device_name':getDeviceInfo(request,floating_ip_port,instance_dict,instance_total),'device_id':floating_ip_port.device_id,'id':floating_ip_port.id,'name':floating_ip_port.name_or_id,'floating_ip_address':getFloatingIpInfo(request,floating_ip_port.id,floatingips,floatingip_total)})
        result['rows']=rows
    except Exception:
        result = []
        exceptions.handle(request, _("Unable to retrieve images."))
    return HttpResponse(json.dumps(result))

def port_update(request):
    try:
        data=request.POST
        port_id=data.get('port_id')
        params={}
        params['name'] = data.get('router_port_name')
        params['admin_state_up'] = (data.get('admin_state') == 'UP')
        api.neutron.port_update(request, port_id,**params)
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse('success')

def port_delete(request):
    try:
        api.neutron.router_remove_interface(request,request.GET.get('router_id'),port_id=request.GET.get('port_id'))
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse('success')   

def route_list(request):
    try:
        nexthop=request.GET.get('nexthop')
        routes=api.neutron.router_static_route_list(request, request.GET.get('router_id'))
        result=[]
        if nexthop:
            for route in routes:
                if route.nexthop == nexthop:
                    result.append({'id':route.id,'destination':route.destination,'nexthop':route.nexthop})
        else:
            for route in routes:
                result.append({'id':route.id,'destination':route.destination,'nexthop':route.nexthop})
    except Exception:
        result = []
        msg = _('Network list can not be retrieved.')
        exceptions.handle(request, msg)
    return HttpResponse(json.dumps({'rows':result})) 



def route_delete(request):
    router_route_ids = request.POST.get('router_route_ids')
    router_id=request.POST.get('router_id')
    try:
        api.neutron.router_static_route_remove(request, router_id, [router_route_id for router_route_id in router_route_ids.split(',')])
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse('success')

def route_create(request):
    try:
        data=request.POST
        api.neutron.router_static_route_add(request, data.get('router_id'), {'destination':data.get('cidr'),'nexthop':data.get('nexthop')})
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse('success')

