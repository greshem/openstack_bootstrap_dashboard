$(document).ready(function () {
	$("#router_routeTable").bootstrapTable(
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
	$("#router_route_meun").find('li').removeClass('disabled');
	if($("#router_routeTable").bootstrapTable('getSelections').length==1){
		$("#btn_router_route_delete").removeClass('btn-6')
		$("#btn_router_route_delete").addClass('btn-5')
	}else if($("#router_routeTable").bootstrapTable('getSelections').length > 1){
		$("#router_route_meun").find('li').addClass('disabled');
		$("#router_route_delete").removeClass('disabled');
		$("#btn_router_route_delete").removeClass('btn-6')
		$("#btn_router_delete").addClass('btn-5')
	}else{
		$("#router_route_meun").find('li').addClass('disabled');
		$("#btn_router_route_delete").removeClass('btn-5');
		$("#btn_router_route_delete").addClass('btn-6');
	}
}
function router_route_init_btn(){
	$("#router_route_meun").find('li').addClass('disabled');
	$("#btn_router_route_delete").removeClass('btn-5');
	$("#btn_router_route_delete").addClass('btn-6');
}
function search() {
	$("#router_routeTable").bootstrapTable('refresh')
}
function router_route_create_form(){
	var router_route_form= $("#router_route_create_form").find('form').eq(0)
	if(router_route_form.data('bootstrapValidator')){
		$(router_form).data('bootstrapValidator').resetForm()
	}
	router_route_form[0].reset();
	$("#router_route_create_form").modal()
}

function router_route_create_action(router_route_create_url){
	var router_route_form= $("#router_route_create_form").find('form').eq(0)
	if(router_route_form.data('bootstrapValidator')){
		$(router_route_form).data('bootstrapValidator',null);
	}
	router_route_form.bootstrapValidator('validate')
    if(!router_route_form.data('bootstrapValidator').isValid())
	    return
	$("#router_route_create_form").mask('云硬盘创建中，请稍后......')
	$.ajax({
		url:router_route_create_url,
		type:"post",
		data:{'router_id':$('#router_id').val(),'cidr':$("#router_route_cidr").val(),'nexthop':$("#router_route_nexthop").val()},
		async:false,
        success:function (data){
        	$("#router_route_create_form").unmask()
        	if (data=='success'){
        		$("#router_route_create_form").modal('toggle');
        		$("#router_routeTable").bootstrapTable('refresh');
        		router_route_init_btn()
            }else{
            	alert('路由器创建失败')
            }
        },
        error: function (data, status, e) {
        	$("#router_route_create_form").unmask()
            alert("赠送失败!");
        }
    });
}


function router_route_delete_action(router_route_delete_url,router_id){
	rows=$("#router_routeTable").bootstrapTable('getSelections')
	if(rows.length<1){
		return
	}
	var router_route_ids=""
	for(var key in rows){
		if(router_route_ids){
			router_route_ids=router_route_ids+","+rows[key].id
		}else{
			router_route_ids=rows[key].id
		}
	}
	$.ajax({
		url:router_route_delete_url,
		type:"post",
		data:{'router_route_ids':router_route_ids,'router_id':router_id},
		async:false,
        success:function (data){
            if (data=='success'){
        		$("#router_routeTable").bootstrapTable('refresh');
        		router_route_init_btn()
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
