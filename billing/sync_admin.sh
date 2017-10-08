set -x 
#6944c1de6f96421b8d182d05702a37e7

source /root/keystonerc_admin 

#openstack user list  |grep admin 

new_admin=$(openstack user list  |grep  '| admin'    |awk '{print $2}' )
echo  create database  billing  > create_db.sql 

mysql  < create_db.sql 

sed "s/6944c1de6f96421b8d182d05702a37e7/$new_admin/"   billing_data.sql >   tmp.sql

mysql  billing < tmp.sql

mysql <   mysql_pass.sql
systemctl restart mariadb 
