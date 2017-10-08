$(document).ready(function () {
	$("#network_portTable").bootstrapTable(
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
	$("#network_portTable").bootstrapTable('selectPage', 1)
}

function network_port_edit_form(id,name,admin_state){
	$("#network_port_name_edit").val(name)
	$("#network_port_id_edit").val(id)
	$("#network_port_admin_state_edit").val(admin_state)
	$("#network_port_edit_form").modal()
}

function network_port_edit_action(network_port_edit_url){
	row=$("#network_portTable").bootstrapTable("getSelections")[0]
	$("#network_port_edit_form").mask('云硬盘编辑中，请稍后......')
	$.ajax({
		url:network_port_edit_url,
		type:"post",
		data:{'port_id':$("#network_port_id_edit").val(),'network_port_name':$("#network_port_name_edit").val(),'admin_state':$("#network_port_admin_state_edit").val()},
		async:false,
        success:function (data){
        	$("#network_port_edit_form").unmask()
        	if (data=='success'){
        		$("#network_port_edit_form").modal('toggle');
        		$("#network_portTable").bootstrapTable('refresh');
        		network_port_init_btn()
            }else{
            	alert("云硬盘扩展失败")
            }
        },
        error: function (data, status, e) {
        	$("#network_port_edit_form").unmask()
            alert("赠送失败!");
        }
    });
}
