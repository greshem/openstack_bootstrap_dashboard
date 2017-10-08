# -*- coding:utf-8 -*-
from billing.db.sqlalchemy import session as sa
from billing.constant.sql import SQL
from oslo_log import log as logging
from billing.util.handlerUtil import *
import json
import traceback
from billing.constant.constant import constVar
import datetime

LOG=logging.getLogger(__name__)
# 获取客户列表
def getcustomerList(condition=None,**args) :
    '''客户列表获取'''
    try:
        session=sa.get_session()
        sql=SQL.CustomerList
        if condition:
            for key,value in condition.items():
                if key=='username':
                    sql+=' and username like'+' \'%'+'%s'%value +'%\''  #用户名
                if key=='company':
                    sql+=' and company like'+' \'%'+'%s'%value +'%\'' #公司名
                if key=='telephone':
                    sql+=' and usertelephone like'+' \'%'+'%s'%value +'%\'' #注册手机号
                if key=='email':
                    sql+=' and useremail like'+' \'%'+'%s'%value +'%\'' #注册邮箱
                if key=='sales':
                    sql+=' and full_name like'+' \'%'+'%s'%value +'%\'' #业务员
                if key=='type':
                    sql+=' and type=\'%s\''%value #用户类型
                if key=='role':
                    if value in('user','_member_'):
                        sql+=' and name in (\'_member_\',\'user\') and parent_role=\'admin\''
#                        sql+=' and name=\'user\' and parent_role=\'admin\''

                    if value=='project_admin':
                        sql+=' and name=\'project_admin\''#and parent_role=\'admin\''
                    if value=='project_sub':
                        sql+=' and name in(\'user\',\'_member_\') and parent_role=\'project_admin\''
                if key=='status':
                    sql+=' and status=\'%s\''%value
                if key=='time_from':
                    sql+=' and created_at>\'%s\''%value
                if key=='time_to':
                    sql+=' and created_at<\'%s\''%value
                if key=='salesman_id':
                    sql+=' and salesman_id=%s' %value
                if key=='parent_id':
                    sql+=' and parent_id=\'%s\'' %value
                if key=='cash_balance':
                    if value=='0':
                        sql+=' and cash_balance<0'
                    elif value in ['0-500', '500-1000']:
                        m=value.split('-')
                        sql+=' and cash_balance between %s and %s' % (m[0], m[1])
                    else:
                        sql+=' and cash_balance>1000'

        sql+=' order by created_at desc'
        user=session.execute(sql).fetchall()
        count=len(user)
        if condition:
            if condition.has_key('limit') and condition.has_key('offset'):
                limit=int(condition['limit'])
                offset=int(condition['offset'])
                user=user[(limit*offset):((offset+1)*limit)]
        result=[]
        normalcount=0
        frozencount=0
        for item in user:
            tempdict={}
            tempdict['account_id']=item.account_id
            tempdict['username']=item.username
            tempdict['telephone']=item.usertelephone
            tempdict['email']=item.useremail
            tempdict['company']=item.company
            tempdict['type']=item.type
            tempdict['status']=item.status
            tempdict['cash_balance']=float(item.cash_balance) if item.cash_balance else 0
            tempdict['gift_balance']=float(item.gift_balance) if item.gift_balance else 0
            tempdict['balance']=tempdict['cash_balance']+tempdict['gift_balance']
            tempdict['credit_line']=float(item.credit_line) if item.credit_line else 0
            tempdict['created_at']=item.created_at.strftime("%Y-%m-%d %H:%M:%S") if item.created_at else None
            tempdict['sales']=item.full_name
            # tempdict['updated_at']=item.updated_at.strftime("%Y-%m-%d %H:%M:%S") if item.updated_at else None
            tempdict['project_id']=item.project_id
            tempdict['default_role_id']=item.default_role_id
            tempdict['parent_id']=item.parent_id
            tempdict['parent_name']=item.parent_name
            tempdict['user_id']=item.userId
            tempdict['name']=item.name
            if item.name in('user','_member_'):
                if item.parent_name in('admin','register'):
                    tempdict['role']='common_user'
                else:
                    tempdict['role']='project_subaccount'
            elif item.name=='project_admin':
                tempdict['role']='project_admin'
            elif item.name=='admin':
                tempdict['role']='admin'
            else:
                tempdict['role']=None
            if item.status=='normal':
                normalcount+=1
            if item.status=='frozen':
                frozencount+=1
            result.append(tempdict)
        return json.dumps({'count':count,'normalcount':normalcount,'frozencount':frozencount,'customerList':result, "success":"success"},cls=CJsonEncoder, ensure_ascii=False)
    except Exception as e:
        session.close()
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("获取客户列表失败!")

# arsene
def getcustomercount(parent_id=None):
    sql=SQL.CustomerCount

    if parent_id:
        sql+= " and parent_id ='%s'"%parent_id
    try:
        session=sa.get_session()
        user=session.execute(sql).fetchall()
        total=len(user)
        count_frozen=0
        count_normal=0
        count_deleted=0
        for i in user:
            if i.status=='frozen':
                count_frozen+=1
            if i.status=='normal':
                count_normal+=1
            if i.status=='deleted':
                count_deleted+=1
        return json.dumps({'success': 'success', 'total': total, 'frozen':count_frozen, 'normal': count_normal, 'deleted': count_deleted})
    except Exception as e:
        session.close()
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("获取客户数量汇总失败!")


def updatebasicinfo(account_id, para_dict):
    sql1=SQL.UpdateBasicInfo_account
    try:
        session=sa.get_session()
        session.execute(sql1, dict({'customer_level': para_dict['customer_level'], 'company_property': para_dict['company_property'], 'account_id': account_id}))
        if 'salesman_id' in para_dict and 'type' in para_dict:
            session.execute('update account set salesman_id=:salesman_id, type=:type where account_id=:account_id',
                            dict({'salesman_id': int(para_dict['salesman_id']), 'type': para_dict['type'], 'account_id':account_id}))
        elif 'type' in para_dict:
            session.execute('update account set type=:type where account_id=:account_id', dict({'type': para_dict['type'], 'account_id':account_id}))
        elif 'salesman_id' in para_dict:
            session.execute('update account set salesman_id=:salesman_id where account_id=:account_id',
                            dict({'salesman_id': int(para_dict['salesman_id']), 'account_id':account_id}))
        return json.dumps({'success':'success'})
    except Exception as e:
        session.close()
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("更新信息失败!")


def becomecredit(para_dict):
    sql=SQL.BecomeCredit
    try:
        session=sa.get_session()
        account_id=para_dict['account_id']
        credit_line=para_dict['credit_line']
        session.execute(sql, dict({'account_id':account_id, 'credit_line':credit_line}))
        return json.dumps({'success':'success'})
    except Exception as e:
        return outError('升级信用用户失败！')


def getnaasdiscount(account_id, session=None):
    sql=SQL.GetNaasDiscount
    try:
        session=sa.get_session()
        result = session.execute(sql, dict({'account_id': account_id})).first()
        if result:
            return outSuccess('discount',float(result.discount_ratio))
        else:
            return outSuccess('discount',1)
    except Exception as e:
        return outError('获取naas折扣失败')


def setnaasdiscount(account_id, para_dict, session=None):
    session=sa.get_session()
    discount= para_dict['discount']
    try:
        session.execute('delete from discount where account_id =:account_id and billing_item_id in '
                        '(select billing_item_id from billing_item where region_id=\'naas\')',
                        dict({'account_id': account_id}))
        session.execute('insert into discount (billing_item_id, account_id, discount_ratio) '
                        'select billing_item_id, :account_id as account_id, :discount as discount_ratio '
                        'from billing_item where region_id=\'naas\'', dict({'account_id': account_id, 'discount':discount}))
        return json.dumps({'success':'success'})
    except Exception as e:
        return outError('更新naas折扣失败')


def becomeprojectadmin(para_dict, session=None):
    if session is None:
        session=sa.get_session()
    try:
        role_id=session.execute('select id from keystone.role where name=\'project_admin\'').first().id
        account_id=para_dict['account_id']
        project_id=session.execute("select project_id from account where account_id=:account_id", dict({'account_id': account_id})).first().project_id
        session.execute("update keystone.user set default_role_id=:role_id where default_project_id=:project_id", dict({'project_id': project_id, 'role_id': role_id}))
        session.close()
        return json.dumps({'success':'success'})
    except Exception as e:
        session.close()
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("升级分销商失败!")


def assignsales(para_dict):
    try:
        account_id=para_dict['account_id']
        salesman_id=para_dict['salesman_id']
    except Exception as e:
        return outError('获取account_id, salesman_id失败！')
    try:
        session=sa.get_session()
        session.execute("update account set salesman_id=:salesman_id where account_id=:account_id", dict({'account_id': account_id, 'salesman_id': salesman_id}))
        session.close()
        return json.dumps({'success': 'success'})
    except Exception as e:
        session.close()
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("指派业务员失败！")


def getcontactlist(account_id, session=None):
    if session is None:
        session=sa.get_session()
    sql=SQL.GetContactList
    try:
        contactlist=session.execute(sql, dict({'account_id':account_id})).fetchall()
        result=[]
        for eachcontact in contactlist:
            temp={}
            temp['contact_id']=eachcontact.contact_id
            temp['contact_name']=eachcontact.contactname
            temp['contact_position']=eachcontact.position
            temp['contact_telephone']=eachcontact.telephone
            temp['contact_email']=eachcontact.email
            temp['created_by']=eachcontact.creator
            temp['created_at']=eachcontact.created_at
            temp['remark']=eachcontact.remark
            result.append(temp)
        session.close()
        return outSuccess('subAccountList', result)
    except Exception as e:
        session.close()
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("获取联系人列表失败！")


def addcontact(account_id,para_dict, session=None):
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
        LOG.error(traceback.format_exc())
        return outError("添加联系人失败！")


def updatecontact(contact_id, para_dict, session=None):
    if session is None:
        session=sa.get_session()
    sql=SQL.UpdateContact
    try:
        session.execute(sql, dict({'name': para_dict['name'],
                                   'position': para_dict['position'],
                                   'telephone': para_dict['telephone'],
                                   'email': para_dict['email'],
                                   'remark': para_dict['remark'],
                                   'updated_at': para_dict['updated_at'],
                                   'contact_id': int(contact_id)}))
        session.close()
        return json.dumps({'success':'success'})
    except Exception as e:
        session.close()
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("更新联系人失败！")


def deletecontact(contact_id, session=None):
    if session is None:
        session=sa.get_session()
    sql=SQL.DeleteContact
    try:
        session.execute(sql, dict({'contact_id': contact_id}))
        session.close()
        return json.dumps({'success': 'success'})
    except Exception as e:
        session.close()
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("删除联系人失败！")


def editdiscount(account_id, para_dict, session=None):
    if session is None:
        session=sa.get_session()
    try:
        discountEdit(account_id,para_dict,session)
        session.close()
        return json.dumps({'success':'success'})
    except Exception as e:
        session.close()
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("修改折扣失败！")


def getminorinfo(account_id, session=None):
    if session is None:
        session=sa.get_session()
    try:
        rows=session.execute('''select company_property, customer_level, salesman_id from account where account_id=:account_id''',
                             dict({'account_id': account_id})).first()

        result={'company_property': rows.company_property,
                'customer_level': rows.customer_level,
                'salesman_id': rows.salesman_id}
        return outSuccess('minorinfo', result)
    except Exception as e:
        session.close()
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("获取信息失败")


def getallsales(session=None):
    if session is None:
        session=sa.get_session()
    sql=SQL.GetAllSales
    try:
        rows=session.execute(sql).fetchall()
        saleslist=[]
        for i in rows:
            tem={}
            tem['sales_user_id']=i.sales_user_id
            tem['sales_name']=i.sales_name
            saleslist.append(tem)
        return outSuccess('sales',saleslist)
    except Exception as e:
        session.close()
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("获取销售列表失败")

def getksuserinfo(account_id, session=None):
    if session is None:
        session=sa.get_session()
    try:
        rows=session.execute('select project_id, username, type, salesman_id, company_property, customer_level from account where account_id=\'%s\''%account_id).first()
        project_id=rows.project_id
        username = rows.username
        type = rows.type
        salesman_id = rows.salesman_id
        company_property = rows.company_property
        customer_level = rows.customer_level
        ksuserinfo = session.execute('select id, company, telephone,email from keystone.user where default_project_id=:project_id',
                                     dict({'project_id': project_id})).first()
        ks_user_id = ksuserinfo.id
        ks_company = ksuserinfo.company
        ks_telephone = ksuserinfo.telephone
        ks_email = ksuserinfo.email
        return json.dumps({'success': 'success', 'keystone_user_info':{
            'account_id': account_id,
            'username': username,
            'user_id': ks_user_id,
            'type': type,
            'company': ks_company,
            'company_property': company_property,
            'salesman_id': salesman_id,
            'customer_level': customer_level,
            'email': ks_email,
            'telephone': ks_telephone
        }})
    except Exception as e:
        session.close()
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("获取keystone客户信息失败！")

def getuserrole(para_dict,session=None):
    if session is None:
        session=sa.get_session()
    user_id=para_dict['user_id']
    result=session.execute("select role_id, name role_name, codename from billing.user_role_relation left join billing.role on"
                    " role.id=user_role_relation.role_id where user_id=\'%s\'"%user_id).first()
    try:
        return outSuccess('codename', result.codename)
    except Exception as e:
        session.close()
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("获取用户角色失败")

def getaccountidbyprojectid(para_dict, session=None):
    if session is None:
        session=sa.get_session()
    project_id = para_dict['project_id']
    result=session.execute('select account_id from billing.account where project_id = \'%s\''%project_id).first()
    try:
        return outSuccess('account_id', result.account_id)
    except Exception as e:
        session.close()
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("获取account_id失败")


def getcustomerdetails(account_id, session=None):
    if session is None:
        session=sa.get_session()
    try:
        customer_info ={}
        account_info = session.execute('select * from billing.account where account_id=:account_id', dict({'account_id': account_id})).first()
        k=account_info.username
        if account_info:
            customer_info['username'] = account_info.username
            customer_info['type']= account_info.type
            customer_info['company_property']= account_info.company_property
            customer_info['customer_level'] = account_info.customer_level
            user_id = account_info.user_id
            customer_info['user_id']=user_id
        else:
            return outError('account_id不存在！')
        keystone_info = session.execute('select * from keystone.user where id=:user_id', dict({'user_id': user_id})).first()
        customer_info['company']=keystone_info.company
        customer_info['project_id']=keystone_info.default_project_id
        customer_info['created_at']=keystone_info.created_at
        customer_info['industry']=json.loads(keystone_info.extra)['industry']
        customer_info['email']=keystone_info.email
        customer_info['telephone']=keystone_info.telephone
        '''区域信息'''
        rows=session.execute('select region_id from keystone.user_region where user_id=:user_id', dict({'user_id': user_id})).fetchall()
        m=[i.region_id for i in rows]
        customer_info['regions']=','.join(m)
        '''客户角色'''
        role_id = keystone_info.default_role_id
        role_a = session.execute('select name from keystone.role where id = :role_id', dict({'role_id': role_id})).first()
        if role_a.name in ['user', '_member_']:
            role_b = session.execute('select role.name from keystone.user left join keystone.role on user.default_role_id=role.id where user.id=:role_id', dict({'role_id': keystone_info.parent_id})).first()
            if role_b.name ==None or role_b.name in ['admin', 'register']:
                customer_info['role']='user'
            else:
                customer_info['role']='subaccount'
        elif role_a.name == 'project_admin':
            customer_info['role']='project_admin'
        elif role_a.name == 'admin':
            customer_info['role']='admin'
        else:
            customer_info['role']='unknown'
        return outSuccess('customer_info', customer_info)
    except Exception as e:
        return outError('获取客户详情失败！')


# 获取账户信息(折扣)
def getaccountInfo(account_id,**args):
    '''帐号信息获取'''
    try:
        session=sa.get_session()
        result={}
        discount_sql=SQL.DiscountListPerRegion
        project_id=session.execute('select project_id from account where account_id=\'%s\''%account_id).first().project_id
        userIdQuery=session.execute('select id from keystone.user where default_project_id=\'%s\''%project_id)
        if userIdQuery:
            user_id=userIdQuery.first().id
        else:
            user_id=0
        region_query=session.execute('select region_id from keystone.user_region where user_id=\'%s\''%user_id).fetchall()
        region_temp=[]
        for each in region_query:
            region_temp.append(each.region_id)
        region_temp.append("RegionCdn")
        for item in region_temp:
            if item!='RegionCdn':
                result[item]={}
                temp=session.execute(discount_sql,dict({'account_id':account_id,'region_id':item})).fetchall()
                for each in temp:
                    if each.discount_ratio and each.billing_item:
                        result[item][each.billing_item]=float(each.discount_ratio)
                temp2=session.execute(discount_sql,dict({'account_id':account_id,'region_id':'RegionCdn'})).fetchall()
                for each in temp2:
                    if each.discount_ratio and each.billing_item:
                        result[item][each.billing_item]=float(each.discount_ratio)
        return json.dumps(result)
    except Exception as e:
        session.close()
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("获取帐号信息失败!")

# 用户类型编辑
def userTypeEdit(account_id,type,credit_line,session=None):
    typeEditSql='update account set type=\'%s\',credit_line=%f where account_id=\'%s\''%(type,credit_line,account_id)
    if session is None:
        session=sa.get_session()
    session.begin()
    session.execute(typeEditSql)
    session.commit()

# 账户类型编辑
def accountTypeEdit(role,account_id,session=None):
    if session is None:
        session=sa.get_session()
    roleIdSql='select id from keystone.role where name=\'%s\''%role
    projectIdSql='select project_id from account where account_id=\'%s\''%account_id
    roleId=session.execute(roleIdSql).first().id
    projectId=session.execute(projectIdSql).first().project_id
    typeEditSql='update keystone.user set default_role_id=\'%s\' where default_project_id=\'%s\''%(roleId,projectId)
    session.begin()
    session.execute(typeEditSql)
    session.commit()

# 折扣编辑
def discountEdit(account_id,discountDict,session=None):
    itemIdListSql='select billing_item_id from discount where account_id=\'%s\''%account_id
    if session is None:
        session=sa.get_session()
    formatDiscount=getFormatDiscount(discountDict,session)
    itemIdList=[]
    temp=session.execute(itemIdListSql).fetchall()
    if temp:
        for each in temp:
            itemIdList.append(each.billing_item_id)
    for itemId in formatDiscount.keys():
        if itemId in itemIdList:
            session.begin()
            session.execute(SQL.DiscountUpdate,dict({'discount_ratio':formatDiscount[itemId],'account_id':account_id,'billing_item_id':itemId}))
            session.commit()
        else:
            session.execute(SQL.DiscountInsert,dict({'billing_item_id':itemId,'account_id':account_id,'discount_ratio':formatDiscount[itemId]}))
            session.flush()
def getFormatDiscount(discountDict,session=None):
    region_list=discountDict.keys()
    if session is None:
        session=sa.get_session()
    temp={}
    for item in region_list:
        for each in range(len(discountDict[item])):
            if each!=6 and each!=5:
                billing_item=constVar.discountEdit[each]
                billing_item_id=session.execute(SQL.getBillingItemIdSql,dict({'region_id':item,'billing_item':billing_item})).first().billing_item_id
                discount_ratio=float(discountDict[item][each])
                temp[billing_item_id]=discount_ratio
            else:
                billing_item=constVar.discountEdit[each]
                print billing_item
                billing_item_id=session.execute(SQL.getBillingItemIdSql,dict({'region_id':'RegionCdn','billing_item':billing_item})).first().billing_item_id
                discount_ratio=float(discountDict[item][each])
                temp[billing_item_id]=discount_ratio
    return temp

# 账户信息编辑
def accountinfoEdit(account_id,editcontent):
    try:
        session=sa.get_session()
        type=editcontent['type']
        credit_line=float(editcontent['credit_line'])
        role=editcontent['role']
        discountDict=editcontent['discount']
        userTypeEdit(account_id,type,credit_line,session)
        accountTypeEdit(role,account_id,session)
        discountEdit(account_id,discountDict,session)
        session.close()
        return json.dumps({'success':'success'})
    except Exception as e:
        session.close()
        LOG.error(str(e))
        LOG.error(traceback.format_exc())
        return outError("帐号信息修改失败!")











if __name__=='__main__':
    data={'RegionOne':[0.81,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89],
          'RegionTwo':[0.81,0.82,0.83,0.84,0.85,0.86,0.87,0.88,0.89]
        }

    tg=getFormatDiscount(data)
