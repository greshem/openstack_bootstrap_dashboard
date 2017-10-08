# -*- coding:utf-8 -*-
'''
Created on 2016年9月28日

@author: greshem
'''
from dashboard import api
LIMIT=10
def getFix(floating_ip_port):
    if floating_ip_port and floating_ip_port.fixed_ips:
        fixed_ip_address=''
        for fixed_ip in floating_ip_port.fixed_ips:
            if fixed_ip_address:
                fixed_ip_address=fixed_ip_address+'</br>'+fixed_ip['ip_address']
            else:
                fixed_ip_address=fixed_ip['ip_address']
        return fixed_ip_address
    return None
def getFloatingIpInfo(request,port_id,floatingips,floatingip_total):
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
def getDeviceInfo(request,floating_ip_port,instance_dict,total):
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