$(document).ready(function () {
	$("#router_portTable").bootstrapTable(
            {
            	'clickToSelect':true,
                'queryParams' : function(params) {
                	var opt=$('#search_opt option:selected').val();
                	var value=$("#search_input").val()
                	if(value.length>0){
                		params[opt]=value
                	}
                    return params
                }
            });
});

function search() {
	$("#router_portTable").bootstrapTable('selectPage', 1)
}

function router_port_edit_form(id,name,admin_state){
	$("#router_port_name_edit").val(name)
	$("#router_port_id_edit").val(id)
	$("#router_port_admin_state_edit").val(admin_state)
	$("#router_port_edit_form").modal()
}

function router_port_edit_action(router_port_edit_url){
	row=$("#router_portTable").bootstrapTable("getSelections")[0]
	$("#router_port_edit_form").mask('云硬盘编辑中，请稍后......')
	$.ajax({
		url:router_port_edit_url,
		type:"post",
		data:{'port_id':$("#router_port_id_edit").val(),'router_port_name':$("#router_port_name_edit").val(),'admin_state':$("#router_port_admin_state_edit").val()},
		async:false,
        success:function (data){
        	$("#router_port_edit_form").unmask()
        	if (data=='success'){
        		$("#router_port_edit_form").modal('toggle');
        		$("#router_portTable").bootstrapTable('refresh');
            }else{
            	alert("云硬盘扩展失败")
            }
        },
        error: function (data, status, e) {
        	$("#router_port_edit_form").unmask()
            alert("赠送失败!");
        }
    });
}

function router_port_delete_action(router_port_delete_url,port_id,router_id){
	$.ajax({
		url:router_port_delete_url+'?port_id='+port_id+'&router_id='+router_id,
		type:"get",
		data:{},
		async:false,
        success:function (data){
            if (data=='success'){
        		$("#router_portTable").bootstrapTable('refresh');
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

