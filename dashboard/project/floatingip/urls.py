"""billing_center URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns

from django.views.generic import TemplateView
from views import indexView
from views import floatingip_list
from views import floatingip_delete
from views import floatingip_pools_list
from views import floatingip_allocate
from views import getPriceDiscount
from views import port_list
from views import floatingip_associate
from views import floatingip_disassociate
from views import floatingip_noassociate_list

urlpatterns = patterns('',
   url(r'^$', indexView.as_view(),name="floatingip_index"),
   url(r'^list$', floatingip_list,name="floatingip_list"),
   url(r'^noassociate_list$', floatingip_noassociate_list,name="floatingip_noassociate_list"),
   url(r'^delete$', floatingip_delete,name="floatingip_delete"),
   url(r'^allocate$', floatingip_allocate,name="floatingip_allocate"),
   url(r'^associate$', floatingip_associate,name="floatingip_associate"),
   url(r'^disassociate$', floatingip_disassociate,name="floatingip_disassociate"),
   url(r'^floatingip_billing$', getPriceDiscount,name="floatingip_billing"),
   url(r'^pool/list$', floatingip_pools_list,name="floatingip_pools_list"),
   url(r'^port/list$', port_list,name="floatingip_port_list"),
)
