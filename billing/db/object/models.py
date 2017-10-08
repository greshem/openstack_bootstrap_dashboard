# -*- coding:utf-8 -*-
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, DateTime, Boolean, Text, DECIMAL
from sqlalchemy import event
from sqlalchemy.orm import relationship
from oslo_config import cfg

from billing.db.sqlalchemy import models
from billing.common import timeutils


CONF = cfg.CONF
BASE = declarative_base()

def MediumText():
    return Text().with_variant(MEDIUMTEXT(), 'mysql')
def init_db():
    BASE.metadata.create_all()



class BillingBase(
    #                 models.SoftDeleteMixin,
    #               models.TimestampMixin,
    models.ModelBase):
    metadata = None

'''
账户
'''
class Account(BASE,BillingBase,models.TimestampMixin):
    __tablename__ = 'account'
    __table_args__ = ()
    account_id = Column(String(64), primary_key=True)
    username = Column(String(64))
    cash_balance = Column(DECIMAL(10,4),default=0)
    gift_balance = Column(DECIMAL(10,4),default=0)
    type = Column(String(32),nullable=False)
    credit_line=Column(DECIMAL(8,2),default=0)
    status = Column(String(32),nullable=False)
    user_id=Column(String(64))
    project_id=Column(String(64))
    frozen_status=Column(String(64))
    frozon_at=Column(DateTime)
    current_month_amount = Column(DECIMAL(10,4),default=0)
    current_month_standard_amount = Column(DECIMAL(10,4),default=0)
    salesman_id= Column(Integer)
    customer_level=Column(String(32))
    company_property=Column(String(64))
    parent_account = Column(String(64))
    #    user_md5=Column(String(64))
    addresses=relationship('Address')
#    billes=relationship('Bill',backref='account')

'''
地址
'''
class Address(BASE,BillingBase,models.TimestampMixin):
    __tablename__ = 'address'
    __table_args__ = ()
    address_id= Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(32))
    address=Column(String(255))
    post_code=Column(String(32))
    phone=Column(String(32))
    mobile=Column(String(32))
    status=Column(String(32))
    account_id=Column(String(64), ForeignKey('account.account_id'),nullable=False)
#    account=relationship('Account',backref='addresses')


'''
账单
'''
class Bill(BASE,BillingBase):
    __tablename__ = 'bill'
    __table_args__ = ()
    bill_id = Column(Integer, primary_key=True,autoincrement=True)
    no =  Column(String(32))
    started_at=Column(DateTime)
    ended_at=Column(DateTime)
    amount=Column(DECIMAL(8,2))
    created_at=Column(DateTime, default=timeutils.utcnow)
    standard_amount=Column(DECIMAL(8,2))
    gift_amount=Column(DECIMAL(8,2))
    type = Column(String(32))
    account_id=Column(String(64), ForeignKey('account.account_id'),nullable=False)
    account=relationship('Account')
    bill_items=relationship('BillItem')


'''
账单项
'''
class BillItem(BASE,BillingBase):
    __tablename__ = 'bill_item'
    __table_args__ = ()
    bill_item_id=Column(Integer, primary_key=True,autoincrement=True)
    resource_id=Column(String(64))
    region_id=Column(String(64))
    resource_name=Column(String(64))
    resource_type = Column(String(32))
    started_at=Column(DateTime)
    ended_at=Column(DateTime)
    amount=Column(DECIMAL(8,2))
    standard_amount=Column(DECIMAL(8,2))
    gift_amount=Column(DECIMAL(8,2))
    created_at=Column(DateTime, default=timeutils.utcnow)
    bill_id=Column(Integer, ForeignKey('bill.bill_id'),nullable=False)
#    bill=relationship('Bill',backref='bill_items')

'''
计费项
'''
class BillingItem(BASE,BillingBase,models.TimestampMixin):
    __tablename__ = 'billing_item'
    __table_args__ = ()
    billing_item_id=Column(Integer, primary_key=True,autoincrement=True)
    region_id=Column(String(64))
    billing_item=Column(String(64),nullable=False)
    unit=Column(String(64))
    price=Column(DECIMAL(10,4))

'''
折扣
'''
class Discount(BASE,BillingBase,models.TimestampMixin):
    __tablename__ = 'discount'
    __table_args__ = ()
    discount_id=Column(Integer, primary_key=True,autoincrement=True)
    discount_ratio=Column(DECIMAL(3,2))
    account_id=Column(String(64), ForeignKey('account.account_id'),nullable=False)
    billing_item_id=Column(Integer, ForeignKey('billing_item.billing_item_id'),nullable=False)
    billing_item=relationship('BillingItem')


'''
消费记录
'''
class Consumption(BASE,BillingBase):
    __tablename__ = 'consumption'
    __table_args__ = ()
    consumption_id=Column(Integer, primary_key=True,autoincrement=True)
    amount=Column(DECIMAL(10,4))
    billing_item=Column(String(64))
    sum=Column(DECIMAL(10,2))
    price=Column(DECIMAL(10,4))
    unit=Column(String(64))
    discount_ratio=Column(DECIMAL(3,2))
    resource_id=Column(String(64),nullable=False)
    resource_name=Column(String(64))
    parent_id=Column(String(64))
    region_id=Column(String(64),nullable=False)
    discounted_at=Column(DateTime,default=timeutils.utcnow)
    discount_by=Column(String(32))
    resource_type=Column(String(32))
    started_at=Column(DateTime)
    ended_at=Column(DateTime)
    standard_amount=Column(DECIMAL(10,4))
    account_id=Column(String(64), ForeignKey('account.account_id'),nullable=False)
    account= relationship('Account')

'''
发票
'''
class Invoice(BASE,BillingBase):
    __tablename__ = 'invoice'
    __table_args__ = ()
    invoice_id=Column(Integer, primary_key=True,autoincrement=True)
    type=Column(String(32))
    title=Column(String(64))
    amount=Column(DECIMAL(8,2))
    prove=Column(String(256))
    apply_at=Column(DateTime, default=timeutils.utcnow)
    status=Column(String(32))
    process_by = Column(String(64))
    post_by=Column(String(64))
    reason=Column(String(256))
    express_no=Column(String(64))
    invoice_no=Column(String(64))
    process_at=Column(DateTime)
    account_id=Column(String(64), ForeignKey('account.account_id'),nullable=False)
    address_id=Column(Integer, ForeignKey('address.address_id'),nullable=False)
    address=relationship('Address')

class Order(BASE,BillingBase,models.TimestampMixin):
    __tablename__ = 'order'
    __table_args__ = ()
    order_no=Column(String(20), primary_key=True)
    account_id=Column(String(64), ForeignKey('account.account_id'),nullable=False)
    payment_type=Column(String(32))
    amount=Column(DECIMAL(8,2))
    status=Column(String(32))
    remark=Column(String(256))

def pay_success_reminder2(order_no):
    def func(session):
        try:
            from billing.emailsms.customer_communication import info_center
            info_center().paySuccess(order_no)#target.dict["order_no"]
        except Exception as e:
            pass
        return True
    return func

@event.listens_for(Order, 'after_insert',raw=True)
@event.listens_for(Order, 'after_update',raw=True)
def pay_success_reminder1(mapper, connection, target):#
    '''
     已经充值成功，给用户发送提醒
    :return:
    '''
    if target.dict["status"]!=target.committed_state["status"] and target.dict["status"]=="pay_success":
        event.listen(target.session,"after_commit",pay_success_reminder2(target.dict["order_no"]) )

# @event.listens_for(Order.status,"set",retval=True)
# def pay_success_reminder2(target, value, oldvalue, initiator):
#     '''
#      已经充值成功，给用户发送提醒
#     :return:
#     '''
#     if value==oldvalue:return value
#     if value=="pay_success":#支付成功
#         try:
#             from billing.emailsms.customer_communication import info_center
#             info_center().paySuccess(target.order_no)
#         except Exception as e:
#             pass
#         return value
# event.listen(Order.status,"set",pay_success_reminder, retval=True)
#
# def insufficient_reminder():
#     '''
#     金额不足时候提醒
#     :return:
#     '''
#     pass

class Recharge(BASE,BillingBase,models.TimestampMixin):
    __tablename__ = 'recharge'
    __table_args__ = ()
    recharge_id=Column(Integer, primary_key=True,autoincrement=True)
    order_no=Column(String(20), ForeignKey('order.order_no'),nullable=False)
    payment_way=Column(String(32))
    receive_account=Column(String(64))
    amount=Column(DECIMAL(8,2))
    status=Column(String(32))
    is_instead_recharge=Column(Boolean)
    remark=Column(String(256))
    pay_at=Column(DateTime)
    order=relationship('Order')

class Gift(BASE,BillingBase,models.TimestampMixin):
    __tablename__ = 'gift'
    __table_args__ = ()
    gift_id=Column(Integer, primary_key=True,autoincrement=True)
    order_no=Column(String(20), ForeignKey('order.order_no'),nullable=False)
    gift_by=Column(String(64))
    amount=Column(DECIMAL(8,2))
    status=Column(String(32))
    remark=Column(String(256))
    gift_at=Column(DateTime,default=timeutils.utcnow)
    order=relationship('Order')

class AlipayInfo(BASE,BillingBase,models.TimestampMixin):
    __tablename__ = 'alipay_info'
    __table_args__ = ()
    alipay_info_id=Column(Integer, primary_key=True,autoincrement=True)
    recharge_id=Column(Integer, ForeignKey('recharge.recharge_id'),nullable=False)
    order_no=Column(String(20),nullable=False)
    payer=Column(String(32))
    pay_account=Column(String(64))
    amount=Column(DECIMAL(8,2))
    trade_no=Column(String(64))
    status=Column(String(32))
    email=Column(String(64))
    phone=Column(String(32))
    remark=Column(String(256))
    pay_at=Column(DateTime,default=timeutils.utcnow)
    bank_no=Column(String(64))
#    recharge=relationship('Recharge')

class InsteadRecharge(BASE,BillingBase,models.TimestampMixin):
    __tablename__ = 'instead_recharge'
    __table_args__ = ()
    instead_recharge_id=Column(Integer, primary_key=True,autoincrement=True)
    recharge_id=Column(Integer, ForeignKey('recharge.recharge_id'),nullable=False)
    instead_recharge_by=Column(String(32))
    instead_recharge_account=Column(String(64))
    remark=Column(String(256))
    recharge=relationship('Recharge')

class TransferInfo(BASE,BillingBase,models.TimestampMixin):
    __tablename__ = 'transfer_info'
    __table_args__ = ()
    transfer_info_id=Column(Integer, primary_key=True,autoincrement=True)
    recharge_id=Column(Integer, ForeignKey('recharge.recharge_id'),nullable=False)
    trade_no=Column(String(64))
    remittance_account=Column(String(128))
    remittance_bank=Column(String(256))
    remittance_way=Column(String(64))
    remittance_at=Column(DateTime)
    remittance_remark=Column(String(256))
    remittance_corporation=Column(String(128))
    inward_account=Column(String(128))
    inward_bank=Column(String(256))
    inward_at=Column(DateTime)
    inward_corporation=Column(String(128))
    amount=Column(DECIMAL(8,2))
    
    #
    #
    # class CDNDomain() :
    #     tenant_id = Column(Integer)
    #     domain_id = Column(Integer)
    #     domain_name = Column(String(32))
    #     domain_cname = Column(String(32))
    #     create_time = Column(DateTime)
    #     source_type = Column(String(32))
    #     status = Column(String(32))
    #     enable = Column(String(32))



    #
    #class User(BASE,SearchBase,models.TimetampDefault):
    #    """Represents a running service on a host."""
    #
    #    __tablename__ = 'user'
    #    __table_args__ = ()
    #
    #    id = Column(Integer, primary_key=True,autoincrement=True)
    #    username = Column(String(100),nullable=False)
    #    password = Column(String(100))
    #    realname = Column(String(255))
    #    phone = Column(String(50))
    #    telephone = Column(Integer)
    #    email = Column(String(100))
    #    comment = Column(String(4000))
    #    type=Column(String(50))
    #    state=Column(String(50))
    #    isAdmin=Column(Boolean)
    ##    createTime = Column(DateTime, default=timeutils.utcnow,
    ##                              nullable=False)
    ##    updateTime = Column(DateTime, default=timeutils.utcnow,
    ##                              nullable=False)
    #
    #
    #class Core(BASE,SearchBase,models.TimetampDefault):
    #    __tablename__ = 'core'
    #    __table_args__ = ()
    #    id = Column(Integer, primary_key=True,autoincrement=True)
    #    core=Column(String(255),nullable=False)
    #    corePath=Column(String(255))
    #
    #
    #class Corporation(BASE,SearchBase,models.TimetampDefault):
    #    __tablename__ = 'corporation'
    #    __table_args__ = ()
    #    id = Column(Integer, primary_key=True,autoincrement=True)
    #    name=Column(String(255),nullable=False)
    #    info=Column(MediumText())
    #
    #
    #class Role(BASE,SearchBase,models.TimetampDefault):
    #    __tablename__ = 'role'
    #    __table_args__ = ()
    #    id = Column(Integer, primary_key=True,autoincrement=True)
    #    roleName=Column(String(100),nullable=False)
    #    roleId=Column(String(100),nullable=False)
    #
    #
    #class CoreCorporation(BASE,SearchBase,models.TimetampDefault):
    #    __tablename__ = 'core_corporation'
    #    __table_args__ = ()
    #    id = Column(Integer, primary_key=True,autoincrement=True)
    #    coreId=Column(Integer,ForeignKey('core.id'),nullable=False)
    #    corporationId=Column(Integer,ForeignKey('corporation.id'),nullable=False)
    #
    #class UserCorporation(BASE,SearchBase,models.TimetampDefault):
    #    __tablename__ = 'user_corporation'
    #    __table_args__ = ()
    #    id = Column(Integer, primary_key=True,autoincrement=True)
    #    userId=Column(Integer,ForeignKey('user.id'),nullable=False)
    #    corporationId=Column(Integer,ForeignKey('corporation.id'),nullable=False)
    #
    #class UserRole(BASE,SearchBase,models.TimetampDefault):
    #    __tablename__ = 'user_role'
    #    __table_args__ = ()
    #    id = Column(Integer, primary_key=True,autoincrement=True)
    #    userId=Column(Integer,nullable=False)
    #    roleId=Column(String(100),nullable=False)
    #
    #class Resource(BASE,SearchBase,models.TimetampDefault):
    #    __tablename__ = 'resource'
    #    __table_args__ = ()
    #    id = Column(Integer, primary_key=True,autoincrement=True)
    #    name=Column(String(255))
    #    desc=Column(MediumText())
    #    type=Column(String(50))
    #    coreId=Column(Integer)
    #    state=Column(String(50))
    #    docId=Column(String(100))
    #    scanSum=Column(Integer,default=0)
    #    downloadSum=Column(Integer,default=0)
    #    searchSum=Column(Integer,default=0)
    #
    #class LogAction(BASE,SearchBase,models.TimetampDefault):
    #    __tablename__ = 'log_action'
    #    __table_args__ = ()
    #    id = Column(Integer, primary_key=True,autoincrement=True)
    #    action=Column(String(255))
    #    userId=Column(Integer)
    #    username=Column(String(100))
    #    hostIp=Column(String(100))
    #    info=Column(MediumText())
    #
    #class log_data(BASE,SearchBase,models.TimetampDefault):
    #    __tablename__ = 'log_data'
    #    __table_args__ = ()
    #    id = Column(Integer, primary_key=True,autoincrement=True)
    #    docId=Column(String(100),nullable=False)
    #    coreId=Column(Integer)
    #    action=Column(String(100))
    #    info=Column(MediumText())
    #    userId=Column(Integer)
    #    username=Column(String(100))
    #
    #class Token(BASE,SearchBase,models.TimetampDefault):
    #    __tablename__ = 'token'
    #    __table_args__ = ()
    #    id = Column(Integer, primary_key=True,autoincrement=True)
    #    token=Column(String(50),nullable=False)
    #    userId=Column(Integer)
    #    username=Column(String(100))

class WorkOrder(BASE,BillingBase,models.TimestampMixin):
    __tablename__ = 'workorder'
    __table_args__ = ()
    id=Column("workoder_id",Integer, primary_key=True,autoincrement=True)
    workorder_no=Column(String(32))
    workordertype=Column("workorder_type_id",Integer, ForeignKey('workorder_type.workorder_type_id'),nullable=False)
    apply_by=Column(String(64), ForeignKey('account.account_id'),nullable=False)
    apply_source=Column(String(32))
    theme=Column(String(256))
    content=Column(String(4000))
    status=Column(String(32))
    apply_at=Column(DateTime, default=timeutils.utcnow)
    lasthandled_at=Column(DateTime, onupdate=timeutils.utcnow)
    lasthandled_by=Column(String(64), ForeignKey('account.account_id'),nullable=False)
    records=relationship('WorkOrderRecord',order_by="desc(WorkOrderRecord.record_at)")
    type=relationship('WorkOrderType')

class WorkOrderRecord(BASE,BillingBase,models.TimestampMixin):
    __tablename__ = 'workorder_record'
    __table_args__ = ()
    id=Column("workorder_record_id",Integer, primary_key=True,autoincrement=True)
    workorder=Column("workorder_id",Integer, ForeignKey('workorder.workoder_id'),nullable=False)
    record_by=Column(String(64), ForeignKey('account.account_id'),nullable=False)
    content=Column(String(4000))
    status=Column(String(32))
    record_at=Column(DateTime, default=timeutils.utcnow)
    order=relationship("WorkOrder")

class WorkOrderType(BASE,BillingBase,models.TimestampMixin):
    '''
    code name
    consult 商务咨询工单
    function 功能咨询工单
    error 故障工单
    finance 财务,发票工单
    payment 催款工单
    regionQuota 区域,配额申请工单
    others 其他
    '''
    __tablename__ = 'workorder_type'
    __table_args__ = ()
    id=Column("workorder_type_id",Integer, primary_key=True,autoincrement=True)
    name=Column(String(64))
    code=Column(String(32))
    remark=Column(String(256))

# add by zhangaw
class Advert(BASE,BillingBase,models.TimestampMixin):
    __tablename__ = 'advert'
    __table_args__ = ()
    advert_id=Column(Integer,primary_key=True,autoincrement=True)
    title=Column(String(256))
    url=Column(String(256))
    started_at=Column(DateTime)
    ended_at=Column(DateTime)

# *** add by zhangaw ***
'''
返现账单
'''
class RebateBill(BASE,BillingBase):
    __tablename__ = 'rebate_bill'
    __table_args__ = ()
    rebate_bill_id = Column(Integer,primary_key=True,autoincrement=True)
    account_id = Column(String(64))
    no = Column(String(32))
    started_at = Column(DateTime)
    ended_at = Column(DateTime)
    rebate_amount = Column(DECIMAL(8,2),default=0.00)
    subaccount_amount = Column(DECIMAL(8,2),default=0.00)
    subaccount_gift_amount = Column(DECIMAL(8,2),default=0.00)
    created_at = Column(DateTime,default=timeutils.utcnow())
    rebate_subbills = relationship('RebateSubBill')

'''
返现账单项
'''
class RebateBillItem(BASE,BillingBase):
    __tablename__ = 'rebate_bill_item'
    __table_args__ = ()
    rebate_bill_item = Column(Integer,primary_key=True,autoincrement=True)
    rebate_subbill_id = Column(Integer,ForeignKey('rebate_subbill.rebate_subbill_id'))
    resource_id = Column(String(64))
    resource_name = Column(String(64))
    resource_type = Column(String(32))
    region_id = Column(String(64))
    amount = Column(DECIMAL(8,2))
    gift_amount = Column(DECIMAL(8,2))
    rebate_amount = Column(DECIMAL(8,2))
    started_at = Column(DateTime)
    ended_at = Column(DateTime)
    created_at = Column(DateTime,default=timeutils.utcnow())

'''
返现子账单
'''
class RebateSubBill(BASE,BillingBase):
    __tablename__ = 'rebate_subbill'
    __table_args__ = ()
    rebate_subbill_id = Column(Integer,primary_key=True,autoincrement=True)
    rebate_bill_id = Column(Integer,ForeignKey('rebate_bill.rebate_bill_id'),nullable=False)
    account_id = Column(String(64),nullable=False)
    rebate_amount = Column(DECIMAL(8,2),default=0.00)
    amount = Column(DECIMAL(8,2),default=0.00)
    gift_amount = Column(DECIMAL(8,2),default=0.00)
    started_at = Column(DateTime)
    ended_at = Column(DateTime)
    created_at = Column(DateTime,default=timeutils.utcnow())
    rebate_bill_items = relationship('RebateBillItem')
# *** end ***
