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
    template_name = "user/usermanage.html"
    def get_data(self):
        return {}

class UserInfoView(HomePageView):
    template_name = "user/user_info.html"
    def get_data(self):
        return {}
