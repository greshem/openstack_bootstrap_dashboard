# -*- coding:utf-8 -*-
'''
Created on 2015-8-21

@author: greshem
账户数据库操作类
'''
from billing.db.sqlalchemy import session as sa
from billing.db.object.models import Account
from billing.db.Pagination import Pagination
from oslo_log import log as logging
from billing.util.handlerUtil import *
from billing.constant.sql import SQL
import json
from billing.util.tzUtil import change2UTC,datetime2Str
import datetime

LOG = logging.getLogger(__name__)

class AccountDao():
    def __init__(self, account=None):
        self.account = account
    
    def getQuery(self, session=None):
        if not session:
            session = sa.get_session()
        return session.query(Account)
    
    def getQueryByCondition(self, condition=None, likeCondition=None, session=None):
        '''条件查询'''
        if not session:
            session = sa.get_session()
        if condition is None and likeCondition is None:
            return session.query(Account)
        query = session.query(Account)
        if condition:
            for (attr, attrValue) in [(key, value)for (key, value) in condition.items()]:
                if attr == 'type':
                    query = query.filter(Account.type == attrValue)
                if attr == 'status':
                    query = query.filter(Account.status == attrValue)
        if likeCondition:
            for (attr, attrValue) in [(key, value)for (key, value) in likeCondition.items()]:
                if attr == 'username':
                    query = query.filter(Account.username.like('%' + attrValue + '%'))
        return query

    def list(self, condition=None, likeCondition=None, session=None):
        '''按条件查询所有的账户'''
        if not session:
            session = sa.get_session()
        query = self.getQueryByCondition(condition, likeCondition)
        rows = query.all()
#        session.close()
        return rows
    
    def getAccountByPage(self, query=None, page_no=1, page_size=15, edge_size=0, session=None):
        ''' 分页查询'''
        if not session:
            session = sa.get_session()
        if query is None:
            query = self.getQuery(session)
        pagination = Pagination(query)
        return pagination.paginate(page_no, page_size, edge_size)
    
    def add(self, session=None):
        '''添加账户'''
        try:
            if not session:
                session = sa.get_session()
            session.add(self.account)
            session.flush()
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e
    
    def update(self, values, session=None):
        """数据更新"""
        try:
            if not session:
                session = sa.get_session()
            session.begin()
            self.account = session.query(Account).filter(Account.account_id == self.account.account_id).first()
            self.account.update(values)
            session.commit()
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e
        
    def detail(self, session=None):
        '''账号详情'''
        try:
            if not session:
                session = sa.get_session()
            self.account = session.query(Account).filter(Account.account_id == self.account.account_id).first()
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e

    def detail_dict(self, session=None):
        '''账号详情:包括account，user，区域等信息'''
        try:
            if not session:
                session = sa.get_session()
            self.account = session.query(Account).filter(Account.account_id == self.account.account_id).first()
            project_id=self.account.project_id
            user_info=session.execute(SQL.get_user_info, {'project_id':project_id}).first()
            user_id=user_info and user_info.user_id
            region_info_list=user_id and session.execute(SQL.get_region_info, {'user_id':user_id}).fetchall()
            self.user_info={}
            self.region_info={}
            if user_info:
                self.user_info=row2dict(user_info)
            #判断这个账户是否分销商，还是普通用户，还是分销商的子账户
            if not user_info:
                pass
            elif self.user_info["role_name"]=="project_admin":
                self.user_info["sale_type"]="distributor"
            elif self.user_info["role_name"] in ["user", '_member_']:
                if self.user_info["parent_role_name"]=="proejct_admin":
                    self.user_info["sale_type"]="distributor_user"
                elif self.user_info["parent_role_name"] in ['admin', 'register']:
                    self.user_info["sale_type"]="ordinary"
                else:
                    self.user_info["sale_type"]="error"
            else:
                self.user_info["sale_type"]="error"
            if region_info_list:
                self.region_info=[row2dict(row) for row in region_info_list]
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e

    def delete(self, session=None):
        try:
            if not session:
                session = sa.get_session()
            session.begin()
            self.account = session.query(Account).filter(Account.account_id == self.account.account_id).first()
            self.account.status = 'deleted'
            session.commit()
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e
    
    def getAccountByUserID(self, user_id, session=None):
        '''根据user的ID查找账号'''
        try:
            if not session:
                session = sa.get_session()
            self.account = session.query(Account).filter(Account.user_id == user_id).first()
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e
        
    def getUserById(self,user_id,session=None):
        '''根据user的ID查找用户'''
        try:
            if not session:
                session = sa.get_session()
            user=session.execute('select * from keystone.user where id=:user_id',{'user_id':user_id}).first()
            if user:
                return dict(zip(user.keys(), user.values()))
            return None
        except Exception as e:
            session.close()
            LOG.error(str(e))
#            raise e

    def getParentUserById(self,user_id,session=None):
        '''根据user的ID查找父用户'''
        try:
            if session is None:
                session = sa.get_session()
            user=session.execute('select pu.* from keystone.user u  join keystone.user pu on u.parent_id=pu.id where u.id=:user_id',{'user_id':user_id}).first()
            if user:
                return dict(zip(user.keys(), user.values()))
            return None
        except Exception as e:
            session.close()
            LOG.error(str(e))
    
    def getAccountByProjectId(self, project_id, session=None):
        '''根据user的ID查找账号'''
        try:
            if not session:
                session = sa.get_session()
            self.account = session.query(Account).filter(Account.project_id == project_id).first()
        except Exception as e:
            session.close()
            LOG.error(str(e))
            raise e
    
    def getSubAccountComsump(self, parent_id, session=None):
        if session is None:
            session = sa.get_session()
        adminrow=session.execute(SQL.checkAdmin,{'user_id':parent_id}).first()
        if adminrow:
            query = session.execute(SQL.admin_subAccountSum)
        else:
            query = session.execute(SQL.subAccountSum, {'parent_id':parent_id})
        row = query.first()
        session.close()
        return {'sum':row.sum, 'credit_sum':row.credit_sum}
    
    def subAccountList(self, parent_id, condition=None, page_no=1, page_size=15, session=None):
        if session is None:
            session = sa.get_session()
        adminrow=session.execute(SQL.checkAdmin,{'user_id':parent_id}).first()
        isAdmin=False
        if adminrow:
            isAdmin=True
        if condition is None:
            condition = {}
        count = session.execute(self.subAccountListCount(condition,isAdmin=isAdmin),dict({'parent_id':parent_id}, **condition)).first().total_sum
        query = session.execute(self.subAccountListSql(condition,isAdmin=isAdmin), dict({'parent_id':parent_id, 'offset':page_size * (page_no - 1), 'page_size':page_size}, **condition))
        rows = query.fetchall()
        result = []
        if rows:
            for row in rows:
                extra = json.loads(row.extra) if row.extra else {}
                company = row.company
                if company is None and extra.has_key('company'):
                    company = extra['company']
                result.append({'account_id':row.account_id,'project_id':row.project_id ,'user_id':row.user_id, 'name':row.name, 'email':row.email, 'telephone':row.telephone, \
                               'cash_balance':row.cash_balance, 'gift_balance':row.gift_balance, 'type':row.type, 'credit_line':row.credit_line, 'company':company})
        session.close()
        return result, count

    def ProjectAdminsubAccountList(self, parent_id, condition=None, session=None):
        if session is None:
            session = sa.get_session()
        if condition is None:
            condition = {}

        sql=SQL.subAccountList_business
        sql+=' order by created_at desc'
        query = session.execute(sql, dict({'parent_id':parent_id}, **condition))
        rows = query.fetchall()
        count=len(rows)

        if condition:
            if condition.has_key('limit') and condition.has_key('offset'):
                limit=int(condition['limit'])
                offset=int(condition['offset'])
                rows=rows[(limit*offset):((offset+1)*limit)]
        result = []
        for row in rows:
            extra = json.loads(row.extra) if row.extra else {}
            company = row.company
            if company is None and extra.has_key('company'):
                company = extra['company']
            result.append({'account_id':row.account_id, 'user_id':row.user_id, 'username':row.name, 'email':row.email, 'telephone':row.telephone, \
                           'cash_balance':row.cash_balance, 'gift_balance':row.gift_balance, 'type':row.type, 'credit_line':row.credit_line, 'company':company,
                           'role': 'project_subaccount', 'created_at': row.created_at, 'sales': row.sales_name, 'status': row.status})
        session.close()
        return result, count

    def subAccountListCount(self, condition=None,isAdmin=False):
        sql = SQL.subAccountListCount
        if isAdmin:
            sql=SQL.admin_subAccountListCount
        sql = self._getConditionSql(sql, condition)
        return sql
    
    def subAccountListSql(self, condition=None,isAdmin=False):
        sql = SQL.subAccountList
        if isAdmin:
            sql=SQL.admin_subAccountList
        sql = self._getConditionSql(sql, condition)
        return sql + " limit :offset,:page_size"
    
    def _getConditionSql(self, sql, condition=None):
        if condition:
            for key, value in condition.items():
                if key == 'type':
                    sql += " and account.type=:type"
                if key == 'name':
                    sql += " and account.username=:name"
                if key == 'max_cash':
                    sql += " and account.cash_balance<=:max_cash"
                if key == 'min_cash':
                    sql += " and account.cash_balance>=:min_cash"
                if key == 'max_gift':
                    sql += " and account.gift_balance<=:max_gift"
                if key == 'min_gift':
                    sql += " and account.gift_balance>=:min_gift"
                if key == 'max_credit':
                    sql += " and account.credit_line<=:max_credit"
                if key == 'min_credit':
                    sql += " and account.credit_line>=:min_credit"
        return sql
    
    def subAccountDetail(self, account_id, session=None):
        if session is None:
            session = sa.get_session()
        query = session.execute(SQL.subAccountDetail, {'account_id':account_id})
        row = query.first()
        session.close()
        if row:
            extra = json.loads(row.extra) if row.extra else {}
            company = None
            contact = None
            if extra.has_key('company'):
                company = extra['company']
            if extra.has_key('contact'):
                contact = extra['contact']
            return {'account_id':row.account_id, 'user_id':row.user_id, 'name':row.name, 'email':row.email, 'telephone':row.telephone, \
                    'contact':contact, 'cash_balance':row.cash_balance, 'gift_balance':row.gift_balance, 'type':row.type, 'credit_line':row.credit_line, 'company':company}
        return None
    
    def subAccountAmountSum(self, parent_id, started_at, ended_at, session=None):
        if session is None:
            session = sa.get_session()
        adminrow=session.execute(SQL.checkAdmin,{'user_id':parent_id}).first()
        if adminrow:
            if datetime2Str(started_at)==change2UTC(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m')+'-01',format='%Y-%m-%d') and datetime2Str(datetime2Str(ended_at,outformat='%Y-%m-%d %H'),informat='%Y-%m-%d %H')==change2UTC(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H'),format='%Y-%m-%d %H'):
                query = session.execute(SQL.admin_subAccountCurrentMonthAmountSum, {'parent_id':parent_id})
            else:
                query = session.execute(SQL.admin_subAccountAmountSum, {'parent_id':parent_id,'started_at':started_at, 'ended_at':ended_at})
        else:
            if datetime2Str(started_at)==change2UTC(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m')+'-01',format='%Y-%m-%d') and datetime2Str(datetime2Str(ended_at,outformat='%Y-%m-%d %H'),informat='%Y-%m-%d %H')==change2UTC(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H'),format='%Y-%m-%d %H'):
                query = session.execute(SQL.subAccountCurrentMonthAmountSum, {'parent_id':parent_id, 'started_at':started_at, 'ended_at':ended_at})
            else:
                query = session.execute(SQL.subAccountAmountSum, {'parent_id':parent_id, 'started_at':started_at, 'ended_at':ended_at})     
        row = query.first()
        if row:
            return {'amount_total':row.amount_total, 'standard_amount_total':row.standard_amount_total}
        session.close()
        return {}
    
    def changeCreditLine(self,account_id,credit_line,session=None):
        '''调整信用额度'''
        if session is None:
            session=sa.get_session()
        session.begin()
        account = session.query(Account).filter(Account.account_id == account_id).first()
        account.credit_line=credit_line
        session.flush()
        self._make_frozen(account.account_id,session)
        session.commit()
        from billing.emailsms.customer_communication import info_center
        infocenter=info_center()
        infocenter.credit_adjust(account_id)
        return account
    
    def change2Credit(self,account_id,credit_line,session=None):
        '''普通用户升级为信用用户'''
        if session is None:
            session=sa.get_session()
        session.begin()
        account = session.query(Account).filter(Account.account_id == account_id).first()
        account.type='credit'
        account.credit_line=credit_line
        session.flush()
        self._make_frozen(account.account_id,session)
        session.commit()
        from billing.emailsms.customer_communication import info_center
        infocenter=info_center()
        infocenter.update_credit(account_id)
        return account
    
    def checkAdmin(self,account_id,session=None):
        if session is None:
            session=sa.get_session()
        account = session.query(Account).filter(Account.account_id == account_id).first()
        if account:
            user=session.execute(SQL.checkAdmin,{'user_id':account.user_id}).first()
            if user:
                return True
        return False
    
    def get_account_info(self,account_id,session=None):
        '''
        获取帐号信息
        :param account_id:
        :return:
        '''
        if session is None:
            session=sa.get_session()
        account_info={}
        account=session.query(Account).filter(Account.account_id==account_id).first()
        if account:#如果存在账户信息
#            user_info=self.session.execute(SQL.get_user_info1, {'user_id':account.user_id}).first()
#            account_info={key :getattr(user_info,key) for key in set(user_info._parent.keys)&{"username","telephone","email"}}
            account.cash_balance=account.cash_balance if account.cash_balance else 0
            account.gift_balance=account.gift_balance if account.gift_balance else 0
            account.credit_line=account.credit_line if account.credit_line else 0
            account_info["account_id"]=account.account_id
            account_info["cash_balance"]=account.cash_balance
            account_info["gift_balance"]=account.gift_balance
            account_info["credit_line"]=account.credit_line
            account_info["type"]=account.type
            account_info["available_balance"]=account.cash_balance+account.gift_balance
            account_info["total_balance"]=account.cash_balance+account.gift_balance+account.credit_line
            account_info["available_credit"]=account.credit_line if account.cash_balance>=0 else account.credit_line+account.cash_balance
        return account_info
            
    def lowcashReminder_3(self,account_id,session=None):
        '''
        当前余额比较低的时候提前三天给客户提醒
        :param account_id:客户帐号
        :return:
        '''
        if session is None:
            session=sa.get_session()
        try:
            account=self.get_account_info(account_id,session)
            consume_3_day=0
            #非cdn项目计费统计值，每小时
            lasthour=(datetime.datetime.utcnow()-datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:00:00")
            amount=session.execute(SQL.sql_other_consume, {'account_id':account_id,'lasthour':lasthour}).first()#求统计值
            if amount.amount:
                consume_3_day=amount.amount*24*3

            #cdb带宽计费统计值，每天
            lastday=(datetime.datetime.utcnow()-datetime.timedelta(days=1)).strftime("%Y-%m-%d 00:00:00")
            amount=session.execute(SQL.sql_cdnbandw_consume, {'account_id':account_id,'lastday':lastday}).first() #求cdn带宽统计值
            if amount.amount:
                consume_3_day=consume_3_day+amount.amount*3

            #cdn流量计费统计值 ，每个月
            lastmonth=datetime.datetime.strptime((datetime.datetime.utcnow()-datetime.timedelta(days=datetime.datetime.utcnow().day)).strftime('%Y-%m')+"-01","%Y-%m-%d")#上个月第一天
            import calendar
            this_day=datetime.datetime.utcnow()
            month_days=calendar.monthrange(this_day.year,this_day.month)[1]
            amount=session.execute(SQL.sql_cdnflow_consume, {'account_id':account_id,'lastmonth':lastmonth}).first()#求cdn流量统计值
            if amount.amount:
                consume_3_day=consume_3_day+(datetime.datetime.utcnow().day+3)/month_days*amount.amount
            if account["type"]=="normal":#普通用户
                if consume_3_day>account["available_balance"]:
                    return True
            else:#信用用户
                if consume_3_day>account["total_balance"]:
                    return True
            return False
        except Exception as e:
            return False
                
    def _make_frozen(self,account_id,session):
        '''解冻账户'''
        account=session.query(Account).filter(Account.account_id==account_id).first()
        if account.status=='frozen' and float(account.cash_balance)+float(account.gift_balance)+float(account.credit_line)>0:
            account.status='normal'
            account.frozen_status='normal'
            from billing.emailsms.customer_communication import info_center
            infocenter=info_center()
            infocenter.unfreezen(account_id)
            
    def addcontact(self,account_id,para_dict, session=None):
        if session is None:
            session=sa.get_session()
        sql=SQL.AddContact
        try:
            session.execute(sql, dict({'name': para_dict['name'],
                                      'position': para_dict['position'],
                                      'telephone': para_dict['telephone'],
                                      'email': para_dict['email'],
                                      'remark': para_dict['remark'],
                                      'created_by': para_dict['created_by'],
                                      'created_at': para_dict['created_at'],
                                      'account_id': account_id}))
            session.close()
            return json.dumps({'success': 'success'})
        except Exception as e:
            session.close()
            LOG.error(str(e))
#            LOG.error(traceback.format_exc())
            return outError("添加联系人失败！")

    def getallsubaccount(self,session=None):
        if session is None:
            session = sa.get_session()
        sql = SQL.get_subaccount
        rows = session.execute(sql).fetchall()
        return rows

    def getAllProjectAdminAccount(self,session=None):
        if session is None:
            session = sa.get_session()
        sql = '''select temp.* from (select account.*,user.parent_id from account join keystone.user on account.user_id = user.id\
              and user.parent_id is not null)as temp join keystone.user on temp.parent_id = user.id and user.name in ('register','admin') '''
        rows = session.execute(sql).fetchall()
        return rows


        
#    def getAccountByUserMD5(self, user_md5, session=None):
#        '''根据user的md5查找账号'''
#        try:
#            if not session:
#                session = sa.get_session()
#            self.account = session.query(Account).filter(Account.user_md5 == user_md5).first()
#        except Exception as e:
#            session.close()
#            LOG.error(str(e))
#            raise e
    
if __name__ == '__main__':
    condition = {}
    accountDao = AccountDao()
    print accountDao.subAccountList('d5f8eaeb780645c6883a4d0b0728298e')
#    account=Account()
#    account.account_id="asdasjdjajsdjsajdj"
#    account.username="jajdsjasd"
#    account.gift_balance=100.04
#    account.cash_balance=200.35
#    account.type="credt"
#    account.status="normal"
#    accountDao=AccountDao(account)
#    accountDao.add()
#    print account.created_at

#    account=Account()
#    print dir(Account)
#    billDao=AccountDao()
#    result = billDao.getQuery()

# #    print result.page_dict()
#    bills = result
#    for k in bills:
#        print k.billes
