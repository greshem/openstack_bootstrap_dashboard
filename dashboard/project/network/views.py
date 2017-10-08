# -*- coding: utf-8 -*-
from django.http.response import HttpResponse
from django.utils.translation import ugettext_lazy as _

from dashboard.views.base import HomePageView
import json
from dashboard import api
from horizon import exceptions
from dashboard.util.portUtil import getDeviceInfo,getFix,getFloatingIpInfo
import logging

LOG = logging.getLogger(__name__)
LIMIT = 10

class indexView(HomePageView):
    template_name = "network/networkManage.html"
    def get_data(self):
        return {}
def network_list(request):
    try:
        limit = request.GET.get('limit')
        offset = request.GET.get('offset')
        name = request.GET.get('name')
        if limit is None:
            limit=1000
        if offset is None:
            offset=0
        tenant_id = request.user.tenant_id
#        param={'router__external':False}
        param = {}
        if name:
            param['name'] = name
        networks, total = api.neutron.network_list_for_tenant(request, tenant_id, include_external=False, page=False, **param)
        result = {'total':total}
        rows = []
        for network in networks:
            subnet_id = None
            if len(network.subnets) > 0:
                subnet_id = network.subnets[0]['id']
            rows.append({'subnet_id':subnet_id, 'id':network.id, 'admin_state':network.admin_state, 'router_external':network.router__external, 'subnet':_get_subnet_info(network), 'name':network.name, 'status':network.status, 'created_at':network.created_at, 'updated_at':network.updated_at})
        result['rows'] = rows
    except Exception:
        networks = []
        msg = _('Network list can not be retrieved.')
        exceptions.handle(request, msg)
    return HttpResponse(json.dumps(result))

def _get_subnet_info(network):
    if network:
        result = ''
        for subnet in network.subnets:
            if result:
                result = result + u'<br />子网名称：' + subnet['name'] + u',&nbsp;版本：' + subnet['ipver_str'] + u',&nbsp;网络：' + subnet['cidr']
                if subnet['allocation_pools']:
                    result = result + u',&nbsp;网段：'
                ip = ''
                for ipstart_end in subnet['allocation_pools']:
                    if ip:
                        ip = ip + ',' + ipstart_end['start'] + '-' + ipstart_end['end']
                    else:
                        ip = ipstart_end['start'] + '-' + ipstart_end['end']
                result = result + ip
            else:
                result = u'子网名称：' + subnet['name'] + u',&nbsp;版本：' + subnet['ipver_str'] + u',&nbsp;网络：' + subnet['cidr']
                if subnet['allocation_pools']:
                    result = result + u',&nbsp;网段：'
                ip = ''
                for ipstart_end in subnet['allocation_pools']:
                    if ip:
                        ip = ip + ',' + ipstart_end['start'] + '-' + ipstart_end['end']
                    else:
                        ip = ipstart_end['start'] + '-' + ipstart_end['end']
                result = result + ip
            if subnet['gateway_ip']:
                result=result+u',&nbsp;网关：'+subnet['gateway_ip']
            DNS = None
            for dns in subnet['dns_nameservers']:
                if DNS:
                    DNS = DNS + ',' + dns
                else:
                    DNS = dns
            if DNS:
                result = result + ',&nbsp;DNS:' + DNS
            host_route = None
            for route in subnet['host_routes']:
                if host_route:
                    host_route = host_route + u',[网络：' + route['destination'] + u',下一跳：' + route['nexthop'] + ']'
                else:
                    host_route = u'[网络：' + route['destination'] + u',下一跳：' + route['nexthop'] + ']'
            if host_route:
                result = result + u',&nbsp;主机路由：' + host_route
            return result
        return None

def network_delete(request):
    try:
        network_ids = request.POST.get('network_ids')
        for network_id in network_ids.split(','):
            network = api.neutron.network_get(request, network_id,
                                          expand_subnet=False)
            for subnet_id in network.subnets:
                api.neutron.subnet_delete(request, subnet_id)
                LOG.debug('Deleted subnet %s', subnet_id)
            api.neutron.network_delete(request, network_id)
            LOG.debug('Deleted network %s successfully', network_id)
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse('success')

def network_update(request):
    try:
        post_data = request.POST
        params = {'admin_state_up': (post_data.get('admin_state') == 'UP'),
                      'name': post_data.get('name'), }
        
        api.neutron.network_update(request,
                                             post_data.get('network_id'),
                                             **params)
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse('success')

def network_create(request):
    try:
        network = _create_network(request)
        if not network:
            raise
        subnet = _create_subnet(request, network)
        if  not subnet:
            _delete_network(request, network)
    except Exception:
        _delete_network(request, network)
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse('success')

def _create_network(request):
    data = request.POST
    params = {'name': data.get('net_name'),
                      'admin_state_up': (data.get('admin_state') == 'UP'),
                      'shared': False}
    if api.neutron.is_port_profiles_supported():
        params['net_profile_id'] = data['net_profile_id']
    network = api.neutron.network_create(request, **params)
    return network

def _setup_subnet_parameters(params, data, is_create=True):
        """Setup subnet parameters

        This methods setups subnet parameters which are available
        in both create and update.
        """
        is_update = not is_create
        params['enable_dhcp'] = data.get('enable_dhcp')
        if data.get('allocation_pools'):
            pools = [dict(zip(['start', 'end'], pool.strip().split(',')))
                     for pool in data.get('allocation_pools').split('\n')
                     if pool.strip()]
            params['allocation_pools'] = pools
        if data.get('host_routes') or is_update:
            routes = [dict(zip(['destination', 'nexthop'],
                               route.strip().split(',')))
                      for route in data.get('host_routes').split('\n')
                      if route.strip()]
            params['host_routes'] = routes
        if data.get('dns_nameservers') or is_update:
            nameservers = [ns.strip()
                           for ns in data.get('dns_nameservers').split('\n')
                           if ns.strip()]
            params['dns_nameservers'] = nameservers


def _create_subnet(request, network):
    data = request.POST
    network_id = network.id
    params = {'network_id': network_id,
              'name': data.get('subnet_name')}
    if 'cidr' in data and data.get('cidr'):
        params['cidr'] = data['cidr']
    params['ip_version'] = 4
    params['tenant_id'] = request.user.tenant_id
    params['gateway_ip'] = data.get('gateway_ip')
    if 'subnetpool' in data and len(data.get('subnetpool')):
        params['subnetpool_id'] = data.get('subnetpool')
        if 'prefixlen' in data and len(data.get('prefixlen')):
            params['prefixlen'] = data.get('prefixlen')
    _setup_subnet_parameters(params, data)
    subnet = api.neutron.subnet_create(request, **params)
    return subnet

def _delete_network(request, network):
    if network:
        api.neutron.network_delete(request, network.id)   


def subnet_update(request):
    try:
        data=request.POST
        subnet_id=data.get('subnet_id')
        params={}
        params['gateway_ip'] = data.get('gateway_ip') if data.get('gateway_ip') else None
        params['name'] = data.get('subnet_name')
        _setup_subnet_parameters(params, data, is_create=False)
        api.neutron.subnet_update(request, subnet_id,**params)
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse('success')


def get_subnet(request):
#    {u'description': u'', u'enable_dhcp': True, u'network_id': u'617cb1bf-42e4-494f-93af-
# fceb53a81936', u'tenant_id': u'b8de93e20148470dbc45e802240c3d10', u'created_at': u'2016-09-27T03:
# 54:41', u'dns_nameservers': [], u'updated_at': u'2016-09-27T03:54:41', u'ipv6_ra_mode': None, 
# u'allocation_pools': [{u'start': u'10.0.0.1', u'end': u'10.0.0.254'}], u'gateway_ip': None, 
# u'ipv6_address_mode': None, u'ip_version': 4, u'host_routes': [{u'destination': u'192.168.0.0/24', 
# u'nexthop': u'10.0.0.1'}], u'cidr': u'10.0.0.0/24', 'ipver_str': 'IPv4', u'id': u'6ba21bc0-baa4-43ab-9419-
# cb78f4efbda5', u'subnetpool_id': None, u'name': u'subnet001'}
    try:
        subnet_id = request.GET.get('subnet_id')
        subnet = api.neutron.subnet_get(request, subnet_id)
        if not subnet:
            raise
        result = {'gateway_ip':subnet.gateway_ip,'name':subnet.name, 'cidr':subnet.cidr, 'enable_dhcp':subnet.enable_dhcp, 'allocation_pools':_get_allocation_pools(subnet), 'dns_nameservers':_get_dns_nameservers(subnet), 'host_routes':_get_host_routes(subnet)}
    except Exception:
        result={}
        msg = _('Network list can not be retrieved.')
        exceptions.handle(request, msg)
    return HttpResponse(json.dumps(result))

def _get_allocation_pools(subnet):
    if subnet:
        result=''
        for pool in subnet.allocation_pools:
            if result:
                result=result+'\n'+pool['start']+','+pool['end']
            else:
                result=pool['start']+','+pool['end']
        return result
    return None

def _get_dns_nameservers(subnet):
    if subnet:
        result=''
        for dns in subnet.dns_nameservers:
            if result:
                result=result+'\n'+dns
            else:
                result=dns
        return result
    return None

def _get_host_routes(subnet):
    if subnet:
        result=''
        for host_route in subnet.host_routes:
            if result:
                result=result+'\n'+host_route['destination']+','+host_route['nexthop']
            else:
                result=host_route['destination']+','+host_route['nexthop']
        return result
    return None

class portView(HomePageView):
    template_name = "network/portManage.html"
    def get_data(self):
        return {'network_id':self.request.GET.get('network_id'),'net_name':self.request.GET.get('net_name')}

def port_list(request):
    try:
        network_id=request.GET.get('network_id')
        limit=request.GET.get('limit')
        offset=request.GET.get('offset')
        params={}
        if request.GET.has_key('device_owner'):
            params['device_owner']=request.GET.get('device_owner')
        floating_ip_ports,total=api.neutron.port_list(request,marker=str(offset)+'_'+str(limit),page=True,network_id=network_id,**params)
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
        params['name'] = data.get('network_port_name')
        params['admin_state_up'] = (data.get('admin_state') == 'UP')
        api.neutron.port_update(request, port_id,**params)
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse('success')
