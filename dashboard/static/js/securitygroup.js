$(document).ready(function () {
	$("#securitygroupTable").bootstrapTable(
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
	$("#securitygroup_meun").find('li').removeClass('disabled');
	rows=$("#securitygroupTable").bootstrapTable('getSelections')
	if(rows.length==1){
		$("#btn_securitygroup_delete").removeClass('btn-6')
		$("#btn_securitygroup_delete").addClass('btn-5')
	}else if(rows.length > 1){
		$("#securitygroup_meun").find('li').addClass('disabled');
		$("#securitygroup_delete").removeClass('disabled');
		$("#btn_securitygroup_delete").removeClass('btn-6')
		$("#btn_securitygroup_delete").addClass('btn-5')
	}else{
		$("#securitygroup_meun").find('li').addClass('disabled');
		$("#btn_securitygroup_delete").removeClass('btn-5');
		$("#btn_securitygroup_delete").addClass('btn-6');
	}
}
function securitygroup_init_btn(){
//	$("#securitygroup_meun").find('li').addClass('disabled');
	$("#btn_securitygroup_delete").removeClass('btn-5');
	$("#btn_securitygroup_delete").addClass('btn-6');
}

function search() {
	$("#securitygroupTable").bootstrapTable('selectPage', 1)
}

function securitygroup_edit_form(){
	rows=$("#securitygroupTable").bootstrapTable('getSelections')
	if(rows.length!=1){
		return
	}
	$("#securitygroup_edit_form").modal()
	$("#securitygroup_name_edit").val(rows[0].name)
	$("#securitygroup_description_edit").val(rows[0].description)
}

function securitygroup_edit_action(securitygroup_edit_url){
	var securitygroup_form= $("#securitygroup_edit_form").find('form').eq(0)
	securitygroup_form.bootstrapValidator('validate')
    if(!securitygroup_form.data('bootstrapValidator').isValid())
	    return
	row=$("#securitygroupTable").bootstrapTable("getSelections")[0]
	var name=$("#securitygroup_name_edit").val();
	var description=$("#securitygroup_description_edit").val()
	$.ajax({
		url:securitygroup_edit_url,
		type:"post",
		data:{'sg_id':row.id,'name':name,'description':description},
		async:false,
        success:function (data){
        	$("#securitygroup_edit_form").unmask()
        	if (data=='success'){
        		$("#securitygroup_edit_form").modal('toggle');
        		$("#securitygroupTable").bootstrapTable('refresh');
        		securitygroup_init_btn()
            }else{
            	alert("云硬盘扩展失败")
            }
        },
        error: function (data, status, e) {
        	$("#securitygroup_edit_form").unmask()
            alert("赠送失败!");
        }
    });
}


function securitygroup_delete_action(securitygroup_delete_url){
	rows=$("#securitygroupTable").bootstrapTable('getSelections')
	if(rows.length<1){
		return
	}
	var securitygroup_ids=""
	for(var key in rows){
		if(securitygroup_ids){
			securitygroup_ids=securitygroup_ids+","+rows[key].id
		}else{
			securitygroup_ids=rows[key].id
		}
	}
	$.ajax({
		url:securitygroup_delete_url,
		type:"post",
		data:{'sg_ids':securitygroup_ids},
		async:false,
        success:function (data){
            if (data=='success'){
        		$("#securitygroupTable").bootstrapTable('refresh');
        		securitygroup_init_btn()
            }
            else{
                alert("删除安全组失败");
            }

        },
        error: function (data, status, e) {
            alert("赠送失败!");
        }
    });
}

function securitygroup_create_form(zone_list_url,region_list_url,securitygroup_billing_url){
	$("#securitygroup_create_form").modal()
}

function securitygroup_create_action(securitygroup_create_url){
	var securitygroup_form= $("#securitygroup_create_form").find('form').eq(0)
	securitygroup_form.bootstrapValidator('validate')
    if(!securitygroup_form.data('bootstrapValidator').isValid())
	    return
	var name=$("#securitygroup_name").val();
	var description=$("#securitygroup_description").val()
	$("#securitygroup_create_form").mask('云硬盘创建中，请稍后......')
	$.ajax({
		url:securitygroup_create_url,
		type:"post",
		data:{'name':name,'description':description},
		async:false,
        success:function (data){
        	$("#securitygroup_create_form").unmask()
        	if (data=='success'){
        		$("#securitygroup_create_form").modal('toggle');
        		$("#securitygroupTable").bootstrapTable('refresh');
        		securitygroup_init_btn()
            }else{
            	alert('安全组创建失败')
            }
        },
        error: function (data, status, e) {
        	$("#securitygroup_create_form").unmask()
            alert("赠送失败!");
        }
    });
}
