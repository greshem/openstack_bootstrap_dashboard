from django.conf.urls import include, url, patterns
from dashboard.admin.urls import *
from dashboard.admin import views

#VIEWS_MOD = 'dashboard.admin.views'

urlpatterns = patterns('dashboard.admin.views',
#     VIEWS_MOD,
     #url(r'^admin/accounts', 'account_manage',name='account_manage'),
     url(r'^$', views.IndexView.as_view(), name='index'),
     url(r'^users/create/$', 'create_user', name='create_user'),
     url(r'^users/update/(?P<user_id>\w+)/$', 'update_user', name='update_user'),
     url(r'^users/change_password/(?P<user_id>\w+)/$', 'change_password', name='change_password'),
     #url(r'^users/change_password/$', 'change_password', name='change_password'),
     url(r'^users/delete/(?P<user_id>\w+)/$', 'delete_user', name='delete_user'),
     url(r'^users/toggle/(?P<user_id>\w+)/$', 'toggle_user', name='toggle_user'),
     
     url(r'^project/$', views.ProjectIndexView.as_view(), name='admin_project'),
     url(r'^project/create/$', 'create_project', name='create_project'),
     url(r'^project/update/(?P<project_id>\w+)/$', 'update_project', name='update_project'),
     url(r'^project/delete/(?P<project_id>\w+)/$', 'delete_project', name='delete_project'),

     
)
