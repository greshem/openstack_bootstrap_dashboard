# -*- coding:utf-8 -*-
"""Starter script for billing OS API."""

import sys
sys.path.append("/home/yamin/me/git_home/billing")
sys.path.append("/home/yamin/me/git_home/sms_sdk")
sys.path.append("/home/greshem/billing")
from oslo_config import cfg
from oslo_log import log as logging
CONF = cfg.CONF
timezone_local=[
    cfg.StrOpt('timezone_local',
               default='Asia/Shanghai',
               help=''),
]
workers=[
    cfg.IntOpt('workers',
               default=1,
               help=''),
]
CONF.register_opts(timezone_local)
CONF.register_opts(workers)

from billing import config
#from billing import objects
#from billing.openstack.common.report import guru_meditation_report as gmr
from billing import service
from billing import utils
#from billing import version
#CONF.import_opt('enabled_ssl_apis', 'billing.service')


def main():
    config.parse_args(sys.argv)  #--config-dir D:\\workspace\\billing\\etc
    logging.setup(CONF, "billing")
    utils.monkey_patch()
#    objects.register_all()

#    gmr.TextGuruMeditation.setup_autorun(version)

#    should_use_ssl = 'api_billing' in CONF.enabled_ssl_apis
    server = service.WSGIService('api_billing', use_ssl=False)
    service.serve(server, workers=CONF.workers)
    service.wait()

if __name__=="__main__":
    main()
#    import cProfile
#    cProfile.run('main()','/home/yamin/billing.profile')
