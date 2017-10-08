function  change_to_127()
{
#sed -i  's/127.0.0.1/1.1.1.101/g' settings_dashboard.py 
# 'LOCATION': ['127.0.0.1:11211'],
# OPENSTACK_HOST='127.0.0.1'
sed -i  "/LOCATION/{s/.*/'LOCATION':\['127.0.0.1:11211'\],/}"   settings_dashboard.py 
sed -i  "/OPENSTACK_HOST/{s/.*/OPENSTACK_HOST='127.0.0.1' /g}"  settings_dashboard.py 
}



function  change_to_1_1_1()
{
sed -i  "/LOCATION/{s/.*/'LOCATION': \['1.1.1.101:11211'\],/}"   settings_dashboard.py 
sed -i  "/OPENSTACK_HOST/{s/.*/OPENSTACK_HOST='1.1.1.101' /g}"  settings_dashboard.py 
}


function  change_to_192()
{
sed -i  "/LOCATION/{s/.*/'LOCATION': \['192.168.130.141:11211'\],/}"   settings_dashboard.py 
sed -i  "/OPENSTACK_HOST/{s/.*/OPENSTACK_HOST='192.168.130.141' /g}"  settings_dashboard.py 
}

change_to_127
#change_to_1_1_1
#change_to_192

