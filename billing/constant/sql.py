# -*- coding:utf-8 -*-
'''
Created on 2015年10月14日

@author: greshem
'''
class SQL(object):
    subAccountSum="SELECT * FROM (SELECT COUNT(*) AS credit_sum FROM keystone.user JOIN billing.account ON user.id = account.user_id WHERE account.status !='deleted' AND user.parent_id=:parent_id \
                AND account.type='credit') credit,\
                (SELECT COUNT(*) AS `sum` FROM keystone.user JOIN billing.account ON user.id = account.user_id WHERE account.status !='deleted' AND user.parent_id=:parent_id) acc"

    admin_subAccountSum="SELECT * FROM (SELECT COUNT(*) AS credit_sum FROM keystone.user JOIN billing.account ON user.id = account.user_id WHERE account.status !='deleted' \
                AND account.type='credit') credit,\
                (SELECT COUNT(*) AS `sum` FROM keystone.user JOIN billing.account ON user.id = account.user_id WHERE account.status !='deleted') acc"

    subAccountList="SELECT account.account_id,account.user_id,account.project_id,user.name,user.email,user.telephone,user.extra,user.company,account.cash_balance,account.gift_balance,account.type,account.credit_line FROM keystone.user JOIN billing.account ON user.id = account.user_id \
                    WHERE account.status !='deleted' AND user.parent_id=:parent_id"

    subAccountList_business='''SELECT temp1.*, real_name sales_name FROM(SELECT account.account_id,account.user_id, account.status, account.created_at, account.salesman_id, user.name,user.email,user.telephone,user.extra,user.company, user.parent_id,account.cash_balance,account.gift_balance,account.type,account.credit_line FROM keystone.user JOIN billing.account ON user.id = account.user_id) as temp1 left join user on temp1.salesman_id=user.id
                    WHERE temp1.status !='deleted' AND temp1.parent_id=:parent_id'''

    admin_subAccountList="SELECT account.account_id,account.user_id,account.project_id,user.name,user.email,user.telephone,user.extra,user.company,account.cash_balance,account.gift_balance,account.type,account.credit_line FROM keystone.user JOIN billing.account ON user.id = account.user_id \
                    WHERE account.status !='deleted'"

    subAccountListCount="SELECT count(*) as total_sum FROM keystone.user JOIN billing.account ON user.id = account.user_id \
                    WHERE account.status !='deleted' AND user.parent_id=:parent_id"

    admin_subAccountListCount="SELECT count(*) as total_sum FROM keystone.user JOIN billing.account ON user.id = account.user_id \
                    WHERE account.status !='deleted'"

    subAccountDetail="SELECT account.account_id,account.user_id,user.name,user.email,user.telephone,user.extra,account.cash_balance,account.gift_balance,account.type,account.credit_line FROM keystone.user JOIN billing.account ON user.id = account.user_id \
                    WHERE account.status !='deleted' AND account.account_id=:account_id"

    subAccountAmountSum="SELECT SUM(amount) AS amount_total,SUM(standard_amount) AS standard_amount_total FROM billing.consumption WHERE account_id IN(\
                    SELECT account_id FROM keystone.user LEFT JOIN billing.account ON user.id=account.user_id WHERE user.parent_id=:parent_id) \
                    and started_at>=:started_at and ended_at<=:ended_at"

    subAccountCurrentMonthAmountSum="SELECT SUM(current_month_amount) AS amount_total,SUM(current_month_standard_amount) AS standard_amount_total FROM keystone.user LEFT JOIN billing.account ON user.id=account.user_id WHERE user.parent_id=:parent_id"

    admin_subAccountAmountSum="SELECT SUM(amount) AS amount_total,SUM(standard_amount) AS standard_amount_total FROM billing.consumption WHERE account_id IN(\
                    SELECT account_id FROM keystone.user LEFT JOIN billing.account ON user.id=account.user_id WHERE started_at>=:started_at and ended_at<=:ended_at)"

    admin_subAccountCurrentMonthAmountSum="SELECT SUM(current_month_amount) AS amount_total,SUM(current_month_standard_amount) AS standard_amount_total FROM billing.account WHERE STATUS !='deleted'"

    bill="SELECT total.*,gift.gift_total FROM \
        (SELECT account_id,SUM(amount) AS amount_total,resource_id,resource_name,parent_id,region_id,resource_type,SUM(standard_amount) AS standard_total,\
        MAX(discounted_at) AS ended_at,MIN(discounted_at) AS started_at \
        FROM billing.consumption WHERE resource_type!='tunnel' and account_id=:account_id AND  started_at>=:started_at AND ended_at<=:ended_at GROUP BY resource_id) total LEFT JOIN \
        (SELECT account_id,SUM(amount) AS gift_total,resource_id \
        FROM billing.consumption WHERE  resource_type!='tunnel' and discount_by='gift_balance' AND account_id=:account_id AND started_at>=:started_at AND ended_at<=:ended_at GROUP BY resource_id) gift \
        ON total.resource_id= gift.resource_id"

    bill_naas="SELECT total.*,gift.gift_total FROM \
        (SELECT account_id,SUM(amount) AS amount_total,resource_id,resource_name,parent_id,region_id,resource_type,SUM(standard_amount) AS standard_total,\
        MAX(discounted_at) AS ended_at,MIN(discounted_at) AS started_at \
        FROM billing.consumption WHERE resource_type='tunnel' and account_id=:account_id AND  started_at>=:started_at AND ended_at<=:ended_at GROUP BY resource_id) total LEFT JOIN \
        (SELECT account_id,SUM(amount) AS gift_total,resource_id \
        FROM billing.consumption WHERE resource_type='tunnel' and discount_by='gift_balance' AND account_id=:account_id AND started_at>=:started_at AND ended_at<=:ended_at GROUP BY resource_id) gift \
        ON total.resource_id= gift.resource_id"

    regionList="SELECT * FROM keystone.region"
    #    checkProjectAdmin="SELECT * FROM (SELECT * FROM keystone.assignment WHERE `type`='UserProject' AND actor_id=:user_id) assgin \
    #                        LEFT JOIN keystone.role ON assgin.role_id=role.id WHERE `name`='project_admin' or `name`='admin'"
    checkProjectAdmin="SELECT kuser.*,role.name AS role_name FROM (SELECT * FROM keystone.user WHERE id=:user_id) kuser LEFT JOIN keystone.role \
                      ON kuser.default_role_id=role.id WHERE role.name='project_admin' OR role.name='admin'"

    checkAdmin="SELECT kuser.*,role.name AS role_name FROM (SELECT * FROM keystone.user WHERE id=:user_id)kuser LEFT JOIN keystone.role ON kuser.default_role_id=role.id where role.name='admin'"

    getRechargeSummary="select * from (SELECT SUM(amount) as bill_amount FROM billing.order WHERE payment_type='recharge' and status='pay_success' and account_id=:account_id) a,\
    (SELECT SUM(amount) as invoice_amount FROM billing.invoice WHERE account_id=:account_id) b"
    # end edit
    #    insteadRechargeList='''select temp3.*,username from (select temp2.*, order.account_id from (select temp.*,order_no,amount,pay_at,is_instead_recharge,status \
    #    from (select recharge_id,remark from instead_recharge where instead_recharge_account='%s')as temp left join recharge on temp.recharge_id=recharge.recharge_id \
    #     where is_instead_recharge=1 and status='pay_success')as temp2 left join billing.order on temp2.order_no=order.order_no)as temp3 left join account on temp3.account_id=account.account_id having 1=1'''
    insteadRechargeList='''select temp3.*,username from (select temp2.*, order.account_id from (select temp.*,order_no,amount,pay_at,is_instead_recharge,status \
    from (select recharge_id,remark from instead_recharge where instead_recharge_account='%s')as temp left join recharge on temp.recharge_id=recharge.recharge_id \
    where is_instead_recharge=1 and status='pay_success')as temp2 left join billing.order on temp2.order_no=order.order_no)as temp3 left join account on temp3.account_id=account.account_id having 1=1'''

    insteadTotalAmount='''select sum(amount) as total from (select recharge_id from instead_recharge where instead_recharge_account=:instead_recharge_account)as temp left join \
    recharge on temp.recharge_id=recharge.recharge_id where is_instead_recharge=1 and status=\'pay_success\''''

    # arsene
    CustomerCount='''select * from (select account_id, status, project_id, user.default_role_id, user.parent_id from billing.account left join keystone.user on account.project_id=user.default_project_id) as temp1 left join keystone.role on temp1.default_role_id=role.id having 1=1'''

    UpdateBasicInfo_account='''update account set customer_level=:customer_level, company_property=:company_property where account_id=:account_id'''
    BecomeCredit='''update account set type='credit', credit_line=:credit_line where account_id=:account_id'''
    GetContactList='''select contact_id, contact.name contactname, contact.position, contact.telephone, contact.email, contact.created_at, remark, user.username creator from contact left join user on created_by=user.id where account_id=:account_id'''
    AddContact = '''insert into contact (name, position, telephone, email, remark, created_by, created_at, account_id) VALUES \
                    (:name, :position, :telephone, :email, :remark, :created_by, :created_at, :account_id)'''
    UpdateContact = '''update contact set name=:name, position=:position, telephone=:telephone, \
                    email=:email, remark=:remark, updated_at=:updated_at where contact_id=:contact_id'''
    DeleteContact = '''delete from contact where contact_id=:contact_id'''
    GetAllSales = '''select * from (select user_role_relation.user_id sales_user_id, status, role_id, real_name sales_name from billing.user left join user_role_relation on user.id= user_role_relation.user_id) as t1 left join role on t1.role_id=role.id having status=\'normal\' and codename in (\'salesman\', \'sales_manager\')'''
    GetNaasDiscount = '''SELECT * from discount LEFT JOIN billing_item on discount.billing_item_id = billing_item.billing_item_id where account_id=:account_id and region_id=\'naas\''''




    # zhangaw
    # 获取客户列表
    CustomerList='''select temp5.*, real_name as full_name from (select temp4.*,user.name as parent_name from (select temp3.*,role.name as parent_role \
    from(select temp2.*,role.name from (select temp.*,user.default_role_id as parent_role_id \
    from (select account.*,user.telephone usertelephone,user.email useremail, user.company company, user.default_role_id, user.parent_id,user.id as userId from account left join keystone.user on account.project_id=user.default_project_id)as temp \
    left join keystone.user on temp.parent_id=user.id) as temp2 left join keystone.role on temp2.default_role_id=role.id) as temp3 \
    left join keystone.role on temp3.parent_role_id=role.id)as temp4 left join keystone.user on temp4.parent_id=user.id) as temp5 left join user on temp5.salesman_id=user.id having 1=1 '''
    # 区域列表获取
    RegionList='select region_id from (select * from account where user_id=:user_id)as temp left join keystone.user_region on temp.user_id=user_region.user_id'
    DiscountListPerRegion='select region_id,billing_item,discount_ratio from (select * from discount where account_id=:account_id) as temp left join \
    (select * from billing_item where region_id=:region_id)as temp2 on temp.billing_item_id=temp2.billing_item_id'
    # 更新折扣表
    DiscountUpdate='update discount set discount_ratio=:discount_ratio where account_id=:account_id and billing_item_id=:billing_item_id'
    DiscountInsert='insert into discount(billing_item_id,account_id,discount_ratio) values (:billing_item_id,:account_id,:discount_ratio)'
    # 票数目统计
    invoiceNumberSql='select * from (select count(*)as invoice_total from billing.invoice where account_id=:account_id)a, \
    (select count(*)as invoice_apply from billing.invoice where account_id=:account_id and status=\'apply\')b'
    # Finance:invoice_manage
    invoiceManageListSql='''select temp3.*,role.name as parent_name from (select temp2.*,role.name from (select temp1.*,user.default_role_id as parent_role_id \
      from (select account.account_id,account.username,account.type,account.project_id,user.id as user_id,user.default_role_id as role_id,parent_id as parent_user_id,user.extra \
     from account left join keystone.user on account.project_id=user.default_project_id)as temp1 left join keystone.user on temp1.parent_user_id=user.id)as temp2 \
      left join keystone.role on temp2.role_id=role.id)as temp3 left join keystone.role on temp3.parent_role_id=role.id having 1=1'''
    invoiceListSqlbyAccount='''select temp4.*,role.name as parent_name from (select temp3.*,role.name from (select temp2.*,user.default_role_id as parent_role_id from \
    (select temp.*,user.parent_id,default_role_id as role_id,user.extra from (select account_id,project_id,username from account where account_id=:account_id)as temp left join \
     keystone.user on temp.project_id=user.default_project_id)as temp2 left join keystone.user on temp2.parent_id = user.id)as temp3 left join keystone.role on temp3.role_id=role.id)as temp4 \
    left join keystone.role on temp4.parent_role_id=role.id'''
    # 获取billing_item_id
    getBillingItemIdSql="select billing_item_id from billing_item where region_id=:region_id and billing_item=:billing_item"
    # *********finance by zhangaw***********

    invoiceListSqlByAccount='''select * from invoice where account_id=:account_id'''

    invoiceListSql='''select * from invoice where 1=1'''

    accountInfoSqlByAccount='''select temp4.*,user.name as parent_name from (select temp3.*,role.name as parent_role \
    from(select temp2.*,role.name as role from (select temp.*,user.default_role_id as parent_role_id \
    from (select te.*,user.telephone,user.company,user.email,user.default_role_id, user.parent_id,user.extra,user.id as userId from (select * from account where account_id=:account_id)as te left join keystone.user on te.project_id=user.default_project_id)as temp \
    left join keystone.user on temp.parent_id=user.id) as temp2 left join keystone.role on temp2.default_role_id=role.id) as temp3 \
    left join keystone.role on temp3.parent_role_id=role.id)as temp4 left join keystone.user on temp4.parent_id=user.id having 1=1'''

    accountInfoSql_2='''select temp4.*,user.name as parent_name from (select temp3.*,role.name as parent_role \
    from(select temp2.*,role.name as role from (select temp.*,user.default_role_id as parent_role_id \
    from (select te.*,user.telephone,user.company,user.email,user.default_role_id, user.parent_id,user.extra,user.id as userId from (select * from account)as te left join keystone.user on te.project_id=user.default_project_id)as temp \
    left join keystone.user on temp.parent_id=user.id) as temp2 left join keystone.role on temp2.default_role_id=role.id) as temp3 \
    left join keystone.role on temp3.parent_role_id=role.id)as temp4 left join keystone.user on temp4.parent_id=user.id having 1=1'''

    accountInfoSql='''select temp4.*,user.name as parent_name from (select temp3.*,role.name as parent_role \
    from(select temp2.*,role.name as role from (select temp.*,user.default_role_id as parent_role_id \
    from (select account.*,user.telephone,user.company,user.email,user.default_role_id, user.parent_id,user.extra,user.id as userId from account left join keystone.user on account.project_id=user.default_project_id)as temp \
    left join keystone.user on temp.parent_id=user.id) as temp2 left join keystone.role on temp2.default_role_id=role.id) as temp3 \
    left join keystone.role on temp3.parent_role_id=role.id)as temp4 left join keystone.user on temp4.parent_id=user.id having 1=1 '''

    rechargeListSql='''select temp.*,instead_recharge.recharge_id as instead_recharge_id,instead_recharge.instead_recharge_by as operate_by from \
    (select order.payment_type,order.order_no,order.amount,order.account_id,recharge.pay_at,recharge.recharge_id,recharge.payment_way from \
     `order` join recharge on `order`.order_no=recharge.order_no where order.status='pay_success')as temp left join instead_recharge on temp.recharge_id=instead_recharge.recharge_id having 1=1'''

    giftRechargeListSql='''select order.payment_type,order.order_no,order.amount,order.account_id,gift.gift_at as pay_at,order.status,gift.gift_id as payment_way,gift.status,gift.gift_by as operate_by from `order` join gift on `order`.order_no=gift.order_no where order.status='pay_success' \
    and order.payment_type='gift' having 1=1'''

    rechargeAmountSql='''select sum(order.amount)as recharge_amount from `order` join recharge on `order`.order_no=recharge.order_no where order.status=\'pay_success\''''
    giftAmountSql='''select sum(order.amount)as gift_amount from `order` join  gift on `order`.order_no=gift.order_no where order.status=\'pay_success\' and order.payment_type=\'gift\''''

    getCompanyInfoByAccount='''select user.*,temp.* from (select * from account where account_id=:account_id)as temp left join keystone.user on temp.project_id=user.default_project_id '''
    invoiceHandleSql='''update invoice set invoice_no=:invoice_no,post_by=:post_by,express_no=:express_no,process_by=:process_by,status=:status,process_at=:process_at where invoice_id=:invoice_id'''


    # end edit
    # yamin
    #查询用户信息
    get_user_info="SELECT " \
                  "t1.id as user_id," \
                  "t1.name as username," \
                  "t1.extra as company_info_json," \
                  "t1.enabled as user_status," \
                  "t1.domain_id," \
                  "t1.company," \
                  "t1.default_project_id as project_id," \
                  "t1.telephone," \
                  "t1.email," \
                  "t2.id as role_id," \
                  "t2.name as role_name," \
                  "t2.extra as role_info_json, " \
                  "t1.parent_id as parent_id, " \
                  "t3.default_role_id as parent_role_id," \
                  "t4.name as parent_role_name " \
                  "from keystone.user as t1 " \
                  "left join keystone.role as t2 on  t1.default_role_id=t2.id " \
                  "left join keystone.user as t3 on  t1.parent_id=t3.id " \
                  "left join keystone.role as t4 on  t3.default_role_id=t4.id " \
                  "where t1.default_project_id=:project_id"

    #查询区域信息
    get_region_info="SELECT " \
                    "t1.user_id," \
                    "t1.region_id," \
                    "t2.description," \
                    "t2.parent_region_id," \
                    "t2.extra as region_info_json " \
                    "FROM keystone.user_region as t1 join keystone.region as t2 on t1.region_id=t2.id " \
                    "where t1.user_id=:user_id"

    #使用user_id查询
    get_user_info1="SELECT " \
                   "t1.id as user_id, " \
                   "t1.name as username," \
                   "t1.extra as company_info_json," \
                   "t1.enabled as user_status," \
                   "t1.domain_id," \
                   "t1.default_project_id as project_id," \
                   "t1.telephone," \
                   "t1.email " \
                   "from keystone.user as t1 " \
                   "where t1.id=:user_id"
    #查询计费项目
    sql_other_consume="SELECT SUM(amount) as amount FROM billing.consumption WHERE  account_id=:account_id AND started_at=:lasthour AND resource_type NOT IN('cdnflow','cdnbandwidth')"
    sql_cdn_consume="SELECT SUM(amount) as amount FROM billing.consumption WHERE  account_id=:account_id AND started_at>:lastday AND resource_type in ('cdnbandwidth','cdnflow')"

    #boss系统用户信息
    sql_boss_user_all='''SELECT a1.id as user_id,a1.password,a1.last_login,a1.is_superuser,\
a1.username,a1.first_name,a1.last_name,a1.email,a1.is_staff,a1.is_active,a1.date_joined,\
a1.real_name,a1.position,a1.gender,a1.phone,a1.mobile,a1.status,a1.leader_id,a1.dept_id,\
a1.updated_at,a1.deleted_at,a3.id as role_id,a3.name as role_name,a3.codename as role_code \
FROM billing.user as a1 join billing.user_role_relation as a2  on a1.id=a2.user_id  \
join billing.role as a3 on a2.role_id=a3.id'''

    sql_boss_user_code='''SELECT a1.id as user_id,a1.password,a1.last_login,a1.is_superuser,\
a1.username,a1.first_name,a1.last_name,a1.email,a1.is_staff,a1.is_active,a1.date_joined,\
a1.real_name,a1.position,a1.gender,a1.phone,a1.mobile,a1.status,a1.leader_id,a1.dept_id,\
a1.updated_at,a1.deleted_at,a3.id as role_id,a3.name as role_name,a3.codename as role_code \
FROM billing.user as a1 join billing.user_role_relation as a2  on a1.id=a2.user_id  \
join billing.role as a3 on a2.role_id=a3.id where a3.codename=:codename'''
  # 返现账单相关sql

    #获取每个分销商子账户指定时间段内返现总额及消费总额
    get_rebate_subbill_item = '''select temp3.account_id,temp3.parent_account,sum(rebate_amount) as rebate_amount_total,sum(amount) as amount_total from \
    (select temp2.* from (select temp.*,account.user_id as parent_user_id from (select consumption.*,account.parent_account from consumption join account \
    on consumption.account_id = account.account_id and account.parent_account is not null and started_at >=:started_at and ended_at <=:ended_at and consumption.account_id =:account_id )as temp\
    join account on temp.parent_account = account.account_id)as temp2 join keystone.user on temp2.parent_user_id = user.id and user.name not in('register','admin')) as temp3 group by account_id,parent_account '''

    #获取某个分销商子账号在指定时间段内的消费赠送金额总额
    get_rebate_subbill_giftamount = '''select sum(amount) as gift_amount_total from (select temp2.* from (select temp.*,account.user_id as parent_user_id\
    from (select consumption.*,account.parent_account from consumption join account on consumption.account_id = account.account_id and account.parent_account is not null \
    and started_at >=:started_at and ended_at <=:ended_at and discount_by = 'gift_balance' and consumption.account_id=:account_id)as temp join account on temp.parent_account = account.account_id)as temp2\
    join keystone.user on temp2.parent_user_id = user.id and user.name not in('register','admin')) as temp3'''

    #从account表中获取所有的分销商子账号的account_id
    get_subaccount = ''' select temp2.account_id from (select temp.*,user.parent_id from (select * from account ) as temp join keystone.user on\
    temp.user_id = user.id and user.parent_id is not null) as temp2 join keystone.user on temp2.parent_id = user.id and user.name not in ('register','admin')'''

    #获取指定分销商子账号在指定时间段内每种资源类型的消费总额
    get_one_rebatebill_item = '''select resource_id,region_id,resource_type,resource_name,sum(amount) as amount_total,sum(rebate_amount) as rebate_amount_total from consumption where started_at >=:started_at and ended_at <=:ended_at\
    and account_id=:account_id group by resource_id '''

    #获取指定分销商账号在指定时间段内指定资源的赠送消费总额
    get_one_rebatebill_item_gift_amount = ''' select sum(amount) as gift_amount_total from consumption where started_at >=:started_at and ended_at <=:ended_at and resource_id=:resource_id and\
    discount_by = 'gift_balance' group by resource_id'''
