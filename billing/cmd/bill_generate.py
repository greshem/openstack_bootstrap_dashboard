# -*- coding:utf-8 -*-
'''
Created on 2015-09-01

@author: greshem
'''
import sys
sys.path.append("/root/billing")
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from oslo_config import cfg
CONF = cfg.CONF
import datetime
import pytz
timezone_local=[
    cfg.StrOpt('timezone_local',
               default='Asia/Shanghai',
               help=''),
]
CONF.register_opts(timezone_local)



scheduler_time=[
    cfg.StrOpt('bill_generation_month',
               default='*',
               help=''),
    cfg.StrOpt('bill_generation_day',
               default='1,5,10,20',
               help=''),
    cfg.StrOpt('bill_generation_hour',
               default='0',
               help=''),
    cfg.StrOpt('bill_generation_minute',
               default='0',
               help=''),
]
CONF.register_opts(scheduler_time, 'scheduler_time')
from oslo_log import log as logging

from billing import config
from billing.hander.Bill import generateBill,generateBill_naas
from billing.hander.Rebate import generateRebateBill



tz = pytz.timezone(CONF.timezone_local)
utc = pytz.utc


def tick():
    last=datetime.datetime(datetime.date.today().year if datetime.date.today().month - 1 else datetime.date.today().year - 1,\
                                datetime.date.today().month - 1 or 12, 1,0,0,0)
    current=datetime.datetime(datetime.date.today().year, datetime.date.today().month, 1,0,0,0)
    last=datetime.datetime(2016,4,1,0,0,0)
    current=datetime.datetime(2016,5,1,0,0,0)
    last=tz.localize(last)
    current=tz.localize(current)
    generateBill(last.astimezone(utc),current.astimezone(utc),last,current)
    generateBill_naas(last.astimezone(utc),current.astimezone(utc),last,current)
    generateRebateBill(last.astimezone(utc),current.astimezone(utc),last,current)
    # generateBill('2016-04-08 01:00:00','2016-04-08 02:00:00')
    # generateBill_naas('2016-04-08 01:00:00','2016-04-08 02:00:00')
def main():
    config.parse_args(sys.argv)
    logging.setup(CONF, "billing")
   
    executors = {    
                 'default': ThreadPoolExecutor(10),
                 'processpool': ProcessPoolExecutor(3)
                 }
    job_defaults = {    
                    'coalesce': True,
                    'max_instances':2,
                    'misfire_grace_time':3600
                    }
    scheduler = BlockingScheduler(executors=executors, job_defaults=job_defaults, timezone=CONF.timezone_local)
#    scheduler.add_jobstore('sqlalchemy', url=CONF.database.connection)
#    scheduler.add_job(tick, 'interval', seconds=10,id="abcdefg")
#    scheduler.add_job(tick, 'cron', second='5,10,15,20,25,30,35,40,45,50,55',id="bill_generation")
    scheduler.get_job("bill_generation") or scheduler.add_job(tick, 'cron', month=CONF.scheduler_time.bill_generation_month,day=CONF.scheduler_time.bill_generation_day,hour=CONF.scheduler_time.bill_generation_hour,minute=CONF.scheduler_time.bill_generation_minute, id="bill_generation")
    scheduler.start()

if __name__ == '__main__':
    tick()
#    main()
 
