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
from views import router_list
from views import get_ext_net
from views import router_create
from views import router_delete
from views import router_update
from views import getPriceDiscount
from views import portView
from views import port_list
from views import port_update
from views import port_delete
from views import routeView
from views import route_list
from views import route_delete
from views import route_create

urlpatterns = patterns('',
   url(r'^$', indexView.as_view(),name="router_index"),
   url(r'^port$', portView.as_view(),name="router_port_index"),
   url(r'^route$', routeView.as_view(),name="router_route_index"),
   url(r'^router$', router_list,name="router_list"),
   url(r'^extnet$', get_ext_net,name="router_extnet"),
   url(r'^create$', router_create,name="router_create"),
   url(r'^delete$', router_delete,name="router_delete"),
   url(r'^update$', router_update,name="router_update"),
   url(r'^router_billing$', getPriceDiscount,name="router_billing"),
   url(r'^port/list$', port_list,name="router_port_list"),
   url(r'^port/update$', port_update,name="router_port_update"),
   url(r'^port/delete$', port_delete,name="router_port_delete"),
   url(r'^route/list$', route_list,name="router_route_list"),
   url(r'^route/delete$', route_delete,name="router_route_delete"),
   url(r'^route/create$', route_create,name="router_route_create"),
)
