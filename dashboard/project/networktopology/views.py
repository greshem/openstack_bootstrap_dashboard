# -*- coding: utf-8 -*-


import json
import six
from django.conf import settings
from django.http import HttpResponse  # noqa
from django.utils.translation import pgettext_lazy
from django.views.generic import View  # noqa
from horizon.utils.lazy_encoder import LazyTranslationEncoder

from dashboard import api



from dashboard.views.base import HomePageView



import logging

LOG = logging.getLogger(__name__)
LIMIT = 10

class indexView(HomePageView):
    template_name = "networktopology/networktopologyManage.html"
    def get_data(self):
        return {}

def get_data_json(request):
    return HttpResponse({'networks':[{'subnets':[{'cidr':"2.2.2.0/24",'id':"efbca8ba-489a-4170-a52c-d107f6b9c3ff",'url':"/dashboard/project/networks/subnets/efbca8ba-489a-4170-a52c-d107f6b9c3ff/detail"}],'id':"0ebe2af2-9d81-4964-ae0d-bbe918620839",'name':"public",'original_status':"ACTIVE",'router:external:truestatus':"正常"}]})


INSTANCE_STATUS_DISPLAY_CHOICES = (
    ("deleted", pgettext_lazy("Current status of an Instance", u"Deleted")),
    ("active", pgettext_lazy("Current status of an Instance", u"Active")),
    ("shutoff", pgettext_lazy("Current status of an Instance", u"Shutoff")),
    ("suspended", pgettext_lazy("Current status of an Instance",
                                u"Suspended")),
    ("paused", pgettext_lazy("Current status of an Instance", u"Paused")),
    ("error", pgettext_lazy("Current status of an Instance", u"Error")),
    ("resize", pgettext_lazy("Current status of an Instance",
                             u"Resize/Migrate")),
    ("verify_resize", pgettext_lazy("Current status of an Instance",
                                    u"Confirm or Revert Resize/Migrate")),
    ("revert_resize", pgettext_lazy(
        "Current status of an Instance", u"Revert Resize/Migrate")),
    ("reboot", pgettext_lazy("Current status of an Instance", u"Reboot")),
    ("hard_reboot", pgettext_lazy("Current status of an Instance",
                                  u"Hard Reboot")),
    ("password", pgettext_lazy("Current status of an Instance", u"Password")),
    ("rebuild", pgettext_lazy("Current status of an Instance", u"Rebuild")),
    ("migrating", pgettext_lazy("Current status of an Instance",
                                u"Migrating")),
    ("build", pgettext_lazy("Current status of an Instance", u"Build")),
    ("rescue", pgettext_lazy("Current status of an Instance", u"Rescue")),
    ("soft-delete", pgettext_lazy("Current status of an Instance",
                                  u"Soft Deleted")),
    ("shelved", pgettext_lazy("Current status of an Instance", u"Shelved")),
    ("shelved_offloaded", pgettext_lazy("Current status of an Instance",
                                        u"Shelved Offloaded")),
    # these vm states are used when generating CSV usage summary
    ("building", pgettext_lazy("Current status of an Instance", u"Building")),
    ("stopped", pgettext_lazy("Current status of an Instance", u"Stopped")),
    ("rescued", pgettext_lazy("Current status of an Instance", u"Rescued")),
    ("resized", pgettext_lazy("Current status of an Instance", u"Resized")),
)

NETWORK_DISPLAY_CHOICES = (
    ("up", pgettext_lazy("Admin state of a Network", u"UP")),
    ("down", pgettext_lazy("Admin state of a Network", u"DOWN")),
)

NETWORK_STATUS_DISPLAY_CHOICES = (
    ("active", pgettext_lazy("Current status of a Network", u"Active")),
    ("build", pgettext_lazy("Current status of a Network", u"Build")),
    ("down", pgettext_lazy("Current status of a Network", u"Down")),
    ("error", pgettext_lazy("Current status of a Network", u"Error")),
)

PORT_STATUS_DISPLAY_CHOICES = (
    ("ACTIVE", pgettext_lazy("current status of port", u"Active")),
    ("BUILD", pgettext_lazy("current status of port", u"Build")),
    ("DOWN", pgettext_lazy("current status of port", u"Down")),
    ("ERROR", pgettext_lazy("current status of port", u"Error")),
    ("N/A", pgettext_lazy("current status of port", u"N/A")),
)

PORT_DISPLAY_CHOICES = (
    ("UP", pgettext_lazy("Admin state of a Port", u"UP")),
    ("DOWN", pgettext_lazy("Admin state of a Port", u"DOWN")),
)

ROUTER_STATUS_DISPLAY_CHOICES = (
    ("active", pgettext_lazy("current status of router", u"Active")),
    ("error", pgettext_lazy("current status of router", u"Error")),
)

ROUTE_ADMIN_STATE_DISPLAY_CHOICES = (
    ("up", pgettext_lazy("Admin state of a Router", u"UP")),
    ("down", pgettext_lazy("Admin state of a Router", u"DOWN")),
)

class TranslationHelper(object):
    """Helper class to provide the translations of instances, networks,
    routers and ports from other parts of the code to the network topology
    """
    def __init__(self):
        # turn translation tuples into dicts for easy access
        self.instance = dict(INSTANCE_STATUS_DISPLAY_CHOICES)
        self.network = dict(NETWORK_STATUS_DISPLAY_CHOICES)
        self.network.update(dict(NETWORK_DISPLAY_CHOICES))
        self.router = dict(ROUTE_ADMIN_STATE_DISPLAY_CHOICES)
        self.router.update(dict(ROUTER_STATUS_DISPLAY_CHOICES))
        self.port = dict(PORT_DISPLAY_CHOICES)
        self.port.update(dict(PORT_STATUS_DISPLAY_CHOICES))
        # and turn all the keys into Uppercase for simple access
        self.instance = {k.upper(): v for k, v in six.iteritems(self.instance)}
        self.network = {k.upper(): v for k, v in six.iteritems(self.network)}
        self.router = {k.upper(): v for k, v in six.iteritems(self.router)}
        self.port = {k.upper(): v for k, v in six.iteritems(self.port)}



class JSONView(View):
    trans = TranslationHelper()
    @property
    def is_router_enabled(self):
        network_config = getattr(settings, 'OPENSTACK_NEUTRON_NETWORK', {})
        return network_config.get('enable_router', True)
    def add_resource_url(self, view, resources):
        tenant_id = self.request.user.tenant_id
        for resource in resources:
            if (resource.get('tenant_id')
                    and tenant_id != resource.get('tenant_id')):
                continue
    def _check_router_external_port(self, ports, router_id, network_id):
        for port in ports:
            if (port['network_id'] == network_id
                    and port['device_id'] == router_id):
                return True
        return False
    def _get_servers(self, request):
        # Get nova data
        search_opts = {'paginate': True,'limit':100}
        try:
            servers = api.nova.server_list(request,search_opts=search_opts)
            data = []
            for server in servers:            
                server_data = {'name': server.name,
                               'status': self.trans.instance[server.status],
                               'original_status': server.status,
                               'task': getattr(server, 'OS-EXT-STS:task_state'),
                               'id': server.id}
                data.append(server_data)
        except Exception:
            servers = []
        #self.add_resource_url('horizon:project:instances:detail', data)
        return data
    def _get_networks(self, request):
        # Get neutron data
        # if we didn't specify tenant_id, all networks shown as admin user.
        # so it is need to specify the networks. However there is no need to
        # specify tenant_id for subnet. The subnet which belongs to the public
        # network is needed to draw subnet information on public network.
        try:
            neutron_networks,total = api.neutron.network_list_for_tenant(
                request,
                request.user.tenant_id)
        
            networks = []
            for network in neutron_networks:
                subnet_id = None
                subnet_cidr= None
                network_name = network.name
                network_id = network.id
                if len(network.subnets) > 0:
                    subnet_id = network.subnets[0]['id']
                    subnet_cidr = network.subnets[0]['cidr']
                network_status = self.trans.network[network.status]
                orign_status = network.status
                network_external =  network['router:external'];
                obj = {'name': network_name,
                       'id': network_id,
                       'subnets': [{'id': subnet_id,
                                    'cidr': subnet_cidr}],
                       'status': network_status,
                       'original_status':orign_status,
                       'router:external': network_external}
#               self.add_resource_url('horizon:project:networks:subnets:detail',
#                                     obj['subnets'])
                networks.append(obj)
    
            # Add public networks to the networks list
            if self.is_router_enabled:
                neutron_public_networks,total = api.neutron.network_list(
                    request,
                    **{'router:external': True})
                my_network_ids = [net['id'] for net in networks]
                for publicnet in neutron_public_networks:
                    if publicnet.id in my_network_ids:
                        continue
                    subnets = []
                    for subnet in publicnet.subnets:
                        snet = {'id': subnet.id,
                                'cidr': subnet.cidr}
#                    self.add_resource_url(
#                          'horizon:project:networks:subnets:detail', snet)
                        subnets.append(snet)
                    networks.append({
                        'name': publicnet.name_or_id,
                        'id': publicnet.id,
                        'subnets': subnets,
                        'status': self.trans.network[publicnet.status],
                        'original_status': publicnet.status,
                        'router:external': publicnet['router:external']})
        except Exception:
            neutron_networks = []
        return sorted(networks,
                      key=lambda x: x.get('router:external'),
                      reverse=True)
    def _get_routers(self, request):
        if not self.is_router_enabled:
            return []
        try:
            neutron_routers,total = api.neutron.router_list(
                request,
                tenant_id=request.user.tenant_id)
            routers = [{'id': router.id,
                    'name': router.name_or_id,
                    'status': self.trans.router[router.status],
                    'original_status': router.status,
                    'external_gateway_info': router.external_gateway_info}
                   for router in neutron_routers]
        except Exception:
            neutron_routers = []
        return routers
    def _get_ports(self, request):
        try:
            neutron_ports,total = api.neutron.port_list(request,tenant_id=request.user.tenant_id)
            ports = []
            for port in neutron_ports:
                #print port
                if port.device_owner != 'network:router_ha_interface':
                    ports.append({'id': port.id,
                          'network_id': port.network_id,
                          'device_id': port.device_id,
                          'fixed_ips': port.fixed_ips,
                          'device_owner': port.device_owner,
                          'status': self.trans.port[port.status],
                          'original_status': port.status})
        except Exception:
            neutron_ports = []
        return ports
    def _prepare_gateway_ports(self, routers, ports):
        # user can't see port on external network. so we are
        # adding fake port based on router information
        for router in routers:
            external_gateway_info = router.get('external_gateway_info')
            if not external_gateway_info:
                continue
            external_network = external_gateway_info.get(
                'network_id')
            if not external_network:
                continue
            if self._check_router_external_port(ports,
                                                router['id'],
                                                external_network):
                continue
            fake_port = {'id': 'gateway%s' % external_network,
                         'network_id': external_network,
                         'device_id': router['id'],
                         'fixed_ips': []}
            ports.append(fake_port)
    def get(self, request, *args, **kwargs):
        data = {'servers': self._get_servers(request),
                'networks': self._get_networks(request),
                'ports': self._get_ports(request),
                'routers': self._get_routers(request)}
        self._prepare_gateway_ports(data['routers'], data['ports'])
        json_string = json.dumps(data, cls=LazyTranslationEncoder,
                                 ensure_ascii=False)
        return HttpResponse(json_string, content_type='text/json')



