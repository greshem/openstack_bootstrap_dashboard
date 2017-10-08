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
from django.conf.urls import include, url
from django.conf import settings

urlpatterns = [
    url(r'^project/', include('dashboard.project.urls')),
    url(r'^admin/',include('dashboard.admin.urls')),
    url(r'^network/',include('dashboard.network.urls')),
#    url(r'^(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
    #url(r'^(?P<path>.*)$', serve),
    #url(r'^payment/', include('billing_payment.payment.urls')),
]

for u in getattr(settings, 'AUTHENTICATION_URLS', ['openstack_auth.urls']):
    urlpatterns.append(url(r'^auth/', include(u)))
    
#if not settings.DEBUG:
#    urlpatterns.append(url(r'^(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}))
