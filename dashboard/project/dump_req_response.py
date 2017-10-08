# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.conf import settings
from dashboard.project.utils import getMD5
from dashboard.api.requestClient import request as req
from django.views.defaults import *

from django.http import (HttpResponse, HttpResponseServerError,HttpResponseNotFound, HttpRequest, build_request_repr)

  
import datetime
class dump_req_reponse(object):

    def process_request(self, request):
        print "#==============================================================";
        print "GRESHEM_request:%s"%build_request_repr(request);
        print "dir %s"%dir(request);
        return None

    def process_response(self, request,response):
        #print "GRESHEM_reponse:%s"%response;
        print "dir reponse  %s"%dir(response);
        return response;

