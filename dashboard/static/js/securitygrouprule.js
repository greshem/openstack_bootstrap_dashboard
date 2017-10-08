$(document).ready(function () {
	$("#securitygroupruleTable").bootstrapTable(
            {
            	'clickToSelect':true,
                'onAll':check_row
            });
});

function check_row(row){
	$("#securitygrouprule_meun").find('li').removeClass('disabled');
	rows=$("#securitygroupruleTable").bootstrapTable('getSelections')
	if(rows.length==1){
		$("#btn_securitygrouprule_delete").removeClass('btn-6')
		$("#btn_securitygrouprule_delete").addClass('btn-5')
	}else if(rows.length > 1){
		$("#securitygrouprule_meun").find('li').addClass('disabled');
		$("#securitygrouprule_delete").removeClass('disabled');
		$("#btn_securitygrouprule_delete").removeClass('btn-6')
		$("#btn_securitygrouprule_delete").addClass('btn-5')
	}else{
		$("#securitygrouprule_meun").find('li').addClass('disabled');
		$("#btn_securitygrouprule_delete").removeClass('btn-5');
		$("#btn_securitygrouprule_delete").addClass('btn-6');
	}
}
function direction_formatter(value,row){
	if(value=='egress'){
		return '出口'
	}else if(value=='ingress'){
		return '入口'
	}else{
		return value
	}
}
function port_formatter(value,row){
	if(value==null){
		return '任何'
	}else{
		return value
	}
}
function protocol_formatter(value,row){
	if(value){
		return value
	}else{
		return '任何'
	}
}
function securitygrouprule_init_btn(){
//	$("#securitygrouprule_meun").find('li').addClass('disabled');
	$("#btn_securitygrouprule_delete").removeClass('btn-5');
	$("#btn_securitygrouprule_delete").addClass('btn-6');
}

function search() {
	$("#securitygroupruleTable").bootstrapTable('selectPage', 1)
}


function securitygrouprule_delete_action(securitygrouprule_delete_url){
	rows=$("#securitygroupruleTable").bootstrapTable('getSelections')
	if(rows.length<1){
		return
	}
	var securitygrouprule_ids=""
	for(var key in rows){
		if(securitygrouprule_ids){
			securitygrouprule_ids=securitygrouprule_ids+","+rows[key].id
		}else{
			securitygrouprule_ids=rows[key].id
		}
	}
	$.ajax({
		url:securitygrouprule_delete_url,
		type:"post",
		data:{'sgr_ids':securitygrouprule_ids},
		async:false,
        success:function (data){
            if (data=='success'){
        		$("#securitygroupruleTable").bootstrapTable('refresh');
        		securitygrouprule_init_btn()
            }
            else{
                alert("删除安全组规则失败");
            }

        },
        error: function (data, status, e) {
            alert("赠送失败!");
        }
    });
}
function securitygrouprule_create_form_init(securitygrouprule_menu_url,securitygroup_list_url){
	var securitygrouprule_form= $("#securitygrouprule_create_form").find('form').eq(0)
	if(securitygrouprule_form.data('bootstrapValidator')){
		$(securitygrouprule_form).data('bootstrapValidator').resetForm()
	}
	securitygrouprule_form[0].reset();
	$("#securitygrouprule_port").parent().parent().removeClass('display-none')
	$("#securitygrouprule_ip_protocol").parent().parent().addClass('display-none')
	$("#securitygrouprule_from_port").parent().parent().addClass('display-none')
	$("#securitygrouprule_to_port").parent().parent().addClass('display-none')
	$("#securitygrouprule_cidr").parent().parent().removeClass('display-none')
	$("#securitygrouprule_securitygroup").parent().parent().addClass('display-none')
	$("#securitygrouprule_ethertype").parent().parent().addClass('display-none')
	$("#securitygrouprule_port_type").change(function(event){
		if(this.value=='port'){
			$("#securitygrouprule_port").parent().parent().removeClass('display-none')
			$("#securitygrouprule_from_port").parent().parent().addClass('display-none')
			$("#securitygrouprule_to_port").parent().parent().addClass('display-none')
		}else if(this.value=='port_range'){
			$("#securitygrouprule_port").parent().parent().addClass('display-none')
			$("#securitygrouprule_from_port").parent().parent().removeClass('display-none')
			$("#securitygrouprule_to_port").parent().parent().removeClass('display-none')
		}else{
			
		}
	});
	$("#securitygrouprule_remote").change(function(event){
		if(this.value=='cidr'){
			$("#securitygrouprule_cidr").parent().parent().removeClass('display-none')
			$("#securitygrouprule_securitygroup").parent().parent().addClass('display-none')
			$("#securitygrouprule_ethertype").parent().parent().addClass('display-none')
		}else if(this.value=='securitygroup'){
			$("#securitygrouprule_cidr").parent().parent().addClass('display-none')
			$("#securitygrouprule_securitygroup").parent().parent().removeClass('display-none')
			$("#securitygrouprule_ethertype").parent().parent().removeClass('display-none')
		}else{
			
		}
	})
	$("#securitygrouprule_rule").change(function(event){
		var custom_rules=['tcp','udp','icmp']
		var all_rules=['all_tcp','all_udp','all_icmp']
		var other_rules=['custom']
		if(custom_rules.indexOf(this.value)!=-1){
			$("#securitygrouprule_rule").parent().parent().siblings().addClass('display-none')
			$("#securitygrouprule_direction").parent().parent().removeClass('display-none')
			$("#securitygrouprule_port_type").parent().parent().removeClass('display-none')
			$("#securitygrouprule_remote").parent().parent().removeClass('display-none')
			if($("#securitygrouprule_port_type").val()=='port'){
				$("#securitygrouprule_port").parent().parent().removeClass('display-none')
				$("#securitygrouprule_from_port").parent().parent().addClass('display-none')
				$("#securitygrouprule_to_port").parent().parent().addClass('display-none')
			}else if($("#securitygrouprule_port_type").val()=='port_range'){
				$("#securitygrouprule_port").parent().parent().addClass('display-none')
				$("#securitygrouprule_from_port").parent().parent().removeClass('display-none')
				$("#securitygrouprule_to_port").parent().parent().removeClass('display-none')
			}else{
			}
			if($("#securitygrouprule_remote").val()=='cidr'){
				$("#securitygrouprule_cidr").parent().parent().removeClass('display-none')
				$("#securitygrouprule_securitygroup").parent().parent().addClass('display-none')
				$("#securitygrouprule_ethertype").parent().parent().addClass('display-none')
			}else if($("#securitygrouprule_remote").val()=='securitygroup'){
				$("#securitygrouprule_cidr").parent().parent().addClass('display-none')
				$("#securitygrouprule_securitygroup").parent().parent().removeClass('display-none')
				$("#securitygrouprule_ethertype").parent().parent().removeClass('display-none')
			}else{
			}
		}else if(all_rules.indexOf(this.value)!=-1){
			$("#securitygrouprule_rule").parent().parent().siblings().addClass('display-none')
			$("#securitygrouprule_direction").parent().parent().removeClass('display-none')
			$("#securitygrouprule_remote").parent().parent().removeClass('display-none')
			if($("#securitygrouprule_remote").val()=='cidr'){
				$("#securitygrouprule_cidr").parent().parent().removeClass('display-none')
				$("#securitygrouprule_securitygroup").parent().parent().addClass('display-none')
				$("#securitygrouprule_ethertype").parent().parent().addClass('display-none')
			}else if($("#securitygrouprule_remote").val()=='securitygroup'){
				$("#securitygrouprule_cidr").parent().parent().addClass('display-none')
				$("#securitygrouprule_securitygroup").parent().parent().removeClass('display-none')
				$("#securitygrouprule_ethertype").parent().parent().removeClass('display-none')
			}else{
			}
		}else if(other_rules.indexOf(this.value)!=-1){
			$("#securitygrouprule_rule").parent().parent().siblings().addClass('display-none')
			$("#securitygrouprule_direction").parent().parent().removeClass('display-none')
			$("#securitygrouprule_ip_protocol").parent().parent().removeClass('display-none')
			$("#securitygrouprule_remote").parent().parent().removeClass('display-none')
			if($("#securitygrouprule_remote").val()=='cidr'){
				$("#securitygrouprule_cidr").parent().parent().removeClass('display-none')
				$("#securitygrouprule_securitygroup").parent().parent().addClass('display-none')
				$("#securitygrouprule_ethertype").parent().parent().addClass('display-none')
			}else if($("#securitygrouprule_remote").val()=='securitygroup'){
				$("#securitygrouprule_cidr").parent().parent().addClass('display-none')
				$("#securitygrouprule_securitygroup").parent().parent().removeClass('display-none')
				$("#securitygrouprule_ethertype").parent().parent().removeClass('display-none')
			}else{
			}
		}else{
			$("#securitygrouprule_rule").parent().parent().siblings().addClass('display-none')
			$("#securitygrouprule_remote").parent().parent().removeClass('display-none')
			if($("#securitygrouprule_remote").val()=='cidr'){
				$("#securitygrouprule_cidr").parent().parent().removeClass('display-none')
				$("#securitygrouprule_securitygroup").parent().parent().addClass('display-none')
				$("#securitygrouprule_ethertype").parent().parent().addClass('display-none')
			}else if($("#securitygrouprule_remote").val()=='securitygroup'){
				$("#securitygrouprule_cidr").parent().parent().addClass('display-none')
				$("#securitygrouprule_securitygroup").parent().parent().removeClass('display-none')
				$("#securitygrouprule_ethertype").parent().parent().removeClass('display-none')
			}else{
			}
		}
	})
	$.ajax({
		url:securitygrouprule_menu_url,
		type:"get",
		data:{},
		async:false,
        success:function (data){
        	if (data=='error'){
            	alert("取得区域信息失败!");
            	return
            }
            var rule_menu= eval("(" + data + ")");
            if(rule_menu.length<1)
            	return
        	$('#securitygrouprule_rule').empty()
            for(var key in rule_menu){
            	var option = $("<option>").val(rule_menu[key][0]).text(rule_menu[key][1]);
            	$('#securitygrouprule_rule').append(option)
            }
        },
        error: function (data, status, e) {
            alert("赠送失败!");
        }
    });
	
	$.ajax({
		url:securitygroup_list_url+'?limit=1000&offset=0',
		type:"get",
		data:{},
		async:false,
        success:function (data){
        	if (data=='error'){
            	alert("取得区域信息失败!");
            	return
            }
            var securitygroup= eval("(" + data + ")");
        	$('#securitygrouprule_securitygroup').empty()
            for(var key in securitygroup['rows']){
            	var option = $("<option>").val(securitygroup['rows'][key]['id']).text(securitygroup['rows'][key]['name']);
            	$('#securitygrouprule_securitygroup').append(option)
            }
        },
        error: function (data, status, e) {
            alert("赠送失败!");
        }
    });
}

function securitygrouprule_create_form(securitygrouprule_menu_url,securitygroup_list_url){
	$("#securitygrouprule_create_form").modal()
	securitygrouprule_create_form_init(securitygrouprule_menu_url,securitygroup_list_url)
}

function securitygrouprule_create_action(parent_group_id,securitygrouprule_create_url){
	
	var securitygrouprule_form= $("#securitygrouprule_create_form").find('form').eq(0)
	if(securitygrouprule_form.data('bootstrapValidator')){
//		$(securitygrouprule_form).data('bootstrapValidator').resetForm()
		$(securitygrouprule_form).data('bootstrapValidator',null);
	}
	securitygrouprule_form.bootstrapValidator('validate')
    if(!securitygrouprule_form.data('bootstrapValidator').isValid())
	    return
	var name=$("#securitygrouprule_name").val();
	var description=$("#securitygrouprule_description").val()
	$("#securitygrouprule_create_form").mask('云硬盘创建中，请稍后......')
	var rule_menu=$("#securitygrouprule_rule").val()
	var direction=$("#securitygrouprule_direction").val()
	var ip_protocol=$("#securitygrouprule_ip_protocol").val()
	var port_type=$("#securitygrouprule_port_type").val()
	var port=$("#securitygrouprule_port").val()
	var from_port=$("#securitygrouprule_from_port").val()
	var to_port=$("#securitygrouprule_to_port").val()
	var remote=$("#securitygrouprule_remote").val()
	var cidr=$("#securitygrouprule_cidr").val()
	var securitygroup=$("#securitygrouprule_securitygroup").val()
	var ethertype=$("#securitygrouprule_ethertype").val()
	$.ajax({
		url:securitygrouprule_create_url,
		type:"post",
		data:{'parent_group_id':parent_group_id,'rule_menu':rule_menu,'direction':direction,'ip_protocol':ip_protocol,'port_type':port_type,'port':port,'from_port':from_port,'to_port':to_port,'remote':remote,'cidr':cidr,'group_id':securitygroup,'ethertype':ethertype},
		async:false,
        success:function (data){
        	$("#securitygrouprule_create_form").unmask()
        	if (data=='success'){
        		$("#securitygrouprule_create_form").modal('toggle');
        		$("#securitygroupruleTable").bootstrapTable('refresh');
        		securitygrouprule_init_btn()
            }else{
            	alert('安全组创建失败')
            }
        },
        error: function (data, status, e) {
        	$("#securitygrouprule_create_form").unmask()
            alert("赠送失败!");
        }
    });
}
