# -*- coding:utf-8 -*-
import datetime
import threading
from  SMSSDK.CCPRestSDK import REST
from types import MethodType
from oslo_config.cfg import CONF
import logging
class sms():
    SMS_TEMPLATE={
        "problem":27096,#异常精简版
        "server_except":26668,#服务器不可估算的异常
        "server_except1":26246,#服务器异常提醒
        "bill_expires":26098,#STcloud账单到期提醒
        "server_notify":26096,#STcloud云系统通知
        "veri_code_sms":8082,#STcloud云计算验证码通用
        "veri_code_video":8080,#STcloud云视频验证码通用
        "freeze3_common":71538,#冻结前普通用户提醒
        "freeze3_credit":71538,#冻结前信用用户提醒
        "freeze_common":60067,#冻结普通用户提醒
        "freeze_credit":60067,#冻结信用用户提醒
        "recharge_common":60521,#充值普通用户提醒
        "recharge_credit":60521,#充值信用用户提醒
        #"instead_recharge_common":60070,#代充值普通用户
        #"instead_recharge_credit":60070,#代充值信用用户
        #"retailer_common":60071,#分销商帮普通子账户充值
        #"retailer_credit":60071,#分销商为信用子用户充值
        #"unfreeze":60072,#解冻的提醒
        "del3_common":60074,#删除资源普通用户3
        "del3_credit":60074,#删除资源信用用户前3
        "del_common":60075,#删除资源普通用户
        "del_credit":60075,#删除资源信用用户
        #"update_common":55745,#升级普通用户
        #"adjust_credit":55746,#调整信用额度
        "gift_common":60069,#赠送普通用户
        "gift_credit":60069,#赠送信用用户
    }

    @staticmethod
    def get_rest():
        AccountSid='aaf98f89499d24b50149c7033e70174a'
        AccountToken='7645744968d7481b855a37bd248cc79a'
        AppId='aaf98f894e8a784b014e8b15fc12012b'
        SubAccountSid=''
        SubAccountToken=''
        VoIPAccount=''
        VoIPPassword=''
        ServerIP='sandboxapp.cloopen.com'
        ServerPort='8883'
        SoftVersion='2013-12-26'
        Iflog=False #是否打印日志
        Batch=''  #时间戳
        BodyType = 'xml'#包体格式，可填值：json 、xml

        smsrest=REST(ServerIP,ServerPort,SoftVersion)
        smsrest.AccountSid=AccountSid
        smsrest.AccountToken=AccountToken
        smsrest.AppId=AppId
        smsrest.SubAccountSid=SubAccountSid
        smsrest.SubAccountToken=SubAccountToken
        smsrest.VoIPAccount=VoIPAccount
        smsrest.VoIPPassword=VoIPPassword
        smsrest.Iflog=Iflog
        smsrest.Batch=Batch
        smsrest.BodyType=BodyType
        return smsrest

    @staticmethod
    def _para_formatter(to,data):
        return (to.encode("utf-8") if type(to)==unicode else str(to) ,[each.encode("utf-8") if type(each)==unicode else str(each) for each in data ])

    def credit_adjust(self,info):
        '''
        废弃
        普通用户升级为信用用户，或者信用用户信用额度调整
        :param info:
        :return:
        '''
        datas=[
            info["senday"],#
            info["receiver"]["username"],
            info["receiver"]["credit_line"],
            info["receiver"]["cash_balance"],
            info["receiver"]["gift_balance"],
            info["receiver"]["credit_line"],
            info["receiver"]["available_credit"],
            ]
        sms.sendTemplateSMS_threading(info["receiver"]["telephone"],datas,tempId=sms.SMS_TEMPLATE["adjust_credit"])

    def update_credit(self,info):
        '''
        废弃
        :param info:
        :return:
        '''
        datas=[
            info["senday"],#
            info["receiver"]["username"],
            info["receiver"]["cash_balance"],
            info["receiver"]["gift_balance"],
            info["receiver"]["credit_line"],
            info["receiver"]["available_credit"],
            ]
        sms.sendTemplateSMS_threading(info["receiver"]["telephone"],datas,tempId=sms.SMS_TEMPLATE["update_common"])

    def del_resource(self,info):
        '''
        删除普通用户或者信用用户资源提醒
        :param info:
        :return:
        '''
        if info["receiver"]["type"]=="normal":
            datas=[
                info["senday"],#日期
                info["receiver"]["username"],
                info["receiver"]["available_balance"],
                ]
            sms.sendTemplateSMS_threading(info["receiver"]["telephone"],datas,tempId=sms.SMS_TEMPLATE["del_common"])
        else:
            datas=[
                info["senday"],#日期
                info["receiver"]["username"],
                info["receiver"]["available_balance"],
                ]
            sms.sendTemplateSMS_threading(info["receiver"]["telephone"],datas,tempId=sms.SMS_TEMPLATE["del_credit"])

    def del3_resource(self,info):
        '''
        删除普通用户或者信用用户资源前3天提醒
        :param info:
        :return:
        '''
        if info["receiver"]["type"]=="normal":
            datas=[
                info["senday"],#日期
                info["receiver"]["username"],
                info["receiver"]["available_balance"],
                ]
            sms.sendTemplateSMS_threading(info["receiver"]["telephone"],datas,tempId=sms.SMS_TEMPLATE["del3_common"])
        else:
            datas=[
                info["senday"],#日期
                info["receiver"]["username"],
                info["receiver"]["available_balance"],
                ]
            sms.sendTemplateSMS_threading(info["receiver"]["telephone"],datas,tempId=sms.SMS_TEMPLATE["del3_credit"])

    def unfreeze(self,info):
        '''
        解冻提醒
        :param info:
        :return:
        '''
        datas=[

            info["senday"],#日期
            info["receiver"]["username"],
            ]
        sms.sendTemplateSMS_threading(info["receiver"]["telephone"],datas,tempId=sms.SMS_TEMPLATE["unfreeze"])


    def freeze(self,info):
        '''
        冻结普通用户或者信用用户提醒
        :param info:
        :return:
        '''
        if info["receiver"]["type"]=="normal":
            datas=[
                info["senday"],#日期
                info["receiver"]["username"],
                info["receiver"]["available_balance"],
                ]
            sms.sendTemplateSMS_threading(info["receiver"]["telephone"],datas,tempId=sms.SMS_TEMPLATE["freeze_common"])
        else:
            datas=[
                info["senday"],#赠送日期
                info["receiver"]["username"],
                info["receiver"]["available_balance"],
                ]
            sms.sendTemplateSMS_threading(info["receiver"]["telephone"],datas,tempId=sms.SMS_TEMPLATE["freeze_credit"])


    def pay_success(self,info):
        '''
        包括赠送，充值，代充值，普通用户信用用户提醒。
        :param user:
        :return:
        '''
        # if info["type"]=="instead_recharge":
        #     #向经销商发送代充值成功信息
        #     datas=[
        #         info["senday"],
        #         info["receiver"]["username"],
        #         info["pay_amount"],
        #         ]
        #     sms.sendTemplateSMS_threading(info["recharger"]["telephone"],datas,tempId=sms.SMS_TEMPLATE["retailer_common"])

        if info["receiver"]["type"]=="normal":
            if info["type"]=="recharge":
                #向客户发送充值成功信息
                datas=[
                    info["senday"],
                    info["receiver"]["username"],
                    info["pay_amount"],
                    ]
                sms.sendTemplateSMS_threading(info["receiver"]["telephone"],datas,tempId=sms.SMS_TEMPLATE["recharge_common"])
            # if info["type"]=="gift":
            #     #向客户发送赠送成功信息
            #     datas=[
            #         info["senday"],#赠送日期
            #         info["recharger"]["username"],
            #         info["receiver"]["username"],
            #         info["pay_amount"],
            #         ]
            #     sms.sendTemplateSMS_threading(info["receiver"]["telephone"],datas,tempId=sms.SMS_TEMPLATE["gift_common"])
            # elif info["type"]=="self_recharge":
            #     #向客户发送充值成功信息
            #     datas=[
            #         info["senday"],
            #         info["receiver"]["username"],
            #         info["pay_amount"],
            #         ]
            #     sms.sendTemplateSMS_threading(info["receiver"]["telephone"],datas,tempId=sms.SMS_TEMPLATE["recharge_common"])
            # elif info["type"] in ["instead_recharge" ,"service_recharge"]:
            #     #向客户发送代充值成功信息，#向客户发送代充值成功信息，线下充值
            #     datas=[
            #         info["senday"],
            #         info["recharger"]["username"],
            #         info["receiver"]["username"],
            #         info["pay_amount"],
            #         ]
            #     sms.sendTemplateSMS_threading(info["receiver"]["telephone"],datas,tempId=sms.SMS_TEMPLATE["instead_recharge_common"])
        else:
            if info["type"]=="recharge":
                #向客户发送充值成功信息
                datas=[
                    info["senday"],
                    info["receiver"]["username"],
                    info["pay_amount"],
                    ]
                sms.sendTemplateSMS_threading(info["receiver"]["telephone"],datas,tempId=sms.SMS_TEMPLATE["recharge_credit"])
            # if info["type"]=="gift":
            #     #向客户发送赠送成功信息
            #     datas=[
            #         info["senday"],#赠送日期
            #         info["recharger"]["username"],
            #         info["receiver"]["username"],
            #         info["pay_amount"],
            #         ]
            #     sms.sendTemplateSMS_threading(info["receiver"]["telephone"],datas,tempId=sms.SMS_TEMPLATE["gift_credit"])
            #
            # elif info["type"]=="self_recharge":
            #     #向客户发送充值成功信息
            #     datas=[
            #         info["senday"],
            #         info["receiver"]["username"],
            #         info["pay_amount"],
            #         ]
            #     sms.sendTemplateSMS_threading(info["receiver"]["telephone"],datas,tempId=sms.SMS_TEMPLATE["recharge_credit"])
            # elif info["type"] in ["instead_recharge" ,"service_recharge"]:
            #     #向客户发送代充值成功信息，#向客户发送代充值成功信息，线下充值
            #     datas=[
            #         info["senday"],
            #         info["recharger"]["username"],
            #         info["receiver"]["username"],
            #         info["pay_amount"],
            #         ]
            #     sms.sendTemplateSMS_threading(info["receiver"]["telephone"],datas,tempId=sms.SMS_TEMPLATE["instead_recharge_credit"])

    def lowcash_reminder(self,info):
        '''
        冻结前3天提醒，低现金提醒。
        :param info:
        :return:
        '''
        if info["receiver"]["type"]=="normal":
            user_info=info["receiver"]
            datas=[
                info["senday"],#赠送日期
                info["receiver"]["username"],
                info["receiver"]["available_balance"],
                3
                ]
            sms.sendTemplateSMS_threading(user_info["telephone"],datas,tempId=sms.SMS_TEMPLATE["freeze3_common"])
        else:
            user_info=info["receiver"]
            datas=[
                info["senday"],#赠送日期
                info["receiver"]["username"],
                info["receiver"]["available_balance"],
                3
                ]
            sms.sendTemplateSMS_threading(user_info["telephone"],datas,tempId=sms.SMS_TEMPLATE["freeze3_credit"])


    @staticmethod
    def sendTemplateSMS_threading(to,datas,tempId=8082):
        if not CONF.if_sms:return #判断是否需要启动邮件短信模块
        t=threading.Thread(target=sms.sendTemplateSMS,args=(to,datas,tempId))
        t.start()

    # 发送模板短信
    # @param to 手机号码
    # @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 '',该内容格式由模板决定
    # @param $tempId 模板Id
    @staticmethod
    def sendTemplateSMS(to,datas,tempId=8082):
        #if not CONF.if_sms:return #判断是否需要启动邮件短信模块
        rest = sms.get_rest()
        to,datas=sms._para_formatter(to,datas)
        result = rest.sendTemplateSMS(to,datas,tempId)
        if result['statusCode']=="000000":
            logging.warning("sms sender::to "+to+" success")
        else:
            logging.warning("sms sender::to "+to+" fail")
        for k,v in result.iteritems():
            if k=='templateSMS' :
                for k,s in v.iteritems():
                    return '%s:%s' % (k, s)
            else:
                return '%s:%s' % (k, v)


    # 语音验证码
    # @param verifyCode  必选参数   验证码内容，为数字和英文字母，不区分大小写，长度4-8位
    # @param playTimes  可选参数   播放次数，1－3次
    # @param to 必选参数    接收号码
    # @param displayNum 可选参数    显示的主叫号码
    # @param respUrl 可选参数    语音验证码状态通知回调地址，云通讯平台将向该Url地址发送呼叫结果通知
    # @param lang 可选参数    语言类型
    # @param userData 可选参数    第三方私有数据
    @staticmethod
    def voiceVerify(verifyCode,playTimes,to,displayNum,respUrl,lang,userData):
        rest = sms.get_rest()
        result = rest.voiceVerify(verifyCode,playTimes,to,displayNum,respUrl,lang,userData)
        for k,v in result.iteritems():

            if k=='VoiceVerify' :
                for k,s in v.iteritems():
                    print '%s:%s' % (k, s)
            else:
                print '%s:%s' % (k, v)

                #sendTemplateSMS('18721400263',{'12345','5'},message_config["tempId"])

if  __name__=="__main__":
    s=sms()
    print s.sendTemplateSMS(u"18600045500",["2015-11-01","yamin","3","6688"],52460)
    #print sendTemplateSMS("18600045500",["6688",2])
    #print voiceVerify("1234",2,"18600045500","","","","")