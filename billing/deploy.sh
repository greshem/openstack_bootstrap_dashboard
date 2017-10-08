set -x 
cp -a -r  ../billing/   /usr/lib/python2.7/site-packages/
cp -a -r  SMSSDK/       /usr/lib/python2.7/site-packages/

nohup python billing-api  billing_conf/billing.conf  & 
echo sleep 4
sleep 4
new_admin=$(openstack user list  |grep  '| admin'    |awk '{print $2}' )
curl  http://127.0.0.1:8081/v1.0//account/getaccountbyuserid/$new_admin


