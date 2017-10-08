# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from dashboard.api.requestClient import request as req
from dashboard.views.base import HomePageView
import json
from dashboard.api.nova import server_list
from collections import OrderedDict
from dashboard import api
from horizon import exceptions
from dashboard.api import billing
from django.conf import settings
import logging

LOG = logging.getLogger(__name__)

class indexView(HomePageView):
    template_name = "securityGroup/securityGroupManage.html"

#    def get(self, request, *args, **kwargs):
        # if request.session.get('account',default=None) is None:
        #     return HttpResponseRedirect(settings.HORIZON_URL+'/auth/logout')
#        from dashboard.project.views1 import BillDetailsView
#        from django.core.urlresolvers import reverse
#        return HttpResponseRedirect(reverse('bill_details',args=args,kwargs=kwargs))

    def get_data(self):
        return {}

class securityGroupRuleIndex(HomePageView):
    template_name = "securityGroup/securityGroupRuleManage.html"
    def get_data(self):
        sg_id=self.request.GET.get('sg_id')
        securityGroup=api.network.security_group_get(self.request, sg_id)
        return {'sg_id':sg_id,'sg_name':securityGroup.name}

def securityGroupList(request):
    try:
        name=request.GET.get('name') if request.GET.has_key('name') else None
        if name:
            security_groups, total = api.network.security_group_list(request,name=name)
        else:
            security_groups, total = api.network.security_group_list(request)
        result={'total':total}
        rows=[]
        for security_group in security_groups:
            rows.append({'id':security_group.id,'name':security_group.name,'description':security_group.description})
        result['rows']=rows
    except Exception:
        security_groups = []
        exceptions.handle(request,
                          _('Unable to retrieve security groups.'))
    return HttpResponse(json.dumps(result))

def securityGroupNoPageList(request):
    try:
        security_groups,total = api.network.security_group_list(request)
        result={'total':total}
        rows=[]
        for security_group in security_groups:
            rows.append({'id':security_group.id,'name':security_group.name})
        result['rows']=rows
    except Exception:
        security_groups = []
        exceptions.handle(request,
                          _('Unable to retrieve security groups.'))
    return HttpResponse(json.dumps(rows))

def securityGroupDelete(request):
    try:
        sg_ids=request.POST.get("sg_ids")
        for sg_id in sg_ids.split(','):
            api.network.security_group_delete(request, sg_id)
    except Exception:
        exceptions.handle(request,
                          _('Unable to retrieve security groups.'))
        return HttpResponse('error')
    return HttpResponse('success')

def securityGroupCreate(request):
    try:
        name=request.POST.get("name")
        description=request.POST.get("description") if request.POST.has_key('description') else None
        api.network.security_group_create(request, name, description)
    except Exception:
        exceptions.handle(request,
                          _('Unable to retrieve security groups.'))
        return HttpResponse('error')
    return HttpResponse('success')

def securityGroupUpdate(request):
    try:
        sg_id=request.POST.get('sg_id')
        name=request.POST.get("name")
        description=request.POST.get("description") if request.POST.has_key('description') else None
        api.network.security_group_update(request, sg_id, name, description)
    except Exception:
        exceptions.handle(request,
                          _('Unable to retrieve security groups.'))
        return HttpResponse('error')
    return HttpResponse('success')

def securityGroupRuleList(request):
    try:
        sg_id=request.GET.get('sg_id')
        limit=int(request.GET.get('limit'))
        offset=int(request.GET.get('offset'))
        security_group = api.network.security_group_get(request,sg_id,limit=1000,marker=str(offset)+'_'+str(limit))
        result={'total':security_group.rules_total}
        rows=[]
        for security_group_rule in security_group.rules:
            rows.append({'id':security_group_rule['id'],'group':security_group_rule['group']['name']if security_group_rule['group'].has_key('name') else '' ,'port_range':_getIpProtocolName(security_group_rule['ip_protocol'],security_group_rule['from_port'],security_group_rule['to_port']),'from_port':security_group_rule['from_port'],'to_port':security_group_rule['to_port'],'ip_range':security_group_rule['ip_range']['cidr'] if security_group_rule['ip_range'].has_key('cidr') else '','ethertype':security_group_rule['ethertype'],'direction':security_group_rule['direction'],'ip_protocol':security_group_rule['ip_protocol']})
        result['rows']=rows
    except Exception:
        result = []
        exceptions.handle(request,
                          _('Unable to retrieve security groups.'))
    return HttpResponse(json.dumps(result))

def securityGroupRuleDelete(request):
    try:
        sgr_ids=request.POST.get("sgr_ids")
        for sgr_id in sgr_ids.split(','):
            api.network.security_group_rule_delete(request, sgr_id)
    except Exception:
        exceptions.handle(request,
                          _('Unable to retrieve security groups.'))
        return HttpResponse('error')
    return HttpResponse('success')

def securityGroupRuleMenu(request):
    backend = api.network.security_group_backend(request)

    rules_dict = getattr(settings, 'SECURITY_GROUP_RULES', [])
    common_rules = [(k, rules_dict[k]['name'])
                    for k in rules_dict
                    if rules_dict[k].get('backend', backend) == backend]
    common_rules.sort()
    custom_rules = [('tcp', '定制 TCP规则'),
                    ('udp', '定制UDP规则'),
                    ('icmp', '定制ICMP规则')]
    if backend == 'neutron':
        custom_rules.append(('custom', '其它协议'))
    result= custom_rules + common_rules
    return HttpResponse(json.dumps(result))

def securityGroupRuleCreate(request):
    try:
        custom_rules=['tcp','udp','icmp']
        all_rules=['all_tcp','all_udp','all_icmp']
        other_rules=['custom']
        post_data = request.POST
        rule_menu=post_data.get('rule_menu')
        parent_group_id=post_data.get('parent_group_id')
        direction='ingress'
        ethertype='IPv4'
        ip_protocol=None
        from_port=None
        to_port=None
        cidr=None
        group_id=None
        port_type=post_data.get('port_type')
        remote=post_data.get('remote')
        if remote=='cidr':
            cidr=post_data.get('cidr')
        else:
            group_id=post_data.get('group_id')
            ethertype=post_data.get('ethertype')
        
        if rule_menu in custom_rules:
            direction=post_data.get('direction')
            ip_protocol=rule_menu
            if port_type=='port':
                from_port=post_data.get('port')
                to_port=from_port
            else:
                from_port=post_data.get('from_port')
                to_port=post_data.get('to_port')
        elif rule_menu in all_rules:
            direction=post_data.get('direction')
            ip_protocol=_getIpProtocol(rule_menu)
            from_port,to_port=_getPortByIpProtocol(rule_menu)
        elif rule_menu in other_rules:
            direction=post_data.get('direction')
            ip_protocol=post_data.get('ip_protocol')
        else:
            ip_protocol=_getIpProtocol(rule_menu)
            from_port,to_port=_getPortByIpProtocol(rule_menu)
            
        api.network.security_group_rule_create(request, parent_group_id, direction, ethertype, ip_protocol, from_port, to_port, cidr, group_id)
    except Exception:
        exceptions.handle(request,
                          _('Unable to retrieve security groups.'))
        return HttpResponse('error')
    return HttpResponse('success')

def _getIpProtocolName(ip_protocol,from_port,to_port):
    if from_port==to_port:
        rules_dict = getattr(settings, 'SECURITY_GROUP_RULES', [])
        for k in rules_dict:
            if rules_dict[k].get('ip_protocol') == ip_protocol and rules_dict[k].get('from_port') == str(from_port) and rules_dict[k].get('to_port') == str(to_port):
                return str(from_port) +'('+rules_dict[k].get('name')+')'
        return from_port
    return str(from_port)+'-'+str(to_port)

def _getIpProtocol(ip_protocol):
    rules_dict = getattr(settings, 'SECURITY_GROUP_RULES', [])
    return rules_dict[ip_protocol]['ip_protocol']if rules_dict.has_key(ip_protocol) else ip_protocol

def _getPortByIpProtocol(ip_protocol):
    rules_dict = getattr(settings, 'SECURITY_GROUP_RULES', [])
    return (rules_dict[ip_protocol]['from_port'],rules_dict[ip_protocol]['to_port']) if rules_dict.has_key(ip_protocol) else (None,None)
