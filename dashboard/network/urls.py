from django.conf.urls import include, url, patterns
#from dashboard.admin.urls import *
from dashboard.network import views



urlpatterns = patterns('network.views',

     #url(r'^admin/accounts', 'account_manage',name='account_manage'),
     url(r'^floating_ips/$', views.FloatingView.as_view(), name='floating_ips'),

     
)
