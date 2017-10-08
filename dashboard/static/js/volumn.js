$(document).ready(function () {
	$("#volumeTable").bootstrapTable(
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
	$("#volume_meun").find('li').removeClass('disabled');
	if($("#volumeTable").bootstrapTable('getSelections').length==1){
		$("#btn_volume_delete").removeClass('btn-6')
		$("#btn_volume_delete").addClass('btn-5')
		row=$("#volumeTable").bootstrapTable('getSelections')[0]
		if(row.status!='available' && row.status!='in-use'){
			$("#volume_meun").find('li').addClass('disabled');
			$("#volume_delete").removeClass('disabled');
		}else if(row.status=='available'){
			$("#volume_detach").addClass('disabled');
		}else if(row.status=='in-use'){
			$("#volume_extend").addClass('disabled');
			$("#volume_attach").addClass('disabled');
		}
	}else if($("#volumeTable").bootstrapTable('getSelections').length > 1){
		$("#volume_meun").find('li').addClass('disabled');
		$("#volume_delete").removeClass('disabled');
		$("#btn_volume_delete").removeClass('btn-6')
		$("#btn_volume_delete").addClass('btn-5')
	}else{
		$("#volume_meun").find('li').addClass('disabled');
		$("#btn_volume_delete").removeClass('btn-5');
		$("#btn_volume_delete").addClass('btn-6');
	}
}
function volume_init_btn(){
	$("#volume_meun").find('li').addClass('disabled');
	$("#btn_volume_delete").removeClass('btn-5');
	$("#btn_volume_delete").addClass('btn-6');
}

function search() {
	$("#volumeTable").bootstrapTable('selectPage', 1)
}
function create_form_init(region_list_url,volume_billing_url){
	$("#volume_name").val("");
	$("#volume_size").val(1);
	$("#volume_description").val("");
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
		url:volume_billing_url+'?region_id='+region_id,
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
	getTotalPrice_volume(billing_data,'#volume_size','#price_hour','#price_year')
	$("#volume_size").on('input',function(e){
		getTotalPrice_volume(billing_data,'#volume_size','#price_hour','#price_year')
	});  
}
function getTotalPrice_volume(billing_data,volume_size,price_hour,price_year){
	total=$(volume_size).val()*billing_data['disk_1_G']['price']*billing_data['disk_1_G']['discount_ratio']
	$(price_hour).empty()
	$(price_hour).append(money_formatter(total))
	$(price_year).empty()
	$(price_year).append(money_formatter(total*24*30))
}
function volume_create_form(zone_list_url,region_list_url,volume_billing_url){
	$("#volume_create_form").modal()
	create_form_init(region_list_url,volume_billing_url)
	$("input[for='number']").numeral(4)
	$.ajax({
		url:zone_list_url,
		type:"get",
		data:{},
		async:false,
        success:function (data){
        	if (data=='error'){
            	alert("取得计费信息失败!");
            	return
            }
        	zone_list=eval("(" + data + ")");
        	$('#volume_zone').empty()
            for(var key in zone_list){
            	var option = $("<option>").val(zone_list[key]['zoneName']).text(zone_list[key]['zoneName']);
            	$('#volume_zone').append(option)
            }
        },
        error: function (data, status, e) {
            alert("赠送失败!");
        }
    });
}

function volume_create_action(volume_create_url){
	var name=$("#volume_name").val();
	var size=$("#volume_size").val();
	var description=$("#volume_description").val()
	var availability_zone=$('#volume_zone').val()
	$("#volume_create_form").mask('云硬盘创建中，请稍后......')
	$.ajax({
		url:volume_create_url,
		type:"post",
		data:{'name':name,'size':size,'description':description,'availability_zone':availability_zone},
		async:false,
        success:function (data){
        	$("#volume_create_form").unmask()
        	if (data=='success'){
        		$("#volume_create_form").modal('toggle');
        		$("#volumeTable").bootstrapTable('refresh');
        		volume_init_btn()
            }else{
            	alert('云硬盘创建失败')
            }
        },
        error: function (data, status, e) {
        	$("#volume_create_form").unmask()
            alert("赠送失败!");
        }
    });
}

function extend_form_init(row,region_list_url,volume_billing_url){
	$("input[for='number']").numeral(4)
	$("#volume_name_extend").empty()
	$("#volume_name_extend").append(row.name);
	$("#volume_size_extend_old").empty();
	$("#volume_size_extend_old").append(row.size)
	$("#volume_size_extend").val(row.size);
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
		url:volume_billing_url+'?region_id='+region_id,
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
	getTotalPrice_volume(billing_data,'#volume_size_extend','#price_hour_extend','#price_year_extend')
	$("#volume_size_extend").on('input',function(e){
		getTotalPrice_volume(billing_data,'#volume_size_extend','#price_hour_extend','#price_year_extend')
	});  
}

function volume_extend_form(region_list_url,volume_billing_url){
	if($("#volumeTable").bootstrapTable('getSelections').length!=1){
		return
	}
	row=$("#volumeTable").bootstrapTable('getSelections')[0]
	$("#volume_extend_form").modal()
	extend_form_init(row,region_list_url,volume_billing_url)
}
function volume_extend_action(volume_extend_url){
	row=$("#volumeTable").bootstrapTable('getSelections')[0]
	var volume_size_new=$("#volume_size_extend").val()
	if(volume_size_new<=row.size){
		alert('扩展云硬盘大小不应该小于原大小')
		return
	}
	$("#volume_extend_form").mask('云硬盘扩展中，请稍后......')
	$.ajax({
		url:volume_extend_url,
		type:"post",
		data:{'id':row.id,'size':volume_size_new},
		async:false,
        success:function (data){
        	$("#volume_extend_form").unmask()
        	if (data=='success'){
        		$("#volume_extend_form").modal('toggle');
        		$("#volumeTable").bootstrapTable('refresh');
        		volume_init_btn()
            }else{
            	alert("云硬盘扩展失败")
            }
        },
        error: function (data, status, e) {
        	$("#volume_extend_form").unmask()
            alert("赠送失败!");
        }
    });
}

function volume_delete_action(volume_delete_url){
	rows=$("#volumeTable").bootstrapTable('getSelections')
	if(rows.length<1){
		return
	}
	var volume_ids=""
	for(var key in rows){
		if(volume_ids){
			volume_ids=volume_ids+","+rows[key].id
		}else{
			volume_ids=rows[key].id
		}
	}
	$.ajax({
		url:volume_delete_url,
		type:"post",
		data:{'volume_ids':volume_ids},
		async:false,
        success:function (data){
            if (data=='success'){
        		$("#volumeTable").bootstrapTable('refresh');
        		volume_init_btn()
            }
            else{
                alert("删除云硬盘失败");
            }

        },
        error: function (data, status, e) {
            alert("赠送失败!");
        }
    });
}

function volume_edit_form(){
	rows=$("#volumeTable").bootstrapTable('getSelections')
	if(rows.length!=1){
		return
	}
	row=rows[0]
	$("#volume_name_edit").val(row.name)
	$("#volume_description_edit").val(row.description)
	$("#volume_edit_form").modal()
}

function volume_edit_action(volume_edit_url){
	row=$("#volumeTable").bootstrapTable("getSelections")[0]
	$("#volume_edit_form").mask('云硬盘编辑中，请稍后......')
	$.ajax({
		url:volume_edit_url,
		type:"post",
		data:{'volume_id':row.id,'name':$("#volume_name_edit").val(),'description':$("#volume_description_edit").val()},
		async:false,
        success:function (data){
        	$("#volume_edit_form").unmask()
        	if (data=='success'){
        		$("#volume_edit_form").modal('toggle');
        		$("#volumeTable").bootstrapTable('refresh');
        		volume_init_btn()
            }else{
            	alert("云硬盘扩展失败")
            }
        },
        error: function (data, status, e) {
        	$("#volume_edit_form").unmask()
            alert("赠送失败!");
        }
    });
}
function volume_detach_action(volume_detach_url){
	rows=$("#volumeTable").bootstrapTable("getSelections")
	if(rows.length!=1){
		return
	}
	row=rows[0]
	if(row.status!='in-use'){
		return
	}
	$.ajax({
		url:volume_detach_url,
		type:"post",
		data:{'volume_id':row.id},
		async:false,
        success:function (data){
        	if (data=='success'){
        		$("#volumeTable").bootstrapTable('refresh');
        		volume_init_btn()
            }else{
            	alert("云硬盘扩展失败")
            }
        },
        error: function (data, status, e) {
            alert("赠送失败!");
        }
    });
}

function volume_attach_form(){
	rows=$("#volumeTable").bootstrapTable("getSelections")
	if(rows.length!=1){
		return
	}
	row=rows[0]
	if(row.status!='available'){
		return
	}
	$("#volume_attach_form").modal()
	$("#instanceTable_attach").bootstrapTable({
		'clickToSelect':true,
		'singleSelect':true
	})
	$("#instanceTable_attach").bootstrapTable('refresh');
}


function volume_attach_action(volume_attach_url){
	rows=$("#instanceTable_attach").bootstrapTable("getSelections")
	if(rows.length!=1){
		return
	}
	row=rows[0]
	row_volume=$("#volumeTable").bootstrapTable("getSelections")[0]
	$.ajax({
		url:volume_attach_url,
		type:"post",
		data:{'instance_id':row.id,'volume_id':row_volume.id},
		async:false,
        success:function (data){
        	if (data=='success'){
        		$("#volume_attach_form").modal('toggle')
        		$("#volumeTable").bootstrapTable('refresh');
        		volume_init_btn()
            }else{
            	alert("云硬盘扩展失败")
            }
        },
        error: function (data, status, e) {
            alert("赠送失败!");
        }
    });
	
}