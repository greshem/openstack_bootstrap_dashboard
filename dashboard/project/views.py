# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http.response import HttpResponse
from dashboard.api.requestClient import request as req
from dashboard.views.base import HomePageView
import json
from django.conf import settings
from dashboard.api.requestClient import request as billing_request
from dashboard import api
import datetime
from django.utils import timezone
from horizon import exceptions
from horizon import messages
from django.utils.translation import ugettext_lazy as _

def getRegions(request):
    result=req("common/getregionlist")
    return HttpResponse(json.dumps(result['regionList']))


def index(request):
    result=req("account/list")
    data={'total':result['accountList']['total'],'rows':result['accountList']['accounts']}
    return HttpResponse(json.dumps(data))


class indexView(HomePageView):
    print "LOGGER::  index View  ";
    #from ipdb import  set_trace;
    #set_trace();
    template_name = "ECloud.html"

#    def get(self, request, *args, **kwargs):
        # if request.session.get('account',default=None) is None:
        #     return HttpResponseRedirect(settings.HORIZON_URL+'/auth/logout')
#        from dashboard.project.views1 import BillDetailsView
#        from django.core.urlresolvers import reverse
#        return HttpResponseRedirect(reverse('bill_details',args=args,kwargs=kwargs))

    def get_data(self):
#         account=self.request.session['account']
#         account=billing_request('/account/detail/'+account['account_id'])['account']
#         balance=float(account['cash_balance'])+float(account['gift_balance'])
        
        projectUsage=ProjectUsage(self.request)
        projectUsage.get_limits()
        projectUsage.get_router_usage_list()
        projectUsage.get_network_usage_list()
        limits=projectUsage.limits
        return {'routers':limits['totalRoutersUsed'],'networks':limits['totalNetworksUsed'],'instances':limits['totalInstancesUsed'],'vcpus':limits['totalCoresUsed'],'memory_mb':limits['totalRAMUsed'],'floatingIps':limits['totalFloatingIpsUsed'],'securityGroups':limits['totalSecurityGroupsUsed'],'volumes':limits['totalVolumesUsed'],'volumes_gb':limits['totalGigabytesUsed']}
       
#        account_id=self.request.GET['account_id']
#        m=None
#        if self.request.GET.has_key('m'):
#            m=self.request.GET['m']
#        if 'sign' in self.request.GET:
#            sign=self.request.GET['sign']
#            md5_key=settings.MD5_KEY
#            if self.request.session.has_key('account'):
#                if self.request.session.get('account')['account_id']!=account_id:
#                    self.request.session['account']=None
#            if getMD5(account_id+md5_key) !=sign:
#                return
##        else:
##            return
#        url=None
#        host = self.request.get_host()
#        host_list=host.split(':')
#        host=host_list[0]
#        logo=''
#        hostmanage=settings.HOSTMANAGE
#        if host in hostmanage:
#            logoDic=host.split(".")
#            logo=logoDic[-2]
#        if self.request.session.get('account',default=None) is not None:
#            account_id=self.request.session.get('account')['account_id']
#            url = "/common/checkprojectadmin/%s"%account_id
#            flag = req(url)['isProjectAdmin']
#            url = "/account/checkadmin/%s"%account_id
#            adminflag=req(url)['isAdmin']
#            return {'logo':logo,'isProjectAdmin': flag,'isAdmin':adminflag,'username': self.request.session['account']['username'],'horizon_url':settings.HORIZON_URL,'m':m}
#        else:
##            return {}
#            account=req('/account/detail/%s'%account_id)['account']
#            self.request.session['account']=account
#        url = "/common/checkprojectadmin/%s"%account_id
#        flag = req(url)['isProjectAdmin']
#        url = "/account/checkadmin/%s"%account_id
#        adminflag=req(url)['isAdmin']
#        return {'logo':logo,'isProjectAdmin': flag,'isAdmin':adminflag,'username': self.request.session['account']['username'],'horizon_url':settings.HORIZON_URL,'m':m}

class testView(HomePageView):
    template_name = "test.html"

#    def get(self, request, *args, **kwargs):
        # if request.session.get('account',default=None) is None:
        #     return HttpResponseRedirect(settings.HORIZON_URL+'/auth/logout')
#        from dashboard.project.views1 import BillDetailsView
#        from django.core.urlresolvers import reverse
#        return HttpResponseRedirect(reverse('bill_details',args=args,kwargs=kwargs))

    def get_data(self):
        return {}


class abc(HomePageView):
    template_name = "home.html"

    def get_data(self):

        return {'abc':req("address/list/123hdfsfbsdf7uuieruiteb")}
        #return {'abc':"fdfd"}

        # result=req("invoice/list/2e7d7572a02e4a13852d675973c3e8bf")
        # #result1 = HttpResponse(json.dumps(result))
        #
        # invoices_list=result[u'invoiceList']['invoices']


        # return {'abc': invoices_list}
        # return {'abc':'12344'}

    #
    # def post(self, request, *args, **kwargs):
    #     k={'name':'wangzp','create':'xxxxx', 'post_code':'200000',
    #      'phone':'12345678', 'mobile':'258741369', 'status':'using'}
    #     ddd=json.dumps(k)
    #     result=req("/address/create/2e7d7572a02e4a13852d675973c3e8bf", method='POST', data=ddd)
    #     return result
class BaseUsage(object):
    show_deleted = False

    def __init__(self, request, project_id=None):
        self.project_id = project_id or request.user.tenant_id
        self.request = request
        self.summary = {}
        self.usage_list = []
        self.limits = {}
        self.quotas = {}

    @property
    def today(self):
        return timezone.now()

    @property
    def first_day(self):
        days_range = getattr(settings, 'OVERVIEW_DAYS_RANGE', 1)
        if days_range:
            return self.today.date() - datetime.timedelta(days=days_range)
        else:
            return datetime.date(self.today.year, self.today.month, 1)

    @staticmethod
    def get_start(year, month, day):
        start = datetime.datetime(year, month, day, 0, 0, 0)
        return timezone.make_aware(start, timezone.utc)

    @staticmethod
    def get_end(year, month, day):
        end = datetime.datetime(year, month, day, 23, 59, 59)
        return timezone.make_aware(end, timezone.utc)

    def get_instances(self):
        instance_list = []
        [instance_list.extend(u.server_usages) for u in self.usage_list]
        return instance_list

    def get_date_range(self):
        if not hasattr(self, "start") or not hasattr(self, "end"):
            args_start = (self.first_day.year, self.first_day.month,
                          self.first_day.day)
            args_end = (self.today.year, self.today.month, self.today.day)
            self.start = self.get_start(*args_start)
            self.end = self.get_end(*args_end)
        return self.start, self.end

    def init_form(self):
        self.start = self.first_day
        self.end = self.today.date()

        return self.start, self.end


    def _get_neutron_usage(self, limits, resource_name):
        resource_map = {
            'floatingip': {
                'api': api.network.tenant_floating_ip_list,
                'limit_name': 'totalFloatingIpsUsed',
                'message': _('Unable to retrieve floating IP addresses.')
            },
            'security_group': {
                'api': api.network.security_group_list,
                'limit_name': 'totalSecurityGroupsUsed',
                'message': _('Unable to retrieve security groups.')
            }
        }

        resource = resource_map[resource_name]
        try:
            method = resource['api']
            current_used = len(method(self.request))
        except Exception:
            current_used = 0
            msg = resource['message']
            exceptions.handle(self.request, msg)

        limits[resource['limit_name']] = current_used

    def _set_neutron_limit(self, limits, neutron_quotas, resource_name):
        limit_name_map = {
            'floatingip': 'maxTotalFloatingIps',
            'security_group': 'maxSecurityGroups',
        }
        if neutron_quotas is None:
            resource_max = float("inf")
        else:
            resource_max = getattr(neutron_quotas.get(resource_name),
                                   'limit', float("inf"))
            if resource_max == -1:
                resource_max = float("inf")

        limits[limit_name_map[resource_name]] = resource_max

    def get_neutron_limits(self):
        if not api.base.is_service_enabled(self.request, 'network'):
            return
        try:
#            neutron_quotas_supported = (
#                api.neutron.is_quotas_extension_supported(self.request))
            neutron_sg_used = (
                api.neutron.is_extension_supported(self.request,
                                                   'security-group'))
            if api.network.floating_ip_supported(self.request):
                self._get_neutron_usage(self.limits, 'floatingip')
            if neutron_sg_used:
                self._get_neutron_usage(self.limits, 'security_group')
            else:
                self.limits['totalSecurityGroupsUsed']=0
            # Quotas are an optional extension in Neutron. If it isn't
            # enabled, assume the floating IP limit is infinite.
#            if neutron_quotas_supported:
#                neutron_quotas = api.neutron.tenant_quota_get(self.request,
#                                                              self.project_id)
#            else:
#                neutron_quotas = None
        except Exception:
            # Assume neutron security group and quotas are enabled
            # because they are enabled in most Neutron plugins.
            neutron_sg_used = True
#            neutron_quotas = None
            msg = _('Unable to retrieve network quota information.')
            exceptions.handle(self.request, msg)

#        self._set_neutron_limit(self.limits, neutron_quotas, 'floatingip')
#        if neutron_sg_used:
#            self._set_neutron_limit(self.limits, neutron_quotas,
#                                    'security_group')

    def get_cinder_limits(self):
        """Get volume limits if cinder is enabled."""
        if not api.cinder.is_volume_service_enabled(self.request):
            return
        try:
            self.limits.update(api.cinder.tenant_absolute_limits(self.request))
        except Exception:
            msg = _("Unable to retrieve volume limit information.")
            exceptions.handle(self.request, msg)

        return

    def get_limits(self):
        try:
            self.limits = api.nova.tenant_absolute_limits(self.request,
                                                          reserved=True)
        except Exception:
            exceptions.handle(self.request,
                              _("Unable to retrieve limit information."))
        self.get_neutron_limits()
        self.get_cinder_limits()

    def get_usage_list(self, start, end):
        return []

    def summarize(self, start, end):
        if not api.nova.extension_supported('SimpleTenantUsage', self.request):
            return

        if start <= end and start <= self.today:
            # The API can't handle timezone aware datetime, so convert back
            # to naive UTC just for this last step.
            start = timezone.make_naive(start, timezone.utc)
            end = timezone.make_naive(end, timezone.utc)
            try:
                self.usage_list = self.get_usage_list(start, end)
            except Exception:
                exceptions.handle(self.request,
                                  _('Unable to retrieve usage information.'))
        elif end < start:
            messages.error(self.request,
                           _("Invalid time period. The end date should be "
                             "more recent than the start date."))
        elif start > self.today:
            messages.error(self.request,
                           _("Invalid time period. You are requesting "
                             "data from the future which may not exist."))

        for project_usage in self.usage_list:
            project_summary = project_usage.get_summary()
            for key, value in project_summary.items():
                self.summary.setdefault(key, 0)
                self.summary[key] += value


    def csv_link(self):
        form = self.get_form()
        data = {}
        if hasattr(form, "cleaned_data"):
            data = form.cleaned_data
        if not ('start' in data and 'end' in data):
            data = {"start": self.today.date(), "end": self.today.date()}
        return "?start=%s&end=%s&format=csv" % (data['start'],
                                                data['end'])


class GlobalUsage(BaseUsage):
    show_deleted = True

    def get_usage_list(self, start, end):
        return api.nova.usage_list(self.request, start, end)


class ProjectUsage(BaseUsage):
    attrs = ('memory_mb', 'vcpus', 'uptime',
             'hours', 'local_gb')

    def get_usage_list(self, start, end):
        show_deleted = self.request.GET.get('show_deleted',
                                            self.show_deleted)
        instances = []
        deleted_instances = []
        usage = api.nova.usage_get(self.request, self.project_id)
        # Attribute may not exist if there are no instances
        if hasattr(usage, 'server_usages'):
            now = self.today
            for server_usage in usage.server_usages:
                # This is a way to phrase uptime in a way that is compatible
                # with the 'timesince' filter. (Use of local time intentional.)
                server_uptime = server_usage['uptime']
                total_uptime = now - datetime.timedelta(seconds=server_uptime)
                server_usage['uptime_at'] = total_uptime
                if server_usage['ended_at'] and not show_deleted:
                    deleted_instances.append(server_usage)
                else:
                    instances.append(server_usage)
        usage.server_usages = instances
        return (usage,)
    
    def get_router_usage_list(self):
        limit = 1
        offset = 0
        param = {'marker':str(offset) + '_' + str(limit)}
        result = api.neutron.router_list(self.request,
                                          tenant_id=self.project_id,page=True,**param)
        total = 0
        if isinstance(result,tuple):
            total = result[1]
        self.limits['totalRoutersUsed']=total
    
    def get_network_usage_list(self):
        limit = 1
        offset = 0
#        param={'router__external':False}
        param = {'marker':str(offset) + '_' + str(limit)}
        result = api.neutron.network_list_for_tenant(self.request, self.project_id, include_external=False, page=True, **param)
        total = 0
        if isinstance(result,tuple):
            total = result[1]
        self.limits['totalNetworksUsed']=total
