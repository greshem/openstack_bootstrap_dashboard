$(document).ready(function () {
	$("#networkTable").bootstrapTable(
            {
            	'clickToSelect':true,
                'queryParams' : function(params) {
                	var opt=$('#search_opt option:selected').val();
                	var value=$("#search_input").val()
                	if(value.length>0){
                		params[opt]=value
                	}
                    return params
                },
                'onAll':check_row
            });
	$("#network_subnet_cidr").focusout(function(){
		var cidrtext = $("#network_subnet_cidr").val();
		if(checknet(cidrtext)){
			var cidrsub  = cidrtext.substring(0,cidrtext.lastIndexOf("."));
			$("#gateway_ip").val(cidrsub+".1");
			$("#allocation_pools").val(cidrsub+".2,"+cidrsub+".254");
		}else{
			alert("请输入合法的网络地址（网段）");
		}
	});
});
function checknet(obj){
	var reg = 	/^(([01]?\d?\d|2[0-4]\d|25[0-5])\.){3}([01]?\d?\d|2[0-4]\d|25[0-5])\/(\d{1}|[0-2]{1}\d{1}|3[0-2])$/;
	return reg.test(obj);
}

function check_row(row){
	$("#network_meun").find('li').removeClass('disabled');
	if($("#networkTable").bootstrapTable('getSelections').length==1){
		$("#btn_network_delete").removeClass('btn-6')
		$("#btn_network_delete").addClass('btn-5')
	}else if($("#networkTable").bootstrapTable('getSelections').length > 1){
		$("#network_meun").find('li').addClass('disabled');
		$("#network_delete").removeClass('disabled');
		$("#btn_network_delete").removeClass('btn-6')
		$("#btn_network_delete").addClass('btn-5')
	}else{
		$("#network_meun").find('li').addClass('disabled');
		$("#btn_network_delete").removeClass('btn-5');
		$("#btn_network_delete").addClass('btn-6');
	}
}
function network_init_btn(){
	$("#network_meun").find('li').addClass('disabled');
	$("#btn_network_delete").removeClass('btn-5');
	$("#btn_network_delete").addClass('btn-6');
}

function search() {
	$("#networkTable").bootstrapTable('selectPage', 1)
}
function network_create_form(){
	var network_form= $("#network_create_form").find('form').eq(0)
	if(network_form.data('bootstrapValidator')){
		$(network_form).data('bootstrapValidator').resetForm()
	}
	network_form[0].reset();
	$("#network_subnet_gateway").removeClass('display-none')
	$("input[name=network_subnet_isgateway]").change(function(event){
		if(this.value=='no'){
			$("#gateway_ip").removeClass('display-none')
		}else if(this.value=='yes'){
			$("#gateway_ip").addClass('display-none')
		}else{
		}
	});
	$("#network_create_form").modal()
}

function network_create_action(network_create_url){
	var network_form= $("#network_create_form").find('form').eq(0)
	if(network_form.data('bootstrapValidator')){
		$(network_form).data('bootstrapValidator',null);
	}
	network_form.bootstrapValidator('validate')
    if(!network_form.data('bootstrapValidator').isValid())
	    return
	pool_id=$("input[name='network_pool']:checked").val()
	$("#network_create_form").mask('网络创建中，请稍后......')
	var gateway_ip=null
	if($("input[name=network_subnet_isgateway]").val()=='no'){
		gateway_ip=$("#gateway_ip").val()
	}
	var enable_dhcp=true
	if($("input[name=network_subnet_dhcp]").val()=='no'){
		enable_dhcp=false
	}
	$.ajax({
		url:network_create_url,
		type:"post",
		data:{'net_name':$('#net_name').val(),'admin_state':$("#admin_state").val(),'subnet_name':$("#subnet_name").val(),'cidr':$("#network_subnet_cidr").val()
		,'gateway_ip':gateway_ip,'enable_dhcp':enable_dhcp,'allocation_pools':$("#allocation_pools").val(),'host_routes':$("#host_routes").val(),'dns_nameservers':$("#dns_nameservers").val()
		},
		async:false,
        success:function (data){
        	$("#network_create_form").unmask()
        	if (data=='success'){
        		$("#network_create_form").modal('toggle');
        		$("#networkTable").bootstrapTable('refresh');
        		network_init_btn()
            }else{
            	alert('网络创建失败')
            }
        },
        error: function (data, status, e) {
        	$("#network_create_form").unmask()
            alert("赠送失败!");
        }
    });
}


function network_delete_action(network_delete_url){
	rows=$("#networkTable").bootstrapTable('getSelections')
	if(rows.length<1){
		return
	}
	var network_ids=""
	for(var key in rows){
		if(network_ids){
			network_ids=network_ids+","+rows[key].id
		}else{
			network_ids=rows[key].id
		}
	}
	$.ajax({
		url:network_delete_url,
		type:"post",
		data:{'network_ids':network_ids},
		async:false,
        success:function (data){
            if (data=='success'){
        		$("#networkTable").bootstrapTable('refresh');
        		network_init_btn()
            }
            else{
                alert("删除网络失败");
            }

        },
        error: function (data, status, e) {
            alert("赠送失败!");
        }
    });
}


function network_edit_form(){
	rows=$("#networkTable").bootstrapTable('getSelections')
	if(rows.length!=1){
		return
	}
	row=rows[0]
	$("#network_name_edit").val(row.name)
	$("#network_admin_state_edit").val(row.admin_state)
	$("#network_edit_form").modal()
}

function network_edit_action(network_edit_url){
	row=$("#networkTable").bootstrapTable("getSelections")[0]
	$("#network_edit_form").mask('网络编辑中，请稍后......')
	$.ajax({
		url:network_edit_url,
		type:"post",
		data:{'network_id':row.id,'name':$("#network_name_edit").val(),'admin_state':$("#network_admin_state_edit").val()},
		async:false,
        success:function (data){
        	$("#network_edit_form").unmask()
        	if (data=='success'){
        		$("#network_edit_form").modal('toggle');
        		$("#networkTable").bootstrapTable('refresh');
        		network_init_btn()
            }else{
            	alert("网络扩展失败")
            }
        },
        error: function (data, status, e) {
        	$("#network_edit_form").unmask()
            alert("赠送失败!");
        }
    });
}


function subnet_edit_form(subnet_show_url){
	rows=$("#networkTable").bootstrapTable('getSelections')
	if(rows.length!=1){
		return
	}
	row=rows[0]
	$("input[name=network_subnet_isgateway_edit]").change(function(event){
		if(this.value=='no'){
			$("#gateway_ip_edit").removeClass('display-none')
		}else if(this.value=='yes'){
			$("#gateway_ip_edit").addClass('display-none')
		}else{
		}
	});
	$.ajax({
		url:subnet_show_url+'?subnet_id='+row.subnet_id,
		type:"get",
		data:{},
		async:false,
        success:function (data){
        	if (data=='error'){
            	alert("取得区域信息失败!");
            	return
            }
            var subnet= eval("(" + data + ")");
            $("#subnet_name_edit").val(subnet.name)
            $("#network_subnet_cidr_edit").val(subnet.cidr)
            $("#gateway_ip_edit").val(subnet.gateway_ip)
            $("input[name=network_subnet_isgateway_edit]").removeAttr('checked')
            if(subnet.gateway_ip){
            	$("input[name=network_subnet_isgateway_edit][value=no]").attr("checked",'checked')
            	$("#gateway_ip_edit").removeClass('display-none')
            }else{
            	$("input[name=network_subnet_isgateway_edit][value=yes]").attr("checked",'checked')
            	$("#gateway_ip_edit").addClass('display-none')
            }
            $("#allocation_pools_edit").val(subnet.allocation_pools)
            $("#dns_nameservers_edit").val(subnet.dns_nameservers)
            $("#host_routes_edit").val(subnet.host_routes)
            if(subnet.enable_dhcp){
            	$("input[name=network_subnet_dhcp_edit]").removeAttr('checked')
            	$("input[name=network_subnet_dhcp_edit][value=yes]").attr("checked",'checked')
            }
        },
        error: function (data, status, e) {
            alert("赠送失败!");
            return
        }
    });
	
	$("#subnet_edit_form").modal()
}

function subnet_edit_action(subnet_update_url){
	var subnet_edit_form= $("#subnet_edit_form").find('form').eq(0)
	if(subnet_edit_form.data('bootstrapValidator')){
		$(subnet_edit_form).data('bootstrapValidator',null);
	}
	subnet_edit_form.bootstrapValidator('validate')
    if(!subnet_edit_form.data('bootstrapValidator').isValid())
	    return
	row=$("#networkTable").bootstrapTable('getSelections')[0]
    var gateway_ip=null
	if($("input[name=network_subnet_isgateway_edit]:checked").val()=='no'){
		gateway_ip=$("#gateway_ip_edit").val()
	}
	var enable_dhcp=true
	if($("input[name=network_subnet_dhcp_edit]").val()=='no'){
		enable_dhcp=false
	}
	$("#subnet_edit_form").mask('网络创建中，请稍后......')
	$.ajax({
		url:subnet_update_url,
		type:"post",
		data:{'subnet_id':row.subnet_id,'subnet_name':$("#subnet_name_edit").val(),'gateway_ip':gateway_ip,'enable_dhcp':enable_dhcp,'allocation_pools':$("#allocation_pools_edit").val(),'host_routes':$("#host_routes_edit").val(),'dns_nameservers':$("#dns_nameservers_edit").val()
		},
		async:false,
        success:function (data){
        	$("#subnet_edit_form").unmask()
        	if (data=='success'){
        		$("#subnet_edit_form").modal('toggle');
        		$("#networkTable").bootstrapTable('refresh');
        		network_init_btn()
            }else{
            	alert('网络创建失败')
            }
        },
        error: function (data, status, e) {
        	$("#subnet_edit_form").unmask()
            alert("赠送失败!");
        }
    });
}
