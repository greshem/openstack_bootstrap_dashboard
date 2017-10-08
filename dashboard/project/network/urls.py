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
from django.conf.urls import url, patterns

from views import indexView
from views import network_list
from views import network_delete
from views import network_update
from views import network_create
from views import subnet_update
from views import get_subnet
from views import portView
from views import port_list
from views import port_update

urlpatterns = patterns('',
   url(r'^$', indexView.as_view(),name="network_index"),
   url(r'^port$', portView.as_view(),name="network_port_index"),
   url(r'^list$', network_list,name="network_list"),
   url(r'^delete$', network_delete,name="network_delete"),
   url(r'^update$', network_update,name="network_update"),
   url(r'^create$', network_create,name="network_create"),
   url(r'^subnet/update$', subnet_update,name="subnet_update"),
   url(r'^subnet/detail$', get_subnet,name="subnet_show"),
   url(r'^port/list$', port_list,name="network_port_list"),
   url(r'^port/update$', port_update,name="network_port_update"),
)
