import logging
import operator
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator  # noqa
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters  # noqa
from django.http import HttpResponse,HttpResponseRedirect
from horizon import exceptions
from horizon import messages
from django.shortcuts import render
from django.http.response import HttpResponse
from dashboard.api.requestClient import request as req
from dashboard.views.base import HomePageView
from dashboard import api
from dashboard import policy
import json
import django.views.generic as classview


LOG = logging.getLogger(__name__)


class FloatingView(classview.TemplateView):
    template_name = 'network/floating_ips.html'
    page_title = _("Floating_ips")

    def get_data(self):
        ips = []
        try:
            ips = api.network.tenant_floating_ip_list(self.request)
        except Exception as e:
            exceptions.handle(self.request,
                              _('Unable to retrieve floating IP addresses.'))
        return ips

    def get_context_data(self, **kwargs):
        context = super(FloatingView, self).get_context_data(**kwargs)
        context['ips'] = self.get_data()
        return context


    
            