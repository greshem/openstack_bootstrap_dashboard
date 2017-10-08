"""
WSGI config for billing_center project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys
import django

from django.core.wsgi import get_wsgi_application

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
django.conf.ENVIRONMENT_VARIABLE = 'DJANGO_CENTER_SETTINGS_MODULE'
os.environ.setdefault("DJANGO_CENTER_SETTINGS_MODULE", "dashboard.settings")

application = get_wsgi_application()
