# -*- coding: utf-8 -*-


import json
import six
from django.conf import settings
from django.http import HttpResponse  # noqa
from django.utils.translation import pgettext_lazy
from django.views.generic import View  # noqa
from horizon.utils.lazy_encoder import LazyTranslationEncoder
from horizon import exceptions
from dashboard import api



from dashboard.views.base import HomePageView



import logging

LOG = logging.getLogger(__name__)
LIMIT = 10

class indexView(HomePageView):
    template_name = "tenant/tenantmanage.html"
    def get_data(self):
        return {}

def tenant_list(request):
    
    try:
        for item in request.GET.keys():
            if item == 'offset':
                marker=request.GET.get(item)

        #tenants, more_data = api.keystone.tenant_list(request, True)
        tenants, more_data = api.keystone.tenant_list(request)

        result = []
        for tenant in tenants:
            result.append({
                "name":tenant.name,
                "description":tenant.description,
                "id":tenant.id,
                "domain_id":tenant.domain_id,
                "enabled":tenant.enabled
                })
        return HttpResponse(json.dumps(result))
    except Exception as e:
        exceptions.handle(request, 'Unable to retrieve tenant:%s' %e)
        return HttpResponse(json.dumps({"code":500, "result":"%s"%e}))
    
    
    
