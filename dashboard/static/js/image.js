$(document).ready(function () {
	$("#imageTable").bootstrapTable(
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
	update_instance_status();
});

function check_row(row){
	$("#image_meun").find('li').removeClass('disabled');
	rows=$("#imageTable").bootstrapTable('getSelections')
	if(rows.length==1){
		if(rows[0].is_owner==true){
			$("#btn_image_delete").removeClass('btn-6')
			$("#btn_image_delete").addClass('btn-5')
			$("#image_delete").removeClass('disabled');
		}else{
			$("#image_meun").find('li').addClass('disabled');
		}
	}else if(rows.length > 1){
		$("#image_meun").find('li').addClass('disabled');
		$("#image_delete").removeClass('disabled');
		$("#btn_image_delete").removeClass('btn-6')
		$("#btn_image_delete").addClass('btn-5')
		for(var key in rows){
			if(rows[key].is_owner==false){
				$("#image_meun").find('li').addClass('disabled');
				$("#btn_image_delete").removeClass('btn-5');
				$("#btn_image_delete").addClass('btn-6');
				return
			}
		}
	}else{
		$("#image_meun").find('li').addClass('disabled');
		$("#btn_image_delete").removeClass('btn-5');
		$("#btn_image_delete").addClass('btn-6');
	}
}
function image_init_btn(){
	$("#image_meun").find('li').addClass('disabled');
	$("#btn_image_delete").removeClass('btn-5');
	$("#btn_image_delete").addClass('btn-6');
}

function search() {
	$("#imageTable").bootstrapTable('selectPage', 1)
}

function image_edit_form(){
	rows=$("#imageTable").bootstrapTable('getSelections')
	if(rows.length!=1){
		return
	}
	row=rows[0]
	if(row.is_owner!=true){
		return
	}
	$("#image_edit_form").modal()
	$("input[for='number']").numeral(5)
	$("#image_name_edit").val(row.name)
	$("#image_description_edit").val(row.description)
	$("#image_min_disk_edit").val(row.min_disk)
	$("#image_min_ram_edit").val(row.min_ram)
	if(row.is_public==true){
		$("#image_is_public_edit").attr('checked','true')
	}else{
		$("#image_is_public_edit").removeAttr('checked')
	}
	if(row.protected==true){
		$("#image_protected_edit").attr('checked','true')
	}else{
		$("#image_protected_edit").removeAttr('checked')
	}
}

function image_edit_action(image_edit_url){
	row=$("#imageTable").bootstrapTable("getSelections")[0]
	$("#image_edit_form").mask('云硬盘编辑中，请稍后......')
	var is_public=false
	if($("#image_is_public_edit").attr("checked")){
		is_public=true
	}
	var protect=false
	if($("#image_protected_edit").attr("checked")){
		protect=true
	}
	$.ajax({
		url:image_edit_url,
		type:"post",
		data:{'root':JSON.stringify({'image_id':row.id,'data':{'name':$("#image_name_edit").val(),'min_ram':$("#image_min_ram_edit").val(),'min_disk':$("#image_min_disk_edit").val(),
			'is_public':is_public,'protected':protect,'properties':{'description':$("#image_description_edit").val()}}})},
		async:false,
        success:function (data){
        	$("#image_edit_form").unmask()
        	if (data=='success'){
        		$("#image_edit_form").modal('toggle');
        		$("#imageTable").bootstrapTable('refresh');
        		image_init_btn()
            }else{
            	alert("云硬盘扩展失败")
            }
        },
        error: function (data, status, e) {
        	$("#image_edit_form").unmask()
            alert("赠送失败!");
        }
    });
}


function image_delete_action(image_delete_url){
	rows=$("#imageTable").bootstrapTable('getSelections')
	if(rows.length<1){
		return
	}
	var image_ids=""
	for(var key in rows){
		if(rows[key].is_owner==false){
			return
		}
		if(image_ids){
			image_ids=image_ids+","+rows[key].id
		}else{
			image_ids=rows[key].id
		}
	}
	$.ajax({
		url:image_delete_url,
		type:"post",
		data:{'image_ids':image_ids},
		async:false,
        success:function (data){
            if (data=='success'){
        		$("#imageTable").bootstrapTable('refresh');
        		image_init_btn()
            }
            else{
                alert("删除镜像失败");
            }

        },
        error: function (data, status, e) {
            alert("赠送失败!");
        }
    });
}









function create_form_init(region_list_url,image_billing_url){
	$("#image_name").val("");
	$("#image_size").val(1);
	$("#image_description").val("");
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
		url:image_billing_url+'?region_id='+region_id,
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
	getTotalPrice_image(billing_data,'#image_size','#price_hour','#price_year')
	$("#image_size").on('input',function(e){
		getTotalPrice_image(billing_data,'#image_size','#price_hour','#price_year')
	});  
}
function getTotalPrice_image(billing_data,image_size,price_hour,price_year){
	total=$(image_size).val()*billing_data['disk_1_G']['price']*billing_data['disk_1_G']['discount_ratio']
	$(price_hour).empty()
	$(price_hour).append(money_formatter(total))
	$(price_year).empty()
	$(price_year).append(money_formatter(total*24*30))
}
function image_create_form(zone_list_url,region_list_url,image_billing_url){
	$("#image_create_form").modal()
	create_form_init(region_list_url,image_billing_url)
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
        	$('#image_zone').empty()
            for(var key in zone_list){
            	var option = $("<option>").val(zone_list[key]['zoneName']).text(zone_list[key]['zoneName']);
            	$('#image_zone').append(option)
            }
        },
        error: function (data, status, e) {
            alert("赠送失败!");
        }
    });
}

function image_create_action(image_create_url){
	var name=$("#image_name").val();
	var size=$("#image_size").val();
	var description=$("#image_description").val()
	var availability_zone=$('#image_zone').val()
	$("#image_create_form").mask('云硬盘创建中，请稍后......')
	$.ajax({
		url:image_create_url,
		type:"post",
		data:{'name':name,'size':size,'description':description,'availability_zone':availability_zone},
		async:false,
        success:function (data){
        	$("#image_create_form").unmask()
        	if (data=='success'){
        		$("#image_create_form").modal('toggle');
        		$("#imageTable").bootstrapTable('refresh');
        		image_init_btn()
            }else{
            	alert('云硬盘创建失败')
            }
        },
        error: function (data, status, e) {
        	$("#image_create_form").unmask()
            alert("赠送失败!");
        }
    });
}

function extend_form_init(row,region_list_url,image_billing_url){
	$("input[for='number']").numeral(4)
	$("#image_name_extend").empty()
	$("#image_name_extend").append(row.name);
	$("#image_size_extend_old").empty();
	$("#image_size_extend_old").append(row.size)
	$("#image_size_extend").val(row.size);
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
		url:image_billing_url+'?region_id='+region_id,
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
	getTotalPrice_image(billing_data,'#image_size_extend','#price_hour_extend','#price_year_extend')
	$("#image_size_extend").on('input',function(e){
		getTotalPrice_image(billing_data,'#image_size_extend','#price_hour_extend','#price_year_extend')
	});  
}

function image_extend_form(region_list_url,image_billing_url){
	if($("#imageTable").bootstrapTable('getSelections').length!=1){
		return
	}
	row=$("#imageTable").bootstrapTable('getSelections')[0]
	$("#image_extend_form").modal()
	extend_form_init(row,region_list_url,image_billing_url)
}
function image_extend_action(image_extend_url){
	row=$("#imageTable").bootstrapTable('getSelections')[0]
	var image_size_new=$("#image_size_extend").val()
	if(image_size_new<=row.size){
		alert('扩展云硬盘大小不应该小于原大小')
		return
	}
	$("#image_extend_form").mask('云硬盘扩展中，请稍后......')
	$.ajax({
		url:image_extend_url,
		type:"post",
		data:{'id':row.id,'size':image_size_new},
		async:false,
        success:function (data){
        	$("#image_extend_form").unmask()
        	if (data=='success'){
        		$("#image_extend_form").modal('toggle');
        		$("#imageTable").bootstrapTable('refresh');
        		image_init_btn()
            }else{
            	alert("云硬盘扩展失败")
            }
        },
        error: function (data, status, e) {
        	$("#image_extend_form").unmask()
            alert("赠送失败!");
        }
    });
}



function image_detach_action(image_detach_url){
	rows=$("#imageTable").bootstrapTable("getSelections")
	if(rows.length!=1){
		return
	}
	row=rows[0]
	if(row.status!='in-use'){
		return
	}
	$.ajax({
		url:image_detach_url,
		type:"post",
		data:{'image_id':row.id},
		async:false,
        success:function (data){
        	if (data=='success'){
        		$("#imageTable").bootstrapTable('refresh');
        		image_init_btn()
            }else{
            	alert("云硬盘扩展失败")
            }
        },
        error: function (data, status, e) {
            alert("赠送失败!");
        }
    });
}

function image_attach_form(){
	rows=$("#imageTable").bootstrapTable("getSelections")
	if(rows.length!=1){
		return
	}
	row=rows[0]
	if(row.status!='available'){
		return
	}
	$("#image_attach_form").modal()
	$("#instanceTable_attach").bootstrapTable({
		'clickToSelect':true,
		'singleSelect':true
	})
	$("#instanceTable_attach").bootstrapTable('refresh');
}


function image_attach_action(image_attach_url){
	rows=$("#instanceTable_attach").bootstrapTable("getSelections")
	if(rows.length!=1){
		return
	}
	row=rows[0]
	row_image=$("#imageTable").bootstrapTable("getSelections")[0]
	$.ajax({
		url:image_attach_url,
		type:"post",
		data:{'instance_id':row.id,'image_id':row_image.id},
		async:false,
        success:function (data){
        	if (data=='success'){
        		$("#image_attach_form").modal('toggle')
        		$("#imageTable").bootstrapTable('refresh');
        		image_init_btn()
            }else{
            	alert("云硬盘扩展失败")
            }
        },
        error: function (data, status, e) {
            alert("赠送失败!");
        }
    });
	
}

function get_image_status(){
	$("#imageTable tbody tr").each(function(){
		var status_td = $(this).find("td:eq(3)");
		var status_value = status_td.html();
		if("active"!=status_value){
			var $key = $(this).find("td:eq(0)").find("input").attr("data-index");
			var $obj = $("#imageTable").bootstrapTable('getData');
			var $image_id = $obj[$key].id; 
			//alert("id:"+$instance_id+"   name:"+$name+"  ip:"+$ip+"   status:"+$status);
			$.ajax({
				url:"/project/image/image_get",
				type:"get",
				data:{'image_id':$instance_id},
				async:false,
		        success:function (data){
		        	if(data){
		        		var instance = eval("(" + data + ")");
			        	status_td.html(instance[0]["status"]);
		        	}
		        },
		    });
		}
	});
}
function update_instance_status(){
	setInterval("get_image_status()",5000);
}