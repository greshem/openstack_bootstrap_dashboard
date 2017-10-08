$(document).ready(function () {
	$("#floatingipTable").bootstrapTable(
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
});
function fixed_ip_address_fomatter(value,row){
	return row['fixed_ip_info']+value?row['fixed_ip_info']+value:null
}


function check_row(row){
	$("#floatingip_meun").find('li').removeClass('disabled');
	if($("#floatingipTable").bootstrapTable('getSelections').length==1){
		$("#btn_floatingip_delete").removeClass('btn-6')
		$("#btn_floatingip_delete").addClass('btn-5')
		row=$("#floatingipTable").bootstrapTable('getSelections')[0]
		if(row.fixed_ip_address){
			$("#floatingip_associate").addClass('disabled')
			$("#floatingip_disassociate").removeClass('disabled')
		}else{
			$("#floatingip_disassociate").addClass('disabled')
			$("#floatingip_associate").removeClass('disabled')
		}
	}else if($("#floatingipTable").bootstrapTable('getSelections').length > 1){
		$("#floatingip_meun").find('li').addClass('disabled');
		$("#floatingip_delete").removeClass('disabled');
		$("#btn_floatingip_delete").removeClass('btn-6')
		$("#btn_floatingip_delete").addClass('btn-5')
	}else{
		$("#floatingip_meun").find('li').addClass('disabled');
		$("#btn_floatingip_delete").removeClass('btn-5');
		$("#btn_floatingip_delete").addClass('btn-6');
	}
}
function floatingip_init_btn(){
	$("#floatingip_meun").find('li').addClass('disabled');
	$("#btn_floatingip_delete").removeClass('btn-5');
	$("#btn_floatingip_delete").addClass('btn-6');
}

function search() {
	$("#floatingipTable").bootstrapTable('selectPage', 1)
}
function create_form_init(region_list_url,floatingip_billing_url){
	var region_id=null;
	$.ajax({
		url:region_list_url,
		type:"get",
		data:{},
		async:false,
        success:function (data){
        	if (data=='error'){
            	alert("取得区域信息失败!");
            	return
            }
            var regions= eval("(" + data + ")");
            if(regions.length<1)
            	return
            region_id=regions[0]['id']
        },
        error: function (data, status, e) {
            alert("赠送失败!");
        }
    });
	var billing_data=null
	$.ajax({
		url:floatingip_billing_url+'?region_id='+region_id,
		type:"get",
		data:{},
		async:false,
        success:function (data){
        	if (data=='error'){
            	alert("取得计费信息失败!");
            	return
            }
        	billing_data=eval("(" + data + ")");
        },
        error: function (data, status, e) {
            alert("赠送失败!");
        }
    });
	getTotalPrice_floatingip(billing_data,'#floatingip_size','#price_hour','#price_year')
}
function getTotalPrice_floatingip(billing_data,floatingip_size,price_hour,price_year){
	total=billing_data['ip_1']['price']*billing_data['ip_1']['discount_ratio']
	$(price_hour).empty()
	$(price_hour).append(money_formatter(total))
	$(price_year).empty()
	$(price_year).append(money_formatter(total*24*30))
}
function floatingip_create_form(region_list_url,floatingip_billing_url,floatingip_pool_list_url){
	$("#floatingip_create_form").modal()
	$.ajax({
		url:floatingip_pool_list_url,
		type:"get",
		data:{},
		async:false,
        success:function (data){
        	if (data=='error'){
            	alert("取得资源池信息失败!");
            	return
            }
        	pools=eval("(" + data + ")");
        	$("#floatingip_pool").empty()
        	for(var key in pools){
        		$("#floatingip_pool").append('<div class="radio"><label><input type="radio" data-bv-notempty-message="请选择资源池"  name="floatingip_pool"value="'+pools[key].id+'" data-bv-notempty>'+pools[key].name+'</label></div>')
        	}
        },
        error: function (data, status, e) {
            alert("赠送失败!");
        }
    });
	//create_form_init(region_list_url,floatingip_billing_url)
}

function floatingip_create_action(floatingip_create_url){
	var floatingip_form= $("#floatingip_create_form").find('form').eq(0)
	if(floatingip_form.data('bootstrapValidator')){
		$(floatingip_form).data('bootstrapValidator',null);
	}
	floatingip_form.bootstrapValidator('validate')
    if(!floatingip_form.data('bootstrapValidator').isValid())
	    return
	pool_id=$("input[name='floatingip_pool']:checked").val()
	$("#floatingip_create_form").mask('浮动IP创建中，请稍后......')
	$.ajax({
		url:floatingip_create_url,
		type:"post",
		data:{'pool_id':pool_id},
		async:false,
        success:function (data){
        	$("#floatingip_create_form").unmask()
        	if (data=='success'){
        		$("#floatingip_create_form").modal('toggle');
        		$("#floatingipTable").bootstrapTable('refresh');
        		floatingip_init_btn()
            }else{
            	alert('浮动IP创建失败')
            }
        },
        error: function (data, status, e) {
        	$("#floatingip_create_form").unmask()
            alert("赠送失败!");
        }
    });
}
function device_owner_formatter(value,row){
	if(value=='compute:nova'){
		return '云主机'
	}else if(value=='neutron:LOADBALANCERV2'){
		return '负载均衡'
	}
	return '其它'	
	
}
function floatingip_associate_form(){
	rows=$("#floatingipTable").bootstrapTable("getSelections")
	if(rows.length!=1){
		return
	}
	row=rows[0]
	if(row.fixed_ip_address){
		return
	}
	$("#floatingip_associate_form").modal()
	$("#portTable_associate").bootstrapTable({
		'clickToSelect':true,
		'singleSelect':true
	})
	$("#portTable_associate").bootstrapTable('refresh');
	
	
}

function floatingip_associate_action(floatingip_associate_url){
	rows=$("#portTable_associate").bootstrapTable('getSelections')
	if(rows.length<1){
		alert('请选择关联端口')
		return
	}
	if(rows[0].device_owner!='compute:nova' && rows[0].device_owner!='neutron:LOADBALANCERV2'){
		alert('请选择云主机或者负载均衡类型端口')
		return
	}
	if(rows[0].floating_ip_address){
		alert('该端口已经关联IP')
		return
	}
	var floatingip_id=$("#floatingipTable").bootstrapTable("getSelections")[0].id
	$("#floatingip_associate_form").mask('浮动IP扩展中，请稍后......')
	$.ajax({
		url:floatingip_associate_url,
		type:"post",
		data:{'port_id':rows[0].id,'floatingip_id':floatingip_id,'fixed_ip_address':rows[0].fixed_ip_address},
		async:false,
        success:function (data){
        	$("#floatingip_associate_form").unmask()
        	if (data=='success'){
        		$("#floatingip_associate_form").modal('toggle');
        		$("#floatingipTable").bootstrapTable('refresh');
        		floatingip_init_btn()
            }else{
            	alert("浮动IP扩展失败")
            }
        },
        error: function (data, status, e) {
        	$("#floatingip_associate_form").unmask()
            alert("赠送失败!");
        }
    });
}

function floatingip_delete_action(floatingip_delete_url){
	rows=$("#floatingipTable").bootstrapTable('getSelections')
	if(rows.length<1){
		return
	}
	var floatingip_ids=""
	for(var key in rows){
		if(floatingip_ids){
			floatingip_ids=floatingip_ids+","+rows[key].id
		}else{
			floatingip_ids=rows[key].id
		}
	}
	$.ajax({
		url:floatingip_delete_url,
		type:"post",
		data:{'floatingip_ids':floatingip_ids},
		async:false,
        success:function (data){
            if (data=='success'){
        		$("#floatingipTable").bootstrapTable('refresh');
        		floatingip_init_btn()
            }
            else{
                alert("删除浮动IP失败");
            }

        },
        error: function (data, status, e) {
            alert("赠送失败!");
        }
    });
}

function floatingip_disassociate_action(floatingip_disassociate_url){
	rows=$("#floatingipTable").bootstrapTable("getSelections")
	if(rows.length!=1){
		return
	}
	row=rows[0]
	if(!row.fixed_ip_address){
		return
	}
	$.ajax({
		url:floatingip_disassociate_url+'?floatingip_id='+row.id,
		type:"get",
		data:{},
		async:false,
        success:function (data){
        	if (data=='success'){
        		$("#floatingipTable").bootstrapTable('refresh');
        		floatingip_init_btn()
            }else{
            	alert("浮动IP扩展失败")
            }
        },
        error: function (data, status, e) {
            alert("赠送失败!");
        }
    });
}