# -*- coding:utf-8 -*-
'''
Created on 2015年10月10日

@author: greshem
'''
from django.views.generic import View
from django.views.generic.base import TemplateView, ContextMixin

class BaseView(View):
    pass

class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context.update(self.get_data())
        return context
    
    def get_data(self):
        pass

class BillReqMixin(ContextMixin):
    '''

    '''
    def get_context_data(self, **kwargs):
        context = super(BillReqMixin, self).get_context_data(**kwargs)
        context.update(self.get_data())
        return context

    def get_data(self):
        pass
