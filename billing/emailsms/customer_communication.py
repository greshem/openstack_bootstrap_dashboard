# -*- coding:utf-8 -*-
__author__ = 'yamin'
from billing.db.dao.accountDao import AccountDao
from billing.emailsms.email_hand.email_handle import EmailHandle
from billing.emailsms.yuntong.api import sms
from billing.db.sqlalchemy import session as sa
from billing.db.object.models import *
import datetime
from billing.constant.sql import SQL
from oslo_config import cfg
from oslo_log import log as logging
import traceback
LOG = logging.getLogger(__name__)
CONF=cfg.CONF
import pytz
from billing.hander.Account import lowcashReminder_3
from billing.db.dao.bossuserDao import BossUserDao
import traceback
from oslo_log import log as logging
LOG = logging.getLogger(__name__)
class info_center():
    '''
    信息中心,单session
    '''
    _session=None
    @property
    def session(self):
        if not self._session:
            self._session=sa.get_session()
        return self._session

    def _get_today(self):
        return datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    def _get_salesman(self,account):
        salesman_list=BossUserDao().sale_list()
        return [salesman for salesman in salesman_list if account["salesman_id"]==salesman["user_id"]]

    def _get_account_info(self,account_id):
        '''
        获取帐号信息
        :param account_id:
        :return:
        '''
        account_info={}
        account=self.session.query(Account).filter(Account.account_id==account_id).first()
        if account.account_id:#如果存在账户信息
            user_info=self.session.execute(SQL.get_user_info1, {'user_id':account.user_id}).first()
            if user_info is None:
                return None
            account_info={key :getattr(user_info,key) for key in set(user_info._parent.keys)&{"username","telephone","email"}}
            import json
            company_info=json.loads(getattr(user_info,"company_info_json"))
            account_info["company"]=company_info.get("industry")
            account.cash_balance=account.cash_balance if account.cash_balance else 0
            account.gift_balance=account.gift_balance if account.gift_balance else 0
            account.credit_line=account.credit_line if account.credit_line else 0
            account_info["cash_balance"]=account.cash_balance
            account_info["gift_balance"]=account.gift_balance
            account_info["credit_line"]=account.credit_line
            account_info["type"]=account.type
            account_info["available_balance"]=account.cash_balance+account.gift_balance
            account_info["total_balance"]=account.cash_balance+account.gift_balance+account.credit_line
            account_info["available_credit"]=account.credit_line if account.cash_balance>=0 else account.credit_line+account.cash_balance
            account_info["salesman_id"]=account.salesman_id
        return account_info

    def paySuccess(self,order_no,remark=""):
        '''
        根据订单号进行判断以下几种情形，并发送邮件与短信
        1.赠送用户金额，通知客户
        2.用户自己充值完成，通知客户
        3.代理给下线充值完成，通知代理与下线
        4.客服给用户充值完成，通知客户
        order_no:用户号
        info:附加信息
        :return:
        '''
        try:
            info={
                "type":"",#gift，self_recharge,instead_recharge,service_recharge
                "pay_amount":0,#金额
                "receiver":{},#金额的接受者，包括telephone,email，username等信息
                "recharger":{},#施行充值动作的人，包括telephone,email，username等信息
                "senday":self._get_today(),
                "remark":remark
            }
            obj_order=self.session.query(Order).filter(Order.order_no==order_no).first()
            #设置pay_amount和receiver
            info["pay_amount"]=obj_order.amount
            info["receiver"]=self._get_account_info(obj_order.account_id)

            #设置类型，如果代冲值，则设置代理者
            if obj_order.payment_type=="gift":#赠送金额
                return True
                info["type"]="gift"
                #获取gift的单据号码,设置赠送原因
                if not remark:
                    gift_info=self.session.query(Gift).filter(Gift.order_no==order_no).first()
                    info["remark"]=gift_info.remark
                    info["recharger"]={
                        "username":gift_info.gift_by,
                        }
            elif obj_order.payment_type=="recharge":
                obj_recharge=self.session.query(Recharge).filter(Recharge.order_no== order_no).first()
                info["type"]="recharge"
                # if not obj_recharge.is_instead_recharge:#不是代充值
                #     info["type"]="self_recharge"
                # else:
                #     obj_instead=self.session.query(InsteadRecharge).filter(InsteadRecharge.recharge_id==obj_recharge.recharge_id).first()#代理充值单据
                #     recharger_account=obj_instead.instead_recharge_account and self._get_account_info(obj_instead.instead_recharge_account)#代充值的人
                #     if recharger_account:#如果有代充帐号，则表明是代理充值
                #         info["type"]="instead_recharge"
                #         info["recharger"]=recharger_account
                #     else:#客服充值
                #         info["type"]="service_recharge"
                #         info["recharger"]={
                #             "username":obj_instead.instead_recharge_by,
                #         }
            emailSender=EmailHandle()
            smsSender=sms()
            emailSender.pay_success(info)
            smsSender.pay_success(info)
        except Exception as e:
            LOG.error(str(e))
            LOG.error(traceback.format_exc())
            raise e

    def lowcashReminder_3(self):
        self.low_7=[]
        for account in self.session.query(Account).filter(Account.status=='normal').all():
            self._lowcashReminder_3(account.account_id)
        lowcashReminder_3()#提醒用户

    def _lowcashReminder_3(self,account_id):
        '''
        每天检测，检测7天费用以及3天费用，
        7天费用不足给销售提醒
        3天费用不足给客户提醒
        :param account_id:客户帐号
        :return:
        '''
        try:
            account=self._get_account_info(account_id)
            info_3={
                "receiver":account,
                "senday":self._get_today(),
                }
            info_7={
                "account":account,
                "senday":self._get_today(),
                }
            consume_3_day=0
            consume_7_day=0
            consume_6_day=0
            #非cdn项目计费统计值，每小时
            lasthour=(datetime.datetime.utcnow()-datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:00:00")
            amount=self.session.execute(SQL.sql_other_consume, {'account_id':account_id,'lasthour':lasthour}).first()#求统计值
            if amount.amount:
                consume_3_day=amount.amount*24*3
                consume_7_day=amount.amount*24*7
                consume_6_day=amount.amount*24*6
            #cdb带宽计费统计值，每天
            lastday=(datetime.datetime.utcnow()-datetime.timedelta(days=1)).strftime("%Y-%m-%d 00:00:00")
            amount=self.session.execute(SQL.sql_cdn_consume, {'account_id':account_id,'lastday':lastday}).first() #求cdn带宽统计值
            if amount.amount:
                consume_3_day=consume_3_day+amount.amount*3
                consume_7_day=consume_7_day+amount.amount*7
                consume_6_day=consume_6_day+amount.amount*6
            #cdn流量计费统计值 ，每个月 废弃
            # lastmonth=datetime.datetime.strptime((datetime.datetime.utcnow()-datetime.timedelta(days=datetime.datetime.utcnow().day)).strftime('%Y-%m')+"-01","%Y-%m-%d")#上个月第一天
            # import calendar
            # this_day=datetime.datetime.utcnow()
            # month_days=calendar.monthrange(this_day.year,this_day.month)[1]
            # amount=self.session.execute(SQL.sql_cdnflow_consume, {'account_id':account_id,'lastmonth':lastmonth}).first()#求cdn流量统计值
            # if amount.amount:
            #     consume_3_day=consume_3_day+(datetime.datetime.utcnow().day+3)/month_days*amount.amount

            emailSender=EmailHandle()
            smsSender=sms()
            if account["type"]=="normal":#普通用户
                if consume_3_day>account["available_balance"]:
                    emailSender.lowcash_reminder(info_3)
                    smsSender.lowcash_reminder(info_3)
                if consume_7_day>account["available_balance"] and consume_6_day<account["available_balance"]:
                    for each_salesman in self._get_salesman(account):
                        try:
                            info_7["receiver"]=each_salesman
                            info_7["consume_7_day"]=consume_7_day
                            emailSender.lowcash7_reminder(info_7)
                            emailSender.lowcash_reminder(info_3)
                            smsSender.lowcash_reminder(info_3)
                        except Exception as e:
                            LOG.error(str(e))
                            LOG.error(traceback.format_exc())
            else:#信用用户
                if consume_3_day>account["total_balance"]:
                    emailSender.lowcash_reminder(info_3)
                    smsSender.lowcash_reminder(info_3)
                if consume_7_day>account["total_balance"] and consume_6_day<account["available_balance"]:
                    for each_salesman in self._get_salesman(account):
                        try:
                            info_7["receiver"]=each_salesman
                            info_7["consume_7_day"]=consume_7_day
                            emailSender.lowcash7_reminder(info_7)
                            emailSender.lowcash_reminder(info_3)
                            smsSender.lowcash_reminder(info_3)
                        except Exception as e:
                            LOG.error(str(e))
                            LOG.error(traceback.format_exc())
        except Exception as e:
            LOG.error(str(e))
            LOG.error(traceback.format_exc())

    def freezen(self,account_id):
        '''
        冻结
        :return:
        '''
        try:
            info={
                "receiver":self._get_account_info(account_id),
                "senday":self._get_today(),
                }
            emailSender=EmailHandle()
            smsSender=sms()
            emailSender.freeze(info)
            smsSender.freeze(info)
        except Exception as e:
            pass

    def unfreezen(self,account_id):
        '''
        解冻
        :return:
        '''
        return True
        try:
            info={
                "receiver":self._get_account_info(account_id),#金额的接受者，包括telephone,email，username等信息
                "senday":self._get_today(),
                }
            emailSender=EmailHandle()
            smsSender=sms()
            emailSender.unfreeze(info)
            smsSender.unfreeze(info)
        except Exception as e:
            pass

    def credit_adjust(self,account_id):
        '''
        调整信用额度
        :return:
        '''
        return True
        try:
            info={
                "receiver":self._get_account_info(account_id),#金额的接受者，包括telephone,email，username等信息
                "senday":self._get_today(),
                }
            emailSender=EmailHandle()
            smsSender=sms()
            emailSender.credit_adjust(info)
            smsSender.credit_adjust(info)
        except Exception as e:
            pass

    def update_credit(self,account_id):
        '''
            调整用户类型额度
        :return:
        '''
        return True
        try:
            info={
                "receiver":self._get_account_info(account_id),#金额的接受者，包括telephone,email，username等信息
                "senday":self._get_today(),
                }
            emailSender=EmailHandle()
            smsSender=sms()
            emailSender.update_credit(info)
            smsSender.update_credit(info)
        except Exception as e:
            pass

    def del_resource_3(self,account_id,):
        '''
        删除资源提前3天提醒
        :return:
        '''
        try:
            info={
                "receiver":self._get_account_info(account_id),#金额的接受者，包括telephone,email，username等信息
                "senday":self._get_today(),
                }
            emailSender=EmailHandle()
            smsSender=sms()
            emailSender.del3_resource(info)
            smsSender.del3_resource(info)
        except Exception as e:
            pass

    def del_resource(self,account_id):
        '''
        删除资源
        :return:
        '''
        try:
            info={
                "receiver":self._get_account_info(account_id),#金额的接受者，包括telephone,email，username等信息
                "senday":self._get_today(),
                }
            emailSender=EmailHandle()
            smsSender=sms()
            emailSender.del_resource(info)
            smsSender.del_resource(info)
        except Exception as e:
            pass

if __name__=="__main__":
    this_info=info_center()
    this_info.lowcashReminder_3()
    #this_info.freezen("fd6f0af1-9cbc-11e5-be79-fa163ee4b056")
    print ("中文")
    #print ("中文")
    #lowcashReminder_3("fd6f0716-9cbc-11e5-be79-fa163ee4b056")