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
import console
import logging
import threading
import time
from django.utils.translation import ugettext_lazy as _
from dashboard.util.cacheUtil import add_cache
from dashboard.util.cacheUtil import get_cache
from dashboard.util.pagingUtil import paginate
from django.conf import settings


LOG = logging.getLogger(__name__)

    
def instance_list(request):
    search_opts = {}
    for item in request.GET.keys():
        search_opts[item] = request.GET.get(item)
    result = get_cache("instance_list")
    
    if 'reload' in search_opts or not result:
        result = _get_instance_list(request)
        add_cache("instance_list", result, settings.PAGE_CACHE_TIMEOUT)
    else:
        result = get_cache("instance_list")
        
    result = paginate(result, search_opts)
    return HttpResponse(json.dumps(result))


def _get_instance_list(request, search_opts={}):
    # Gather our instances
    try:
        instances = api.nova.server_list( request, search_opts=search_opts)
        assert (not isinstance(instances, tuple));
        if isinstance(instances, tuple):
            LOG.error("BUG_of_total_keven ");

    except Exception as e:
        instances = []
        LOG.exception( 'Unable to retrieve instances.');
        exceptions.handle(request, _('Unable to retrieve instances.'))

    result = {'total':len(instances)}
    rows = []
    if instances:
        try:
            api.network.servers_update_addresses(request, instances)
        except Exception:
            LOG.exceptions( 'Unable to update instances.');
            exceptions.handle(
                request,
                message=_('Unable to retrieve IP addresses from Neutron.'),
                ignore=True)

        # Gather our flavors
        try:
            flavors = api.nova.flavor_list(request)
            assert(not isinstance(flavors , tuple) );
        except Exception:
            LOG.exceptions( 'Unable to get  flavor_list ');
            flavors = []
            exceptions.handle(request, ignore=True)
  
  
        full_flavors = OrderedDict([(str(flavor.id), flavor)
                                   for flavor in flavors])


        # Loop through instances to get flavor info.
        for instance in instances:
            network = get_network(instance.addresses)
            try:
                flavor_id = instance.flavor["id"]
                if flavor_id in full_flavors:
                    instance.full_flavor = full_flavors[flavor_id]
                else:
                    instance.full_flavor = api.nova.flavor_get(
                        request, flavor_id)
            except Exception:
                msg = ('Unable to retrieve flavor "%s" for instance "%s".'
                       % (flavor_id, instance.id))
                LOG.exception(msg)
            
            rows.append({
            'id':instance.id,
            'name':instance.name,
            'memory_mb':instance.full_flavor.ram,
            'vcpus':instance.full_flavor.vcpus,
            'root_gb':instance.full_flavor.disk,
            'status':instance.status,
            'image_name':instance.image_name,
            'created':instance.created,
            'power_state':instance.__getattribute__('OS-EXT-STS:power_state'),
            'network':network
            })

    result['rows'] = rows
    #return HttpResponse(json.dumps(result))
    return result


def instance_list_attach(request):
    search_opts = {}
    try:
        instances = api.nova.server_list(
            request,
            search_opts=search_opts)
    except Exception:
        instances = []
        total = 0
        LOG.execption( 'Unable to retrieve instances.');
#        exceptions.handle(request,
#                          _('Unable to retrieve instances.'))
    # Gather our flavors
    try:
        flavors = api.nova.flavor_list(request)
    except Exception:
        flavors = []
        exceptions.handle(request, ignore=True)
    
    
    full_flavors = OrderedDict([(str(flavor.id), flavor)
                               for flavor in flavors])
    result = {'total':len(instances)}
    rows = []
    if instances:
        for instance in instances:
            try:
                flavor_id = instance.flavor["id"]
                if flavor_id in full_flavors:
                    instance.full_flavor = full_flavors[flavor_id]
                else:
                    instance.full_flavor = api.nova.flavor_get(
                        request, flavor_id)
            except Exception:
                msg = ('Unable to retrieve flavor "%s" for instance "%s".'
                       % (flavor_id, instance.id))
                LOG.info(msg)
            
            rows.append({
            'id':instance.id,
            'name':instance.name,
            'memory_mb':instance.full_flavor.ram,
            'vcpus':instance.full_flavor.vcpus,
            'root_gb':instance.full_flavor.disk,
            'status':instance.status,
            'created':instance.created,
            'power_state':instance.__getattribute__('OS-EXT-STS:power_state'),
            })
    result['rows'] = rows
    return HttpResponse(json.dumps(result))


def get_network(address):
    result = ''
    if address:
        for net_name, subnet in address.items():
            for net in subnet:
                if net['OS-EXT-IPS:type'] == 'fixed':
                    ip = u'内网：' + net['addr']
                    for net1 in subnet:
                        if net1['OS-EXT-IPS-MAC:mac_addr'] == net['OS-EXT-IPS-MAC:mac_addr'] and net1['OS-EXT-IPS:type'] == 'floating':
                            ip = ip + u"，外网：" + net1['addr']
                
                    result = result + '</br>' + ip if result else ip
    return result

    


class indexView(HomePageView):
    template_name = "instance/ECloudmanage.html"

#    def get(self, request, *args, **kwargs):
        # if request.session.get('account',default=None) is None:
        #     return HttpResponseRedirect(settings.HORIZON_URL+'/auth/logout')
#        from dashboard.project.views1 import BillDetailsView
#        from django.core.urlresolvers import reverse
#        return HttpResponseRedirect(reverse('bill_details',args=args,kwargs=kwargs))

    def get_data(self):
        return {}


def updateInstance(request):
    post_data = request.POST
    instance_id = post_data.get('instance_id')
    name = post_data.get('name')
    try:
        api.nova.server_update(request,
                                       instance_id,
                                       name)
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse('success')

def startInstance(request):
    instance_id = request.GET.get('instance_id')
    try:
        api.nova.server_start(request,
                                       instance_id)
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse('success')

def stopInstance(request):
    instance_id = request.GET.get('instance_id')
    try:
        api.nova.server_stop(request,
                                       instance_id)
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse('success')

def rebootInstance(request):
    instance_id = request.GET.get('instance_id')
    try:
        api.nova.server_reboot(request,
                                       instance_id)
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse('success')

def deleteInstance(request):
    instance_ids = request.POST.get('instance_ids')
    try:
        for instance_id in instance_ids.split(','):
            api.nova.server_delete(request,
                                           instance_id)
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse('success')

def getImages(request):
    try:
        images = api.glance.image_list_detailed(request,paginate=False,limit=1000)
        assert(not isinstance(images,   tuple));
        result={}
        for image in images:
            if image.status=='active':
                image_dict={'id':image.id,'name':image.name,'size':int(image.size/(1024*1024))}
            os_type=image.properties['os_distro'] if image.properties and image.properties.has_key('os_distro') else 'other'
            if image.properties and image.properties.has_key('image_type') and image.properties['image_type']=='snapshot':
                os_type='snapshot'
            if result.has_key(os_type):
                result[os_type].append(image_dict)
            else:
                result[os_type]=[image_dict]
#        aa = {u'status': u'active', u'virtual_size': None, u'name': u'snapshot_centos', u'deleted': False, u'container_format': u'bare', u'created_at': u'2016-09-02T03:35:43.000000', u'disk_format': u'qcow2', u'updated_at': u'2016-09-02T03:36:23.000000', u'properties': {u'instance_uuid': u'5c09388e-b384-45d1-9fb6-5232840e21a6', u'image_location': u'snapshot', u'image_state': u'available', u'user_id': u'6944c1de6f96421b8d182d05702a37e7', u'os_distro': u'CentOS', u'image_type': u'snapshot', u'ramdisk_id': None, u'os_version': u'CentOS6.5_x64', u'kernel_id': None, u'architecture': u'x86_64', u'base_image_ref': u'3c26f6ba-d224-4c0f-b6ca-d69ce0b9ee01', u'owner_id': u'b8de93e20148470dbc45e802240c3d10'}, u'owner': u'b8de93e20148470dbc45e802240c3d10', u'protected': False, u'min_ram': 0, u'checksum': u'fbc2f3cab6e896b7ffa43efd7d438223', u'min_disk': 40, u'is_public': False, u'deleted_at': None, u'id': u'd46619e2-ed8f-4d94-864b-3ad893c728fa', u'size': 963575808}
    except Exception:
        LOG.exception("getImages error ");
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse(json.dumps(result))

def getRegions(request):
    try:
        regions = api.keystone.list_regions(request)
        result=[]
        for region in regions:
            result.append({'id':region.id,'description':region.description})
    except Exception:
        LOG.exception("getRegions error ");
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
#    {u'parent_region_id': None, u'id': u'RegionOne', u'links': {u'self': u'http://control:35357/v3/regions/RegionOne'}, u'description': u''}
    return HttpResponse(json.dumps(result))

def getPriceDiscount(request):
    try:
        region_id = 'RegionOne'
        #    region_id=request.GET.get('region_id')
        account = request.session.get('account')
        billingItems = ('cpu_1_core', 'memory_1024_M')
        #    result={'cpu_1_core':{'price':0.23,'discount_ratio':0.95}}.
        result=billingUtil.getPriceDiscount(region_id, account, billingItems)
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse(json.dumps(result))

def getNetworks(request):
    try:
        result=[]
        nets = api.neutron.network_list(request)[0]
        if nets:
            for net in nets:
                if net.status=='ACTIVE' and net.router__external==False:   
                    result.append({'name':net.name,'id':net.id})
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse(json.dumps(result))

def _get_flavor_id(request, vcpus=1, ram=1024, disk=1, ephemeral=0, swap=0):
    flavor_id = None
    flavor_list = api.nova.flavor_list(request)
    for flavor in flavor_list:
        if flavor.vcpus == vcpus \
            and flavor.ram == ram \
            and flavor.disk == disk \
            and flavor.ephemeral == ephemeral \
            and flavor.swap == swap \
            and flavor.rxtx_factor == 1.0:
            flavor_id = flavor.id
            break
    
    if not flavor_id:
        flavor_name = "m1." + str(vcpus) + "." + str(ram) + "." + str(disk) + "." + str(ephemeral) + "." + str(swap)
        flavor_new = api.nova.flavor_create(request, flavor_name, ram, vcpus, disk, 'auto', ephemeral, swap)
        if flavor_new:
            flavor_id = flavor_new.id
    return flavor_id

def instance_flavor_create(request):
    try:
        post_data = request.POST
        mem = int(post_data.get('memory'))*1024
        vcpus = int(post_data.get('vcpus'))
        disk = int(post_data.get('disk'))
        ephemeral = int(post_data.get('ephemeral'))
        swap = int(post_data.get('swap'))*1024

        flavor_id = _get_flavor_id(request, vcpus, mem, disk, ephemeral, swap)
        if not flavor_id:
            return HttpResponse('create flavor failure')
        else:
            return HttpResponse('success')
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')

def instance_create(request):
    try:
        post_data = request.POST
        name = post_data.get('name')
        image_id = post_data.get('image_id')
        memory_mb = int(post_data.get('memory'))*1024
        vcpus = int(post_data.get('vcpus'))
        root_gb = int(post_data.get('disk'))
        ephemeral = int(post_data.get('ephemeral'))
        swap = int(post_data.get('swap'))*1024
        nics = [{'net-id':post_data.get('netid')}]
        admin_pass = post_data.get('root_pass')
        meta={'admin_pass':admin_pass,'hostname':name}
        instance_count=post_data.get('instance_count')
        
        #get flavors
        flavor_id = _get_flavor_id(request, vcpus, memory_mb, root_gb, ephemeral, swap)
        if not flavor_id:
            return HttpResponse('create flavor failure')
        server = api.nova.server_create(request,
                                       name,
                                       image_id,
                                       flavor_id,
                                       memory_mb=memory_mb,
                                       vcpus=vcpus,
                                       root_gb=root_gb,
                                       nics=nics,
                                       instance_count=instance_count,
                                       admin_pass=admin_pass,
                                       meta=meta)  
        if server:
            return HttpResponse('success')
        else:
            return HttpResponse('error')
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')

def availability_zone_list(request):
#    {u'zoneState': {u'available': True}, u'hosts': None, u'zoneName': u'nova'}
    try:
        result=[]
        zones=api.nova.availability_zone_list(request)
        if zones:
            for zone in zones:
                result.append({'zoneName':zone.zoneName,'zoneState':zone.zoneState})
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse(json.dumps(result))
    

def get_console(request):
    try:
        instance_id=request.POST.get('instance_id')
        instance_name=request.POST.get('instance_name')
        result={}
        con_type, console_url=console.get_console(request, instance_id, instance_name)
        result['con_type']=con_type
        result['console_url']=console_url
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse(json.dumps(result))

def resize(request):
    instance_id = request.POST.get('instance_id')
    config={
    'memory_mb':int(request.POST.get('memory_mb'))*1024,
    'vcpus':int(request.POST.get('vcpus')),
    'root_gb':int(request.POST.get('root_gb'))
    }
    try:
        instance=api.nova.server_get(request, instance_id)
        api.nova.server_resize(request, instance_id,'2' if instance.flavor["id"]=='1' else '1', disk_config=None,**config)
        t=threading.Thread(target=confirm_resize,args=(request,instance_id))
        t.start()
        time.sleep(2)
#        api.nova.server_confirm_resize(request, instance_id)
    except Exception:
        exceptions.handle(request, ignore=True)
        return HttpResponse('error')
    return HttpResponse('success')
def confirm_resize(request,instance_id):
    instance=api.nova.server_get(request, instance_id)
    count=1
    while True:
        if count>100:
            return
        if instance.status=='VERIFY_RESIZE':
            api.nova.server_confirm_resize(request, instance_id)
            return
        else:
            time.sleep(2)
            instance=api.nova.server_get(request, instance_id)
            count=count+1

def getInstanceSecurityGroup(request):
    try:
        instance_id=request.GET.get('instance_id')
        securitygroups,total=api.network.server_security_groups(request, instance_id);
        result=[]
        for securitygroup in securitygroups:
            result.append({'id':securitygroup.id,'name':securitygroup.name})
    except Exception:
        result = []
        exceptions.handle(request,
                          _('Unable to retrieve security groups.'))
    return HttpResponse(json.dumps(result))

def updateInstanceSecurityGroup(request):
    try:
        instance_id=request.POST.get('instance_id')
        sg_ids=request.POST.get('sg_ids')
        sg_ids=sg_ids.split(',')
        api.network.server_update_security_groups(request, instance_id, sg_ids)
    except Exception:
        HttpResponse('error')
        exceptions.handle(request,
                          _('Unable to retrieve security groups.'))
    return HttpResponse('success')

def disassociate(request):
    try:
        instance_id=request.GET.get('instance_id')
        targets = api.network.floating_ip_target_list_by_instance(
                request, instance_id)

        target_ids = [t.split('_')[0] for t in targets]
        floatingips=api.network.tenant_floating_ip_list(request,marker='0_1000')
        fips = [fip for fip in floatingips[0] if fip.port_id in target_ids]
        
        if fips:
            fip = fips.pop()
            api.network.floating_ip_disassociate(request, fip.id)
    except Exception:
        return HttpResponse('error')
        exceptions.handle(request,
                          _('Unable to retrieve security groups.'))
    return HttpResponse('success')


def getInstancePorts(request):
    try:
        instance_id=request.GET.get('instance_id')
        targets = api.network.floating_ip_target_list_by_instance(
                request, instance_id)
        result=[]
        for target in targets:
            result.append({'id':target.split('_')[0],'ip':target.split('_')[1]})
    except Exception:
        result=[]
        exceptions.handle(request,
                          _('Unable to retrieve security groups.'))
    return HttpResponse(json.dumps(result))

def associate(request):
    try:
        pool_id=request.POST.get('pool_id')
        port_id_ip=request.POST.get('port_id_ip')
        floatingip_id=request.POST.get('floatingip_id')
        if pool_id:
            floatingip=api.network.tenant_floating_ip_allocate(request, pool_id)
            floatingip_id=floatingip.id
        api.network.floating_ip_associate(request, floatingip_id,port_id_ip)
    except Exception:
        return HttpResponse('error')
        exceptions.handle(request,
                          _('Unable to retrieve security groups.'))
    return HttpResponse('success')

def create_snapshot(request):
    try:
        instance_id=request.POST.get('instance_id')
        snapshot_name=request.POST.get('snapshot_name')
        api.nova.snapshot_create(request, instance_id, snapshot_name)
    except Exception:
        return HttpResponse('error')
        exceptions.handle(request,
                          _('Unable to retrieve security groups.'))
    return HttpResponse('success')

def get_instance(request):
    try:
        instance_id=request.GET.get('instance_id')
        instance = api.nova.server_get(request, instance_id)
        rows = []
        rows.append({
            'id':instance.id,
            'name':instance.name,
            'memory_mb':instance.memory_mb,
            'vcpus':instance.vcpus,
            'root_gb':instance.root_gb,
            'status':instance.status,
            'image_name':instance.image_name,
            'created':instance.created,
            'power_state':instance.__getattribute__('OS-EXT-STS:power_state')
            })
    except Exception:
        return HttpResponse('error')
        exceptions.handle(request,
                          _('Unable to get instance.'))
    return HttpResponse(json.dumps(rows))
