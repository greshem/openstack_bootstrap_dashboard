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

from views import indexView
from views import image_list
from views import image_update
from views import image_delete
from views import get_image

urlpatterns = patterns('',
   url(r'^$', indexView.as_view(),name="image_index"),
   url(r'^list$', image_list,name="image_list"),
   url(r'^update$', image_update,name="image_update"),
   url(r'^delete$', image_delete,name="image_delete"),
   url(r'^image_get',get_image,name="image_get"),
)
