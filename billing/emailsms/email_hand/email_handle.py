# --*-- coding: utf-8 --*--
__author__ = 'yamin'

from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
import smtplib
import datetime
import threading
from jinja2 import Environment, PackageLoader
from billing.emailsms.email_hand.user_interface import default_user
from oslo_config import cfg
import logging
CONF = cfg.CONF


class EmailHandle:
    '''

    '''
    def __init__(self,user_info=None):
        if user_info:
            self.user=user_info
        elif CONF.email_user:
            self.user=CONF.email_user
        else:
            self.user=default_user
        self.env = Environment(loader=PackageLoader('billing.emailsms.email_hand', 'templates'))
        self.mu = threading.Lock()
    #  格式化参数
    @staticmethod
    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(),addr.encode('utf-8') if isinstance(addr, unicode) else addr))

    def read_content(self):
        pass

    def write_content(self,template_name,context):
        '''
        通过模板生成html
        :param template_dir:
        :param context:
        :return:
        '''
        template=self.env.get_template(template_name)
        return template.render(context)

    def send_email_threading(self,receiver,title,html_obj):
        if not CONF.if_email:return #判断是否需要启动邮件短信模块
        t=threading.Thread(target=EmailHandle.send_email,args=(self,receiver,title,html_obj))
        t.start()

    def unicode2str(self,str1):
        return str1.encode("utf-8") if type(str1)==unicode else str(str1)

    def send_email(self,receiver,title,html_obj):
        # 邮件头
        self.mu.acquire()
        try:
            if not CONF.if_email:return #判断是否需要启动邮件短信模块
            msg = MIMEMultipart('alternative')
            msg['From'] = formataddr((self.user["username"],self.user["email"]))
            msg['To'] = formataddr((self.unicode2str(receiver["username"]),self.unicode2str(receiver["email"])))
            msg['Subject'] = title
            #msg['Cc'] = cc_addr
            # 邮件正文是MIMEText:
            # msg.attach(MIMEText('send with file...', 'plain', 'utf-8'))
            # msg.attach(MIMEText(''))
            msg.attach(MIMEText(html_obj,'html','utf-8'))

            # 发送邮件
            
            self.login_server()
            self.server.sendmail(msg['From'], msg['To'], msg.as_string())
            self.server.quit()
            logging.warning("email sender::to "+msg['To']+" success")
            self.mu.release()
            return True
        except Exception, e:
            self.mu.release()
            logging.warning("email sender::to "+msg['To']+" fail")
            print str(e)
            return False

    def receive_email(self):
        pass

    def login_server(self):
        self.server = smtplib.SMTP(self.user["smtp_server"], 25)
        #self.server.set_debuglevel(1)
        self.server.login(self.user["email"], self.user["password"])
        return self.server

    def quit_server(self):
        self.server.quit()

    def send_change_pas(self,receiver,change_password_url):
        '''
        receiver:{"name":"","email":""}
        :param receiver:
        :return:
        '''
        context={
            "receiver":receiver,
            "sender":self.user,
            "senday":datetime.datetime.today(),
            "random_url":change_password_url
        }
        self.send_email(receiver,"STcloud云(stcloud.cn)网站密码重置",self.write_content("change_pas.html",context))

    def send_success_reg(self,receiver):
        context={
            "receiver":receiver,
            "sender":self.user,
            "senday":datetime.datetime.today(),
        }
        self.send_email(receiver,"STcloud云(stcloud.cn)恭喜您注册成功!",self.write_content("success_reg.html",context))

    def pay_success(self,info):
        '''

        :param info:支付信息
        :return:
        '''
        info.update({"sender":self.user})
        receiver=info["receiver"]
        if info["type"]=="recharge":
            self.send_email_threading(receiver,"STcloud云(stcloud.cn)充值成功!",self.write_content("self_recharge_success.html",info))
        # if info["type"]=="gift":
        #     self.send_email_threading(receiver,"STcloud云(stcloud.cn)赠送!",self.write_content("gift_success.html",info))
        # elif info["type"]=="self_recharge":
        #     self.send_email_threading(receiver,"STcloud云(stcloud.cn)充值成功!",self.write_content("self_recharge_success.html",info))
        # elif info["type"]=="instead_recharge":
        #     if not CONF.if_email:return #判断是否需要启动邮件短信模块
        #     self.send_email_threading(info["receiver"],"STcloud云(stcloud.cn)充值成功!",self.write_content("instead_recharge_success1.html",info))#给接收者
        #     self.send_email_threading(info["recharger"],"STcloud云(stcloud.cn)代充值成功!",self.write_content("instead_recharge_success2.html",info))##给代理商
        # else:#客服线下充值
        #     self.send_email_threading(receiver,"STcloud云(stcloud.cn)充值成功!",self.write_content("instead_recharge_success1.html",info))#给接收者

    def lowcash7_reminder(self,info):
        '''
        对销售人员发送一份7天不足费用人员名单
        :return:
        '''
        info.update({"sender":self.user})
        receiver=info["receiver"]
        self.send_email_threading(receiver,"STcloud云(stcloud.cn)欠费前7天用户列表!",self.write_content("freeze7.html",info))

    def lowcash_reminder(self,info):
        info.update({"sender":self.user})
        receiver=info["receiver"]
        self.send_email_threading(receiver,"STcloud云(stcloud.cn)欠费提前通知!",self.write_content("freeze3.html",info))

    def freeze(self,info):
        info.update({"sender":self.user})
        self.send_email(info["receiver"],"STcloud云(stcloud.cn)冻结通知!",self.write_content("freeze.html",info))

    def unfreeze(self,info):
        info.update({"sender":self.user})
        self.send_email_threading(info["receiver"],"STcloud云(stcloud.cn)解冻通知!",self.write_content("unfreeze.html",info))

    def del_resource(self,info):
        info.update({"sender":self.user})
        self.send_email_threading(info["receiver"],"STcloud云(stcloud.cn)删除资源通知!",self.write_content("del.html",info))

    def del3_resource(self,info):
        info.update({"sender":self.user})
        self.send_email_threading(info["receiver"],"STcloud云(stcloud.cn)删除资源提前3天通知!",self.write_content("del3.html",info))

    def credit_adjust(self,info):
        info.update({"sender":self.user})
        self.send_email_threading(info["receiver"],"STcloud云(stcloud.cn)信用调整通知!",self.write_content("credit_adjust.html",info))

    def update_credit(self,info):
        info.update({"sender":self.user})
        self.send_email_threading(info["receiver"],"STcloud云(stcloud.cn)升级用户通知!",self.write_content("credit_adjust.html",info))

if __name__=="__main__":
    from billing.emailsms.email_hand import user_interface
    emailman=EmailHandle()
    receiver={"username":"min","email":"yamin_xu@163.com"}
    emailman.send_success_reg(receiver)