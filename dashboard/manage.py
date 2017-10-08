# -*- coding:utf-8 -*-
import os
import sys
#sys.path.append(r'D:\eclipse\plugins\org.python.pydev_2.7.1.2012100913\pysrc') #将pysrc加入到系统路径中
#import pydevd #@UnresolvedImport
#pydevd.patch_django_autoreload()
if __name__ == "__main__":
#    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dashboard.settings")
    sys.path.append("./");
    #sys.path.append("/root/CI/");
    os.environ['DJANGO_SETTINGS_MODULE']="dashboard.settings"
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
