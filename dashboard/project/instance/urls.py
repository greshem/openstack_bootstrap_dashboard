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
from views import instance_list
from views import updateInstance
from views import startInstance
from views import stopInstance
from views import rebootInstance
from views import deleteInstance
from views import getImages
from views import getRegions
from views import getPriceDiscount
from views import instance_create
from views import getNetworks
from views import availability_zone_list
from views import instance_list_attach
from views import get_console
from views import resize
from views import getInstanceSecurityGroup
from views import updateInstanceSecurityGroup
from views import disassociate
from views import getInstancePorts
from views import associate
from views import create_snapshot
from views import instance_flavor_create
from views import get_instance

urlpatterns = patterns('',
   url(r'^$', indexView.as_view(),name="instance_index"),
   url(r'^list$',instance_list ,name="instance_list"),
   url(r'^list_attach$',instance_list_attach ,name="instance_list_attach"),
   url(r'^update$',updateInstance ,name="instance_update"),
   url(r'^start$',startInstance ,name="instance_start"),
   url(r'^stop$',stopInstance ,name="instance_stop"),
   url(r'^reboot$',rebootInstance ,name="instance_reboot"),
   url(r'^delete$',deleteInstance,name="instance_delete"),
   url(r'^console$',get_console,name="instance_console"),
   url(r'^image_list$',getImages,name="instance_image_list"),
   url(r'^region_list$',getRegions,name="region_list"),
   url(r'^instance_billing$',getPriceDiscount,name="instance_billing"),
   url(r'^create$',instance_create,name="instance_create"),
   url(r'^network_list$',getNetworks,name="instance_network_list"),
   url(r'^disassociate$',disassociate,name="instance_disassociate"),
   url(r'^associate$',associate,name="instance_associate"),
   url(r'^zone_list$',availability_zone_list,name="zone_list"),
   url(r'^resize$',resize,name="instance_resize"),
   url(r'^securitygroup$',getInstanceSecurityGroup,name="instance_securitygroup"),
   url(r'^securitygroupupdate$',updateInstanceSecurityGroup,name="instance_securitygroup_update"),
   url(r'^ports$',getInstancePorts,name="instance_ports"),
   url(r'^snapshot_create$',create_snapshot,name="instance_snapshot_create"),
   url(r'^flavor_create$',instance_flavor_create,name="instance_flavor_create"),
   url(r'^instance_get',get_instance,name="instance_get"),
)
