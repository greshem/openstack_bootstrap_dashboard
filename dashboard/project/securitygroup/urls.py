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
from views import securityGroupList

from views import indexView
from views import securityGroupDelete
from views import securityGroupCreate
from views import securityGroupUpdate
from views import securityGroupRuleIndex
from views import securityGroupRuleList
from views import securityGroupRuleDelete
from views import securityGroupRuleMenu
from views import securityGroupRuleCreate
from views import securityGroupNoPageList

urlpatterns = patterns('',
   url(r'^$', indexView.as_view(),name="securitygroup_index"),
   url(r'^list$', securityGroupList,name="securitygroup_list"),
   url(r'^nopagelist$', securityGroupNoPageList,name="securitygroup_nopage_list"),
   url(r'^delete$', securityGroupDelete,name="securitygroup_delete"),
   url(r'^create$', securityGroupCreate,name="securitygroup_create"),
   url(r'^update$', securityGroupUpdate,name="securitygroup_update"),
   url(r'^rule$', securityGroupRuleIndex.as_view(),name="securitygrouprule_index"),
   url(r'^rule/list$', securityGroupRuleList,name="securitygrouprule_list"),
   url(r'^rule/delete$', securityGroupRuleDelete,name="securitygrouprule_delete"),
   url(r'^rule/menu$', securityGroupRuleMenu,name="securitygrouprule_menu"),
   url(r'^rule/create$', securityGroupRuleCreate,name="securitygrouprule_create"),
)
