import logging
import operator
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator  # noqa
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters  # noqa
from django.http import HttpResponse,HttpResponseRedirect
from horizon import exceptions
from horizon import messages
from django.shortcuts import render
from django.http.response import HttpResponse
from dashboard.api.requestClient import request as req
from dashboard.views.base import HomePageView
from dashboard import api
from dashboard import policy
import json
import django.views.generic as classview


LOG = logging.getLogger(__name__)


class IndexView(classview.TemplateView):
    template_name = 'admin/index.html'
    page_title = _("Users")

    def get_data(self):
        users = []
        if policy.check((("identity", "identity:list_users"),),
                        self.request):
            domain_context = api.keystone.get_effective_domain_id(self.request)
            try:
                users = api.keystone.user_list(self.request,
                                               domain=domain_context)
            except Exception as e:
                exceptions.handle(self.request,
                                  _('Unable to retrieve user list.'))
        elif policy.check((("identity", "identity:get_user"),),
                          self.request):
            try:
                user = api.keystone.user_get(self.request,
                                             self.request.user.id)
                users.append(user)
            except Exception:
                exceptions.handle(self.request,
                                  _('Unable to retrieve user information.'))
        else:
            msg = _("Insufficient privilege level to view user information.")
            messages.info(self.request, msg)

        if api.keystone.VERSIONS.active >= 3:
            domain_lookup = api.keystone.domain_lookup(self.request)
            for u in users:
                u.domain_name = domain_lookup.get(u.domain_id)
            
        paginator = Paginator(users,5)
         
        try:
            page = int(self.request.GET.get('page','1'))
        except ValueError:
            page = 1
     
        try:
            users = paginator.page(page)
        except :
            users = paginator.page(paginator.num_pages)
        return users

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['users'] = self.get_data()
        return context

def create_user(request):
    data={}
    domain = api.keystone.get_default_domain(request, False)
    if request.method == 'POST':
        
        data['email'] = request.POST.get("email")
        data['name'] = request.POST.get("name")
        data['description'] =  request.POST.get("description")
        data['password']=request.POST.get("password")
        data['project']=request.POST.get("project")
        
        try:
            new_user = \
                api.keystone.user_create(request,
                                         name=data['name'],
                                         email=data['email'],
                                         password=data['password'],
                                         project=data['project'] or None,
                                         enabled=data['enabled'],
                                         description=data['description'],
                                         domain=domain.id)
        except Exception as e:
            exceptions.handle(request, _('Unable to create user.'))                
            
        return HttpResponseRedirect(reverse('index'))
            
    return render(request,'admin/create.html',{'domain':domain})

def register_user(request):
    data={}
    domain = api.keystone.get_default_domain(request, False)
    if request.method == 'POST':
        
        data['email'] = request.POST.get("email")
        data['name'] = request.POST.get("name")
        data['description'] =  request.POST.get("description")
        data['password']=request.POST.get("password")
        data['project']="services"
        
        try:
            new_user = \
                api.keystone.user_create(request,
                                         name=data['name'],
                                         email=data['email'],
                                         password=data['password'],
                                         project=data['project'] or None,
                                         enabled=data['enabled'],
                                         description=data['description'],
                                         domain=domain.id)
        except Exception as e:
            exceptions.handle(request, _('Unable to create user.'))
                               
        return HttpResponseRedirect(reverse('index'))
                               
    return render(request,'admin/register.html',{'domain':domain})



def update_user(request,user_id=""):
    data={}
    user=api.keystone.user_get(request, user_id,
                                         admin=True)
    if request.method == 'POST':
        data['email'] = request.POST.get("email")
        data['name'] = request.POST.get("name")
        data['description'] =  request.POST.get("description")
        try:
            uu = api.keystone.user_update(request, user.id, **data)
            messages.success(request,
                             _('User has been updated successfully.'))
        except Exception:
            msg = _('User name "%s" is already used.') % data['name']
            messages.error(request, msg)
            
        return HttpResponseRedirect(reverse('index'))
            
    return render(request,'admin/update.html',{'user':user})
    
def delete_user(request,user_id=""):
    data={}
    user=api.keystone.user_get(request, user_id,
                                         admin=True)
    if request.method == 'POST':
        data['enabled'] = not user.enabled
        try:
            uu = api.keystone.user_update(request, user.id, **data)
            messages.success(request,
                             _('User has been updated successfully.'))
        except Exception:
            msg = _('error.')
            messages.error(request, msg)
            
    return HttpResponseRedirect(reverse('index'))


def change_password(request,user_id=""):
    print user_id
    user=api.keystone.user_get(request, user_id,admin=True)
    if request.method == "POST":
        password = request.POST.get("password")
#        print 'password:'
        try:
            response = api.keystone.user_update_password(
                request, user.id, password)
#             if user_id == request.user.id:
#                 return utils.logout_with_message(
#                     request,
#                     _('Password changed. Please log in to continue.'),
#                     redirect=False)
            messages.success(request,
                             _('User password has been updated successfully.'))
        except Exception as e:
            response = exceptions.handle(request, ignore=True)
            messages.error(request, _('Unable to update the user password.'))
        
        return HttpResponseRedirect(reverse('index'))

    return render(request,'admin/change_password.html',{'user':user})

def toggle_user(request,user_id=""):
    data={}
    user=api.keystone.user_get(request, user_id,
                                         admin=True)
    if request.method == 'POST':
        data['enabled'] = not user.enabled
        try:
            uu = api.keystone.user_update(request, user.id, **data)
            messages.success(request,
                             _('User has been updated successfully.'))
        except Exception:
            msg = _('error.')
            messages.error(request, msg)
            
    return HttpResponseRedirect(reverse('index'))
            
            
class ProjectIndexView(classview.TemplateView):
    template_name = 'admin/project.html'
    page_title = _("Projects")

    def get_data(self):
        tenants = []
        #pagination_param = "tenant_marker"
        #marker = self.request.GET.get(
        #   pagination_param, None)

        self._more = False

        if policy.check((("identity", "identity:list_projects"),),
                        self.request):
            domain_context = api.keystone.get_effective_domain_id(self.request)
            try:
                tenants, self._more = api.keystone.tenant_list(
                    self.request)
            except Exception as e:
                pass
        elif policy.check((("identity", "identity:list_user_projects"),),
                          self.request):
            try:
                tenants, self._more = api.keystone.tenant_list(
                    self.request,
                    user=self.request.user.id,
                    paginate=True,
                    marker=None,
                    admin=False)
            except Exception:
                exceptions.handle(self.request,
                                  _("Unable to retrieve project information."))
        else:
            msg = \
                _("Insufficient privilege level to view project information.")
            messages.info(self.request, msg)

        if api.keystone.VERSIONS.active >= 3:
            domain_lookup = api.keystone.domain_lookup(self.request)
            for t in tenants:
                t.domain_name = domain_lookup.get(t.domain_id)
        return tenants

    def get_context_data(self, **kwargs):
        context = super(ProjectIndexView, self).get_context_data(**kwargs)
        context['projects'] = self.get_data()
        print context['projects'] 
        return context
    
def create_project(request):
    data={}
    domain = api.keystone.get_default_domain(request, False)
    if request.method == 'POST':
        
        data['email'] = request.POST.get("email")
        data['name'] = request.POST.get("name")
        data['description'] =  request.POST.get("description")
        data['password']=request.POST.get("password")
        data['project']=request.POST.get("project")
        
        try:
            new_user = \
                api.keystone.user_create(request,
                                         name=data['name'],
                                         email=data['email'],
                                         description=data['description'],
                                         password=data['password'],
                                         project=data['project'] or None,
                                         enabled=data['enabled'],
                                         domain=domain.id)
        except Exception:
            exceptions.handle(request, _('Unable to create user.'))                
            
        return HttpResponseRedirect(reverse('index'))
            
    return render(request,'admin/create_project.html',{'domain':domain})

def update_project(request,user_id=""):
    data={}
    user=api.keystone.user_get(request, user_id,
                                         admin=True)
    if request.method == 'POST':
        data['email'] = request.POST.get("email")
        data['name'] = request.POST.get("name")
        data['description'] =  request.POST.get("description")
        try:
            uu = api.keystone.user_update(request, user.id, **data)
            messages.success(request,
                             _('User has been updated successfully.'))
        except Exception:
            msg = _('User name "%s" is already used.') % data['name']
            messages.error(request, msg)
            
        return HttpResponseRedirect(reverse('index'))
            
    return render(request,'admin/update_project.html',{'user':user})
    
def delete_project(request,user_id=""):
    data={}
    user=api.keystone.user_get(request, user_id,
                                         admin=True)
    if request.method == 'POST':
        data['enabled'] = not user.enabled
        try:
            uu = api.keystone.user_update(request, user.id, **data)
            messages.success(request,
                             _('User has been updated successfully.'))
        except Exception:
            msg = _('error.')
            messages.error(request, msg)
            
    return HttpResponseRedirect(reverse('index'))




    
            
