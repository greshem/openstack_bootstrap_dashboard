# -*- coding:utf-8 -*-
'''
Created on 2015-8-28

@author: greshem
'''
from oslo_config import cfg
from oslo_log import log as logging
from paste import deploy

from billing import config
from billing import service  # noqa
from billing import utils

CONF = cfg.CONF

config_files = ['/etc/billing/api-paste.ini', '/etc/billing/billing.conf']
config.parse_args([], default_config_files=config_files)

LOG = logging.getLogger(__name__)
logging.setup(CONF, "billing")
utils.monkey_patch()

conf = config_files[0]
name = "api_billing"

options = deploy.appconfig('config:%s' % conf, name=name)

application = deploy.loadapp('config:%s' % conf, name=name)
