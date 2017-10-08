$(document).ready(function () {
	$("#instanceTable").bootstrapTable(
            {
                'onPageChange' : function(number, size) {
                },
                'queryParams' : function(params) {
                	var opt=$('#search_opt option:selected').val();
                	var value=$("#search_input").val()
                	if(value.length>0){
                		params[opt]=value
                	}
                    return params
                },
                /*'onCheck':check_row,
                'onUncheck':check_row,
                'onCheckAll':check_row,
                'onUncheckAll':check_row,*/
                'onAll':check_row
            });
	$("#next_firststep").click(function(){
		if(!$("#image_id_select").val()){
			alert('请选择镜像！')
			return
		}
		$('.frame-second').show().siblings('form').hide();
		$('.button-second').show().siblings().hide();
		$('.content-progress').find('ul li').eq(1).addClass('active');
		$('.content-progress div').removeClass("step1").addClass("step2");
	});
	$("#back_secondstep").click(function(){
		$('.frame-first').show().siblings('form').hide();
		$('.button-first').show().siblings().hide();
		$('.content-progress div').removeClass("step2").addClass("step1");
		$('.content-progress').find('ul li').eq(1).removeClass('active');
	});
	$("#next_secondstep").click(function(){
		$('.frame-third').show().siblings('form').hide();
		$('.button-third').show().siblings().hide();
		$('.content-progress div').removeClass("step2").addClass("step3");
		$('.content-progress').find('ul li').eq(2).addClass('active');
	});
	$("#back_thirdstep").click(function(){
		$('.frame-second').show().siblings('form').hide();
		$('.button-second').show().siblings().hide();
		$('.content-progress div').removeClass("step3").addClass("step2");
		$('.content-progress').find('ul li').eq(2).removeClass('active');
	});
	$("#next_thirdstep").click(function(){
		$('.frame-last').show().siblings('form').hide();
		$('.button-last').show().siblings().hide();
		$('.content-progress div').removeClass("step3").addClass("step4");
		$('.content-progress').find('ul li').eq(3).addClass('active');
	});
	$("#back_laststep").click(function(){
		$('.frame-third').show().siblings('form').hide();
		$('.button-third').show().siblings().hide();
		$('.content-progress div').removeClass("step4").addClass("step3");
		$('.content-progress').find('ul li').eq(3).removeClass('active');
	});
	update_instance_status();
})

function refresh() {
	$("#instanceTable").bootstrapTable('refresh',{'url':'/project/instance/list?reload=true'});
	$("#instanceTable").bootstrapTable('refresh',{'url':'/project/instance/list'});
}

function check_row(row){
	$("#instance_meun").find('li').removeClass('disabled');
	if($("#instanceTable").bootstrapTable('getSelections').length==1){
		$("#btn_instance_delete").removeClass('btn-6')
		$("#btn_instance_delete").addClass('btn-5')
		row=$("#instanceTable").bootstrapTable('getSelections')[0]
		if(row.status!='ACTIVE'&& row.status!='SHUTOFF'){
			$("#instance_start").addClass('disabled');
			$("#instance_reboot").addClass('disabled');
			$("#instance_shutdown").addClass('disabled');
		}else if(row.status=='ACTIVE'){
			$("#instance_shutdown").removeClass('disabled');
			$("#instance_reboot").removeClass('disabled');
			$("#instance_start").addClass('disabled');
		}else{
			$("#instance_start").removeClass('disabled');
			$("#instance_shutdown").addClass('disabled');
			$("#instance_reboot").addClass('disabled');
		}
		if(row.network&&row.network.contain('外网')){
			$("#instance_binging_floatingip").addClass('disabled');
			$("#instance_unbinding_floatingip").removeClass('disabled');
		}else{
			$("#instance_binging_floatingip").removeClass('disabled');
			$("#instance_unbinding_floatingip").addClass('disabled');
		}
	}else if($("#instanceTable").bootstrapTable('getSelections').length > 1){
		$("#instance_meun").find('li').addClass('disabled');
		$("#instance_delete").removeClass('disabled');
		$("#btn_instance_delete").removeClass('btn-6')
		$("#btn_instance_delete").addClass('btn-5')
	}else{
		$("#instance_meun").find('li').addClass('disabled');
		$("#btn_instance_delete").removeClass('btn-5');
		$("#btn_instance_delete").addClass('btn-6');
	}
}
function init_btn(){
	$("#instance_meun").find('li').addClass('disabled');
	$("#btn_instance_delete").removeClass('btn-5');
	$("#btn_instance_delete").addClass('btn-6');
}

function search() {
	$("#instanceTable").bootstrapTable('selectPage', 1)
}
function operateFormatter(value, row, index) {
	    return [
			//'<a class="detail" data-toggle="modal" data-target="#Modal_delete" href="javascript:void(0)">删除</a>  '
			'<button class="btn-delete" data-toggle="modal" data-target="#Modal_delete" >删除</button>  '
	    ].join('');
	}

function instance_start(url){
	rows=$("#instanceTable").bootstrapTable('getSelections')
	if(rows.length!=1){
		return
	}
	row=rows[0]
	if(row.status!='SHUTOFF'){
		return
	}
	$("#instance_body").mask('云主机开机中，请稍后......')
	$.ajax({
		url:url+'?instance_id='+row.id,
		type:"get",
		async:false,
        success:function (data){
        	$("#instance_body").unmask()
            if (data=='success'){
        		refresh()
        		init_btn()
            }
            else{
                $('#instance_edit_form').modal('toggle');
                alert("请输入0~{{ gift_value }}之间的数值");
            }

        },
        error: function (data, status, e) {
            alert("赠送失败!");
        }
    });
	
}
function instance_stop(url){
	rows=$("#instanceTable").bootstrapTable('getSelections')
	if(rows.length!=1){
		return
	}
	row=rows[0]
	if(row.status!='ACTIVE'){
		return
	}
	$("#instance_body").mask('云主机关机中，请稍后......')
	$.ajax({
		url:url+'?instance_id='+row.id,
		type:"get",
		async:false,
        success:function (data){
        	$("#instance_body").unmask()
            if (data=='success'){
        		refresh()
        		init_btn()
            }
            else{
                $('#instance_edit_form').modal('toggle');
                alert("请输入0~{{ gift_value }}之间的数值");
            }

        },
        error: function (data, status, e) {
            alert("赠送失败!");
        }
    });
	
}

function instance_reboot(url){
	rows=$("#instanceTable").bootstrapTable('getSelections')
	if(rows.length!=1){
		return
	}
	row=rows[0]
	if(row.status!='ACTIVE'){
		return
	}
	$("#instance_body").mask('云主机重启中，请稍后......')
	$.ajax({
		url:url+'?instance_id='+row.id,
		type:"get",
		async:false,
        success:function (data){
        	$("#instance_body").unmask()
            if (data=='success'){
        		refresh()
        		init_btn()
            }
            else{
                $('#instance_edit_form').modal('toggle');
                alert("请输入0~{{ gift_value }}之间的数值");
            }

        },
        error: function (data, status, e) {
            alert("赠送失败!");
        }
    });
	
}

function floating_ip_form(region_list_url,floatingip_billing_url,instance_ports_url,floatingip_noassociate_list_url,floatingip_pool_list_url){
	rows=$("#instanceTable").bootstrapTable('getSelections')
	if(rows.length!=1){
		return
	}
	var floating_ip_form= $("#floating_ip_form").find('form').eq(0)
	if(floating_ip_form.data('bootstrapValidator')){
		$(floating_ip_form).data('bootstrapValidator').resetForm()
	}
	floating_ip_form[0].reset();
	$("input[name=isDistribution]").click(function(){
		switch($("input[name=isDistribution]:checked").val()){
		  case "yes":
		   $("#associate_ip").parent().parent().addClass('display-none')
		   $("#floatingip_pool").parent().removeClass('display-none')
		   break;
		  case "no":
		   $("#associate_ip").parent().parent().removeClass('display-none')
		   $("#floatingip_pool").parent().addClass('display-none')
		   break;
		  default:
		   break;
		 }
	});
	$("#associate_ip").parent().parent().removeClass('display-none')
	$("#floatingip_pool").parent().addClass('display-none')
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
            $("#region_description").empty();
            $("#region_description").append(regions[0]['description'])
            $("#region_id").val(regions[0]['id'])
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
	getTotalPrice_floatingip(billing_data,'#floatingip_price_hour','#floatingip_price_year')
	$.ajax({
		url:instance_ports_url+'?instance_id='+rows[0].id,
		type:"get",
		data:{},
		async:false,
        success:function (data){
        	if (data=='error'){
            	alert("取得云主机端口失败!");
            	return
            }
        	ports=eval("(" + data + ")");
        	$("#associate_port").empty()
        	for(var i in ports){
        		$("#associate_port").append('<option value="'+ports[i]['id']+'_'+ports[i]['ip']+'">'+ports[i]['ip']+'</option>')
        	}
        },
        error: function (data, status, e) {
            alert("赠送失败!");
        }
    });
	$.ajax({
		url:floatingip_noassociate_list_url,
		type:"get",
		data:{},
		async:true,
        success:function (data){
        	if (data=='error'){
            	alert("取得云主机端口失败!");
            	return
            }
        	floatingips=eval("(" + data + ")");
        	$("#associate_ip").empty()
        	for(var i in floatingips){
        		$("#associate_ip").append('<option value="'+floatingips[i]['id']+'">'+floatingips[i]['pool_name']+'_'+floatingips[i]['floating_ip_address']+'</option>')
        	}
        },
        error: function (data, status, e) {
            alert("赠送失败!");
        }
    });
	$.ajax({
		url:floatingip_pool_list_url,
		type:"get",
		data:{},
		async:true,
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
	$("#floating_ip_form").modal()
}
function getTotalPrice_floatingip(billing_data,price_hour,price_year){
	total=billing_data['ip_1']['price']*billing_data['ip_1']['discount_ratio']
	$(price_hour).empty()
	$(price_hour).append(money_formatter(total))
	$(price_year).empty()
	$(price_year).append(money_formatter(total*24*30))
}

function floating_ip_action(instance_associate_url){
	var floating_ip_form= $("#floating_ip_form").find('form').eq(0)
	if(floating_ip_form.data('bootstrapValidator')){
		$(floating_ip_form).data('bootstrapValidator',null);
	}
	floating_ip_form.bootstrapValidator('validate')
    if(!floating_ip_form.data('bootstrapValidator').isValid())
	    return
	rows=$("#instanceTable").bootstrapTable('getSelections')
	if(rows.length!=1){
		return
	}
	
	var isDistribution=$("input[name='isDistribution']:checked").val()
	var port_id_ip=$("#associate_port").val()
	var data={'instance_id':rows[0].id,'port_id_ip':port_id_ip}
	if(isDistribution=='yes'){
		data['pool_id']=$("input[name='floatingip_pool']:checked").val()
	}else{
		if(!$("#associate_ip").val()){
			alert('没有可用的浮动IP！')
			return
		}
		data['floatingip_id']=$("#associate_ip").val()
	}
	$("#floating_ip_form").mask('关联浮动IP中，请稍后......')
	$.ajax({
		url:instance_associate_url,
		type:"post",
		data:data,
		async:false,
        success:function (data){
        	$("#floating_ip_form").unmask()
            if (data=='success'){
            	$("#floating_ip_form").modal('toggle');
            	refresh()
            }
            else{
            	alert('关联浮动IP失败！')
//                $('#floating_ip_form').modal('toggle');
            }
        },
        error: function (data, status, e) {
        	$("#floating_ip_form").unmask()
            alert("赠送失败!");
        }
    });
}

function securitygroup_edit_form(securitygroup_nopage_list_url,instance_securitygroup_url){
	rows=$("#instanceTable").bootstrapTable('getSelections')
	if(rows.length!=1){
		return
	}
	$.ajax({
		url:securitygroup_nopage_list_url,
		type:"get",
		data:{},
		async:false,
        success:function (data){
        	if (data=='error'){
            	alert("取得区域信息失败!");
            	return
            }
            var sgs= eval("(" + data + ")");
            if(sgs.length<1)
            	return
            $("#selectsecuritygroup").empty();
            for(var i in sgs){
            	$("#selectsecuritygroup").append('<li id="'+sgs[i]['id']+'">'+sgs[i]['name']+'</li>')
            }
        },
        error: function (data, status, e) {
            alert("赠送失败!");
        }
    });
	$("#selectsecuritygroup li").click(function(){
		$(this).toggleClass("active");
	});
	$.ajax({
		url:instance_securitygroup_url+"?instance_id="+rows[0].id,
		type:"get",
		data:{},
		async:false,
        success:function (data){
        	if (data=='error'){
            	alert("取得区域信息失败!");
            	return
            }
            var sgs= eval("(" + data + ")");
            if(sgs.length<1)
            	return
            $("#selectsecuritygroup li").each(function(e){
            	for(var i in sgs){
            		if($(this).attr('id')==sgs[i]['id']){
            			$(this).click();
            		}
            	}
            })
        },
        error: function (data, status, e) {
            alert("赠送失败!");
        }
    });
	$("#securitygroup_edit_form").modal()
}

function securitygroup_edit_action(instance_securitygroup_update_url){
	rows=$("#instanceTable").bootstrapTable('getSelections')
	$("#securitygroup_edit_form").mask('修改安全组中，请稍后......')
	sg_ids=''
	$("#selectsecuritygroup li").each(function(e){
		if($(this).hasClass('active')){
			if(sg_ids){
				sg_ids=sg_ids+','
			}
			sg_ids=sg_ids+$(this).attr('id')
		}
	})
	$.ajax({
		url:instance_securitygroup_update_url,
		type:"post",
		data:{'instance_id':rows[0].id,'sg_ids':sg_ids},
		async:false,
        success:function (data){
        	$("#securitygroup_edit_form").unmask()
            if (data=='success'){
            	alert('修改安全组成功！')
            	$("#securitygroup_edit_form").modal('toggle');
            }
            else{
            	alert('修改安全组失败！')
//                $('#securitygroup_edit_form').modal('toggle');
            }

        },
        error: function (data, status, e) {
        	$("#securitygroup_edit_form").unmask()
            alert("赠送失败!");
        }
    });
	
}



function edit_form(url){
	rows=$("#instanceTable").bootstrapTable('getSelections')
	if(!url){
		if(rows.length==0){
			return
		}
		row=rows[0]
		
		$("#instance_edit_form").modal({backdrop : 'static'})
		$("#instance_name_edit").val(row.name)
	}else{
		var instance_edit_form= $("#instance_edit_form").find('form').eq(0)
		if(instance_edit_form.data('bootstrapValidator')){
			$(instance_edit_form).data('bootstrapValidator',null);
		}
		instance_edit_form.bootstrapValidator('validate')
	    if(!instance_edit_form.data('bootstrapValidator').isValid())
		    return
		row=rows[0]
		$("#instance_edit_modal_dialog").mask('数据保存中，请稍后......')
		$.ajax({
			url:url,
			type:"post",
			data:{'instance_id':row.id,'name':$("#instance_name_edit").val()},
//			data:{recharge:JSON.stringify(request_data)}, 
			async:false,
            success:function (data){
            	$("#instance_edit_modal_dialog").unmask()
                if (data=='success'){
                	$("#instance_edit_form").modal('toggle');
            		refresh()
            		init_btn()
                }
                else{
                    $('#instance_edit_form').modal('toggle');
                    alert("请输入0~{{ gift_value }}之间的数值");
                }

            },
            error: function (data, status, e) {
                $('#instance_edit_form').modal('toggle');
                alert("赠送失败!");
            }
        });
	}
}
function detail_form(){
	rows=$("#instanceTable").bootstrapTable('getSelections')
	if(rows.length==0){
		return
	}
	$("#instance_detail_form").modal()
}

function instance_delete(url){
	rows=$("#instanceTable").bootstrapTable('getSelections')
	if(rows.length<1){
		return
	}
	instance_ids=''
	for ( var key in rows) {
		if(instance_ids){
			instance_ids=instance_ids+','+rows[key].id
		}else{
			instance_ids=rows[key].id
		}
	}
	$("#instance_body").mask('云主机删除中，请稍后......')
	$.ajax({
		url:url,
		type:"post",
		data:{'instance_ids':instance_ids},
		async:false,
        success:function (data){
        	$("#instance_body").unmask()
            if (data=='success'){
        		refresh()
        		init_btn()
            }
            else{
                $('#instance_edit_form').modal('toggle');
                alert("请输入0~{{ gift_value }}之间的数值");
            }

        },
        error: function (data, status, e) {
            alert("赠送失败!");
            $("#instance_body").unmask()
        }
    });
}

function init_instance_create_form(instance_billing_url,region_list_url){
	$('.frame-first').show().siblings('form').hide();
	$('.button-first').show().siblings().hide();
	$('.content-progress div').removeClass("step2 step3 step4").addClass("step1");
	$('.content-progress').find('ul li').eq(1).removeClass('active');
	$(".list-group").empty()
	$("#image_name_select").empty()
	$("#image_id_select").val('')
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
            $("#region_description").empty();
            $("#region_description").append(regions[0]['description'])
            $("#region_id").val(regions[0]['id'])
            region_id=regions[0]['id']
        },
        error: function (data, status, e) {
            alert("赠送失败!");
        }
    });
	var billing_data=null
	$.ajax({
		url:instance_billing_url+'?region_id='+region_id,
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
	$(".cpu-type").find("li").click(function(){
		$(".cpu-type").find("li").removeClass('active')
		$("#vcpus_select").empty()
		$("#vcpus_select").append($(this).find('span').html())
		$(this).addClass("active")
		getTotalPrice(billing_data)
	})
	$(".cpu-type").find("li").eq(0).click()
	$(".mic-type").find("li").click(function(){
		$(".mic-type").find("li").removeClass('active')
		$("#memory_select").empty()
		$("#memory_select").append($(this).find('span').html())
		$(this).addClass("active")
		getTotalPrice(billing_data)
	})
	$(".mic-type").find("li").eq(0).click()
	$(".disk-type").find("li").click(function(){
		$(".disk-type").find("li").removeClass('active')
		$("#disk_select").empty()
		$("#disk_select").append($(this).find('span').html())
		$(this).addClass("active")
	})
	$(".disk-type").find("li").eq(1).click()
	$(".ephemeral-disk-type").find("li").click(function(){
		$(".ephemeral-disk-type").find("li").removeClass('active')
		$("#ephemeral_disk_select").empty()
		$("#ephemeral_disk_select").append($(this).find('span').html())
		$(this).addClass("active")
	})
	$(".ephemeral-disk-type").find("li").eq(0).click()
	$(".swap-disk-type").find("li").click(function(){
		$(".swap-disk-type").find("li").removeClass('active')
		$("#swap_disk_select").empty()
		$("#swap_disk_select").append($(this).find('span').html())
		$(this).addClass("active")
	})
	$(".swap-disk-type").find("li").eq(0).click()
	$('#network_list_select').empty()
	var instance_detail_form= $("#instance_create_detail")
	if(instance_detail_form.data('bootstrapValidator')){
		$(instance_detail_form).data('bootstrapValidator').resetForm()
	}
	instance_detail_form[0].reset();
	
}
function getTotalPrice(billing_data){
	total=$("#vcpus_select").html()*billing_data['cpu_1_core']['price']*billing_data['cpu_1_core']['discount_ratio']+$("#memory_select").html()*billing_data['memory_1024_M']['price']*billing_data['memory_1024_M']['discount_ratio']
	$("#price_hour").empty()
	$("#price_hour").append(money_formatter(total))
	$("#price_year").empty()
	$("#price_year").append(money_formatter(total*24*30))
}
function instance_create_form(image_list_url,region_list_url,instance_billing_url,subnetwork_list_url){
	$('#firststep').modal();
	init_instance_create_form(instance_billing_url,region_list_url)
	var image_data=null;
	$("input[for='number']").numeral(1)
	$.ajax({
		url:image_list_url,
		type:"get",
		data:{},
		async:false,
        success:function (data){
            if (data=='error'){
            	alert("取得镜像失败!");
            	return
            }
            image_data= eval("(" + data + ")");

        },
        error: function (data, status, e) {
            alert("取得镜像失败!");
        }
    });
	$("#operate-os").find("li").click(function () {
		$(this).addClass("active").siblings().removeClass("active");
		var os_type=$(this).find("div span").attr('title')
		$(".list-group").empty()
		if(image_data!=null){
			for(var key in image_data[os_type]){
				$(".list-group").append('<a href="#" class="list-group-item"><input type="hidden" value="'+image_data[os_type][key]['id']+'"><span>'+image_data[os_type][key]['name']+'</span><span class="fr">'+image_data[os_type][key]['size']+'M</span></a>')
			}
		}
		$(".list-group").find("a").click(function(){
			$("#image_name_select").empty()
			$("#image_name_select").append($(this).find('span').eq(0).html())
			$("#image_id_select").val($(this).find('input').val())
		})
	});
	$("#operate-os").find("li").eq(0).click()
	
	$.ajax({
		url:subnetwork_list_url,
		type:"get",
		data:{},
		async:false,
        success:function (data){
        	if (data=='error'){
            	alert("取得区域信息失败!");
            	return
            }
            var nets= eval("(" + data + ")");
            if(nets.length<1)
            	return
            $('#network_list_select').empty()
            for(var key in nets){
            	var option = $("<option>").val(nets[key]['id']).text(nets[key]['name']);
            	$('#network_list_select').append(option)
            }
        },
        error: function (data, status, e) {
            alert("赠送失败!");
        }
    });
}

function instance_create_action(instance_create_url){
	var instance_create_detail_form= $("#instance_create_detail")
	if(instance_create_detail_form.data('bootstrapValidator')){
		$(instance_create_detail_form).data('bootstrapValidator',null);
	}
	instance_create_detail_form.bootstrapValidator('validate')
    if(!instance_create_detail_form.data('bootstrapValidator').isValid())
	    return
	var image_id=$("#image_id_select").val()
	var vcpus=$("#vcpus_select").html()
	var memory=$("#memory_select").html()
	var disk=$("#disk_select").html()
	var ephemeral = $("#ephemeral_disk_select").html()
	var swap = $("#swap_disk_select").html()
	var netid=$("#network_list_select").val()
	var name=$("#instance_name_input").val()
	var root_pass=$("#instance_root_pass").val()
	var instance_count=$("#instance_count_input").val()
	$("#instance_create_form").mask('云主机删除中，请稍后......')
	$.ajax({
		url:instance_create_url,
		type:"post",
		data:{'image_id':image_id,'vcpus':vcpus,'memory':memory,'disk':disk,'ephemeral':ephemeral,'swap':swap,'netid':netid,'name':name,'root_pass':root_pass,'instance_count':instance_count},
		async:false,
        success:function (data){
        	$("#instance_create_form").unmask()
            if (data=='success'){
            	$("#firststep").modal('toggle');
        		refresh()
            }
            else{
                $('#firststep').modal('toggle');
                alert("请输入0~{{ gift_value }}之间的数值");
            }

        },
        error: function (data, status, e) {
        	$("#instance_create_form").unmask()
            alert("赠送失败!");
        }
    });
}


function instance_flavor_create_action(instance_flavor_create_url) {
	var vcpus=$("#vcpus_select").html()
	var memory=$("#memory_select").html()
	var disk=$("#disk_select").html()
	var ephemeral = $("#ephemeral_disk_select").html()
	var swap = $("#swap_disk_select").html()
	$.ajax({
		url:instance_flavor_create_url,
		type:"post",
		data:{'vcpus':vcpus,'memory':memory,'disk':disk,'ephemeral':ephemeral,'swap':swap},
		async:true,
        success:function (data){
        },
        error: function (data, status, e) {
        }
    });
}

function instance_console(url){
	rows=$("#instanceTable").bootstrapTable('getSelections')
	if(rows.length!=1){
		return
	}
	row=rows[0]
	if(row.status!='ACTIVE'){
		return
	}
	$.ajax({
		url:url+'?instance_id='+row.id+'&instance_name='+row.name,
		type:"post",
		async:false,
		data:{'instance_id':row.id,'instance_name':row.name},
        success:function (data){
        	if (data=='error'){
            	alert("连接控制台失败!");
            	return
            }
        	console_data=eval("(" + data + ")");
//        	window.location.href=console_data['console_url']
        	window.open(console_data['console_url'])
        },
        error: function (data, status, e) {
            alert("赠送失败!");
        }
    });
	
}

function instance_resize_form(region_list_url,instance_billing_url){
	rows=$("#instanceTable").bootstrapTable('getSelections')
	if(rows.length!=1){
		return
	}
	row=rows[0]
	if(row.status !='ACTIVE' && row.status !='SHUTOFF'){
		return
	}
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
            /*$("#region_description").empty();
            $("#region_description").append(regions[0]['description'])
            $("#region_id").val(regions[0]['id'])*/
            region_id=regions[0]['id']
        },
        error: function (data, status, e) {
            alert("赠送失败!");
        }
    });
	var billing_data=null
	$.ajax({
		url:instance_billing_url+'?region_id='+region_id,
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
	$(".cpu-type").find("li").click(function(){
		$(".cpu-type").find("li").removeClass('active')
		$("#instance_resize_cpus").empty()
		$("#instance_resize_cpus").append($(this).find('span').html())
		$("#instance_resize_cpu_num").val($(this).find('span').html())
		$(this).addClass("active")
		getResizeTotalPrice(billing_data)
	})
	
	$(".mic-type").find("li").click(function(){
		$(".mic-type").find("li").removeClass('active')
		$("#instance_resize_memory").empty()
		$("#instance_resize_memory").append($(this).find('span').html())
		$("#instance_resize_memory_num").val($(this).find('span').html())
		$(this).addClass("active")
		getResizeTotalPrice(billing_data)
	})
	$(".disk-type").find("li").click(function(){
		if(row.root_gb>$(this).find('span').html()){
			return
		}
		$(".disk-type").find("li").removeClass('active')
		$("#instance_resize_disk").empty()
		$("#instance_resize_disk").append($(this).find('span').html())
		$("#instance_resize_disk_num").val($(this).find('span').html())
		$(this).addClass("active")
	})
	$("#instance_resize_cpu_num").on('input',function(e){
		$(".cpu-type").find("li").removeClass('active')
		$(".cpu-type").find("li").each(function(){
			if($("#instance_resize_cpu_num").val()==$(this).find('span').html()){
				$(this).click()
			}
		})
		$("#instance_resize_cpus").empty()
		$("#instance_resize_cpus").append($("#instance_resize_cpu_num").val())
		getResizeTotalPrice(billing_data)
	});
	$("#instance_resize_memory_num").on('input',function(e){
		$(".mic-type").find("li").removeClass('active')
		$(".mic-type").find("li").each(function(){
			if($("#instance_resize_memory_num").val()==$(this).find('span').html()){
				$(this).click()
			}
		})
		$("#instance_resize_memory").empty()
		$("#instance_resize_memory").append($("#instance_resize_memory_num").val())
		getResizeTotalPrice(billing_data)
	});
	$("#instance_resize_disk_num").on('input',function(e){
		$(".disk-type").find("li").removeClass('active')
		$(".disk-type").find("li").each(function(){
			if($("#instance_resize_disk_num").val()==$(this).find('span').html()){
				$(this).click()
			}
		})
		$("#instance_resize_disk").empty()
		$("#instance_resize_disk").append($("#instance_resize_disk_num").val())
	});
	$("#instance_resize_cpu_num").val(row.vcpus)
	$("#instance_resize_cpus").empty()
	$("#instance_resize_cpus").append(row.vcpus)
	$(".cpu-type").find("li").removeClass('active')
	
	$("#instance_resize_memory_num").val(row.memory_mb/1024)
	$("#instance_resize_memory").empty()
	$("#instance_resize_memory").append(row.memory_mb/1024)
	$(".mic-type").find("li").removeClass('active')
	
	$("#instance_resize_disk_num").val(row.root_gb)
	$("#instance_resize_disk").empty()
	$("#instance_resize_disk").append(row.root_gb)
	$(".disk-type").find("li").removeClass('active')
	
	getResizeTotalPrice(billing_data)
	
	$(".cpu-type").find("li").each(function(){
		if(row.vcpus==$(this).find('span').html()){
			$(this).click()
		}
	})
	$(".mic-type").find("li").each(function(){
		if((row.memory_mb/1024)==$(this).find('span').html()){
			$(this).click()
		}
	})
	$(".disk-type").find("li").each(function(){
		if(row.root_gb==$(this).find('span').html()){
			$(this).click()
		}
	})
	$("#instance_resize_disk_num_label").empty()
	$("#instance_resize_disk_num_label").append("最小值"+row.root_gb+"G")
	$("#instance_resize_disk_num").attr('data-bv-between-min',row.root_gb).attr('data-bv-between-message','硬盘在'+row.root_gb+'G到256G')
	
	$("input[for='number1']").numeral(3)
	var instance_resize_form= $("#instance_resize_form").find('form').eq(0)
	if(instance_resize_form.data('bootstrapValidator')){
		$(instance_resize_form).data('bootstrapValidator').resetForm()
	}
	
	$("#instance_resize_form").modal()
}
function getResizeTotalPrice(billing_data){
	total=$("#instance_resize_cpus").html()*billing_data['cpu_1_core']['price']*billing_data['cpu_1_core']['discount_ratio']+$("#instance_resize_memory").html()*billing_data['memory_1024_M']['price']*billing_data['memory_1024_M']['discount_ratio']
	$("#resize_price_hour").empty()
	$("#resize_price_hour").append(money_formatter(total))
	$("#resize_price_year").empty()
	$("#resize_price_year").append(money_formatter(total*24*30))
}

function instance_resize_action(instance_resize_url){
	var instance_resize_form= $("#instance_resize_form").find('form').eq(0)
	if(instance_resize_form.data('bootstrapValidator')){
		$(instance_resize_form).data('bootstrapValidator',null);
	}
	instance_resize_form.bootstrapValidator('validate')
    if(!instance_resize_form.data('bootstrapValidator').isValid())
	    return
	rows=$("#instanceTable").bootstrapTable('getSelections')
	row=rows[0]
	$("#instance_resize_form").mask('云主机删除中，请稍后......')
	$.ajax({
		url:instance_resize_url,
		type:"post",
		data:{'instance_id':row.id,'vcpus':$("#instance_resize_cpus").html(),'memory_mb':$("#instance_resize_memory").html(),'root_gb':$("#instance_resize_disk").html()},
		async:false,
        success:function (data){
        	$("#instance_resize_form").unmask()
            if (data=='success'){
            	$("#instance_resize_form").modal('toggle');
        		refresh()
            }
            else{
                $('#instance_resize_form').modal('toggle');
                alert("请输入0~{{ gift_value }}之间的数值");
            }

        },
        error: function (data, status, e) {
        	$("#instance_resize_form").unmask()
            alert("赠送失败!");
        }
    });
}


function instance_disassociate(instance_disassociate_url){
	rows=$("#instanceTable").bootstrapTable('getSelections')
	if(rows.length!=1){
		return
	}
	row=rows[0]
	$("#instance_body").mask('解绑浮动IP中，请稍后......')
	$.ajax({
		url:instance_disassociate_url+'?instance_id='+row.id,
		type:"get",
		data:{},
		async:false,
        success:function (data){
        	$("#instance_body").unmask()
            if (data=='success'){
        		refresh()
            }
            else{
            	alert('解绑浮动IP失败！')
            }
        },
        error: function (data, status, e) {
        	$("#instance_body").unmask()
            alert("赠送失败!");
        }
    });
}

function snapshot_form(){
	rows=$("#instanceTable").bootstrapTable('getSelections')
	if(rows.length!=1){
		return
	}
	var snapshot_form= $("#snapshot_form").find('form').eq(0)
	if(snapshot_form.data('bootstrapValidator')){
		$(snapshot_form).data('bootstrapValidator').resetForm()
	}
	snapshot_form[0].reset();
	$("#snapshot_form").modal()
}

function snapshot_action(instance_snapshot_create_url){
	rows=$("#instanceTable").bootstrapTable('getSelections')
	if(rows.length!=1){
		return
	}
	var snapshot_form= $("#snapshot_form").find('form').eq(0)
	if(snapshot_form.data('bootstrapValidator')){
		$(snapshot_form).data('bootstrapValidator',null);
	}
	snapshot_form.bootstrapValidator('validate')
    if(!snapshot_form.data('bootstrapValidator').isValid())
	    return
	$("#snapshot_form").mask('解绑浮动IP中，请稍后......')
    $.ajax({
		url:instance_snapshot_create_url,
		type:"post",
		data:{'instance_id':rows[0].id,'snapshot_name':$("#snapshot_name").val()},
		async:false,
        success:function (data){
        	$("#snapshot_form").unmask()
            if (data=='success'){
            	alert('创建快照成功！')
            	$('#snapshot_form').modal('toggle');
            }
            else{
            	alert('解绑浮动IP失败！')
            }
        },
        error: function (data, status, e) {
        	$("#snapshot_form").unmask()
            alert("赠送失败!");
        }
    });
}

function get_instance_status(){
	$("#instanceTable tbody tr").each(function(){
		var status_td = $(this).find("td:eq(6)");
		var status_value = status_td.html();
		if("BUILD"==status_value){
			var $key = $(this).find("td:eq(0)").find("input").attr("data-index");
			var $obj = $("#instanceTable").bootstrapTable('getData');
			var $instance_id = $obj[$key].id; 
			//alert("id:"+$instance_id+"   name:"+$name+"  ip:"+$ip+"   status:"+$status);
			$.ajax({
				url:"/project/instance/instance_get",
				type:"get",
				data:{'instance_id':$instance_id},
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
	setInterval("get_instance_status()",5000);
}