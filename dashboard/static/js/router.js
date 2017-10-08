$(document).ready(function () {
	$("#routerTable").bootstrapTable(
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

function check_row(row){
	$("#router_meun").find('li').removeClass('disabled');
	if($("#routerTable").bootstrapTable('getSelections').length==1){
		$("#btn_router_delete").removeClass('btn-6')
		$("#btn_router_delete").addClass('btn-5')
	}else if($("#routerTable").bootstrapTable('getSelections').length > 1){
		$("#router_meun").find('li').addClass('disabled');
		$("#router_delete").removeClass('disabled');
		$("#btn_router_delete").removeClass('btn-6')
		$("#btn_router_delete").addClass('btn-5')
	}else{
		$("#router_meun").find('li').addClass('disabled');
		$("#btn_router_delete").removeClass('btn-5');
		$("#btn_router_delete").addClass('btn-6');
	}
}
function router_init_btn(){
	$("#router_meun").find('li').addClass('disabled');
	$("#btn_router_delete").removeClass('btn-5');
	$("#btn_router_delete").addClass('btn-6');
}

function search() {
	$("#routerTable").bootstrapTable('selectPage', 1)
}
function create_form_init(region_list_url,router_billing_url){
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
		url:router_billing_url+'?region_id='+region_id,
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
	getTotalPrice_floatingip(billing_data,'#price_hour','#price_year')
}
function getTotalPrice_floatingip(billing_data,price_hour,price_year){
	total=billing_data['router_1']['price']*billing_data['router_1']['discount_ratio']
	$(price_hour).empty()
	$(price_hour).append(money_formatter(total))
	$(price_year).empty()
	$(price_year).append(money_formatter(total*24*30))
}
function router_create_form(region_list_url,router_billing_url,router_extnet_url){
	var router_form= $("#router_create_form").find('form').eq(0)
	if(router_form.data('bootstrapValidator')){
		$(router_form).data('bootstrapValidator').resetForm()
	}
	router_form[0].reset();
	$.ajax({
		url:router_extnet_url,
		type:"get",
		data:{},
		async:true,
        success:function (data){
        	if (data=='error'){
            	alert("取得区域信息失败!");
            	return
            }
            var extnets= eval("(" + data + ")");
            if(extnets.length<1)
            	return
        	$('#router_ext_net').empty()
            for(var key in extnets){
            	var option = $("<option>").val(extnets[key]['id']).text(extnets[key]['name']);
            	$('#router_ext_net').append(option)
            }
        },
        error: function (data, status, e) {
            alert("赠送失败!");
        }
    });
	//create_form_init(region_list_url,router_billing_url)
	$("#router_create_form").modal()
}

function router_create_action(router_create_url){
	var router_form= $("#router_create_form").find('form').eq(0)
	if(router_form.data('bootstrapValidator')){
		$(router_form).data('bootstrapValidator',null);
	}
	router_form.bootstrapValidator('validate')
    if(!router_form.data('bootstrapValidator').isValid())
	    return
	$("#router_create_form").mask('路由创建中，请稍后......')
	$.ajax({
		url:router_create_url,
		type:"post",
		data:{'name':$('#router_name').val(),'admin_state':$("#router_admin_state").val(),'router_ext_net_id':$("#router_ext_net").val()},
		async:false,
        success:function (data){
        	$("#router_create_form").unmask()
        	if (data=='success'){
        		$("#router_create_form").modal('toggle');
        		$("#routerTable").bootstrapTable('refresh');
        		router_init_btn()
            }else{
            	alert('路由器创建失败')
            }
        },
        error: function (data, status, e) {
        	$("#router_create_form").unmask()
            alert("赠送失败!");
        }
    });
}


function router_delete_action(router_delete_url){
	rows=$("#routerTable").bootstrapTable('getSelections')
	if(rows.length<1){
		return
	}
	var router_ids=""
	for(var key in rows){
		if(router_ids){
			router_ids=router_ids+","+rows[key].id
		}else{
			router_ids=rows[key].id
		}
	}
	$.ajax({
		url:router_delete_url,
		type:"post",
		data:{'router_ids':router_ids},
		async:false,
        success:function (data){
            if (data=='success'){
        		$("#routerTable").bootstrapTable('refresh');
        		router_init_btn()
            }
            else{
                alert("删除路由失败");
            }

        },
        error: function (data, status, e) {
            alert("赠送失败!");
        }
    });
}


function router_edit_form(){
	rows=$("#routerTable").bootstrapTable('getSelections')
	if(rows.length!=1){
		return
	}
	row=rows[0]
	$("#router_name_edit").val(row.name)
	$("#router_admin_state_edit").val(row.admin_state)
	$("#router_edit_form").modal()
}



function router_edit_action(router_edit_url){
	var router_form= $("#router_edit_form").find('form').eq(0)
	if(router_form.data('bootstrapValidator')){
		$(router_form).data('bootstrapValidator',null);
	}
	router_form.bootstrapValidator('validate')
    if(!router_form.data('bootstrapValidator').isValid())
	    return
	    
	row=$("#routerTable").bootstrapTable("getSelections")[0]
	$("#router_edit_form").mask('路由编辑中，请稍后......')
	$.ajax({
		url:router_edit_url,
		type:"post",
		data:{'router_id':row.id,'name':$("#router_name_edit").val(),'admin_state':$("#router_admin_state_edit").val()},
		async:false,
        success:function (data){
        	$("#router_edit_form").unmask()
        	if (data=='success'){
        		$("#router_edit_form").modal('toggle');
        		$("#routerTable").bootstrapTable('refresh');
        		router_init_btn()
            }else{
            	alert("路由扩展失败")
            }
        },
        error: function (data, status, e) {
        	$("#router_edit_form").unmask()
            alert("赠送失败!");
        }
    });
}

