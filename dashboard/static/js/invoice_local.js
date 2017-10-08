/**
 * Created by arsene on 15-10-15.
 */
function saveNewInvoiceBody(event) {
    if (event.which==1){
        var td1 = $("#invoice_title").val();
        var td2 = $("#invoice_amount").val();
        var td3 = $("#invoice_content").val();
        var invoice_type = $('input[name="invoicetype"]:checked').val();
        var alertmsg = "";
        var alert_flag = 0;
        htmlobj_i_summary= $.ajax({url:constant_root_url+'/center/invoice_querySummary', async:false});
        var sum=eval('('+htmlobj_i_summary.responseText+')');

        if (td1==""){
            alertmsg+="发票抬头不能为空<br>";
            alert_flag=1;
        }
        if (td2==""){
            alertmsg+="发票金额不能为空<br>";
            alert_flag=1;
        }
        if (parseFloat(td2)==0){
            alertmsg+='发票金额不能为0';
            alert_flag=1;
        }
        if (parseFloat(td2)>(parseFloat(sum['invoice_amount_avail']))){
            alertmsg+="发票金额不能高于剩余可开发票金额<br>";
            alert_flag=1;
        }
        if (td3==""){
            alertmsg+="发票内容不能为空<br>";
            alert_flag=1;
        }
        if(invoice_type=='normal'){
            $('#invoice_type_choosen').html('增值税普通发票')
        }
        if(invoice_type=='special'){
            $('#invoice_type_choosen').html('增值税专用发票')
        }
        if (alert_flag==1){
            $.alert({
                title: false,
                content: alertmsg,
                confirmButton:'好的',
                confirmButtonClass: 'middle_btn',
            });
        }
        else{
            var invoicestrToInsert = "<tr>"+"<td>"+td1+"</td>"+"<td>"+'￥'+td2+"</td>"+"<td>"+td3+"</td>"+"</tr>";
            $("#invoice_input_form1").hide();
            $("#invoice_pop_tbody").html(invoicestrToInsert);
            $("#invoice_apply_detail").show();
        }
    }
}

function backToInvoiceInput(event){
    if (event.which==1){
        $("#invoice_apply_detail").hide();
        $("#invoice_input_form1").show();
    }
}

function delete_address(mmm){
    htmlobj_i4 = $.post(constant_root_url+'/center/invoice_getAccountAddr',
        {
            'account_id': mmm,
            'delete':'true',
        });
    htmlobj_i5 = $.ajax({url:constant_root_url+'/center/invoice_getAccountAddr', async:false});
    $("#invoice_address_list").html(htmlobj_i5.responseText).show();
}

function fillFormWithCurrentAddr(address_id2){
    $.get(constant_root_url+'/center/invoice_queryAddrDetail', {"address_id": address_id2}, function(result){
        var obj = jQuery.parseJSON(result);
        $("#receiver_name").attr("value", obj.name);
        var phone_tem = obj.phone.split('-');
        var phone_dis = phone_tem[0];
        var phone_body = phone_tem[1];
        var phone_tail = phone_tem[2];
        var select_prov = document.getElementById("seachprov");
        var select_city = document.getElementById("seachcity");
        var select_dis = document.getElementById("seachdistrict");
        var address_tem = obj.address.split('|');
        $("#mobile").attr("value", obj.mobile);
        $("#district_num").attr("value", phone_dis);
        $("#work_num").attr("value", phone_body);
        $("#forward").attr("value", phone_tail);
        $("#zip").attr("value", obj.post_code);
        if (address_tem.length == 4){
            var pro = address_tem[0];
            var cit = address_tem[1];
            var dis = address_tem[2];
            var stre = address_tem[3];
            for(var i=0; i<select_prov.options.length; i++){
                if(select_prov.options[i].innerHTML == pro){
                    select_prov.options[i].selected = true;
                    changeComplexProvince($('#seachprov').val(), sub_array, 'seachcity', 'seachdistrict');
                    break;
                }
            }
            for(var k=0; k<select_city.options.length; k++){
                if(select_city.options[k].innerHTML == cit){
                    select_city.options[k].selected = true;
                    changeCity($('#seachcity').val(),'seachdistrict','seachdistrict');
                    break;
                }
            }
            for(var i=0; i<select_dis.options.length; i++){
                if(select_dis.options[i].innerHTML == dis){
                    select_dis.options[i].selected = true;
                    break;
                }
            };
            $("#street").val(stre);
        }else
        {
            var pro = address_tem[0];
            var cit = address_tem[1];
            var stre = address_tem[2];
            $("#street").val(stre);
            for(var i=0; i<select_prov.options.length; i++){
                if(select_prov.options[i].innerHTML == pro){
                    select_prov.options[i].selected = true;
                    changeComplexProvince($('#seachprov').val(), sub_array, 'seachcity', 'seachdistrict');
                    break;
                }
            }
            for(var i=0; i<select_city.options.length; i++){
                if(select_city.options[i].innerHTML == cit){
                    select_city.options[i].selected = true;
                    changeCity($('#seachcity').val(),'seachdistrict','seachdistrict');
                    break;
                }
            }
        }
    })
}


//function check_money(thisele, moneyvalue){
//      //var reg1 = /^[1-9]{1}[0-9]{0,100}[.]{0,1}[0-9]{0,2}$/;
//      //var reg2 = /^0[.]{1}[0-9]{1,2}$/;
//      if (!reg1.test(moneyvalue) && !reg2.test(moneyvalue) || moneyvalue==0.00){
//          $(thisele).parent().parent().next().show();
//      }else{
//          $(thisele).parent().parent().next().hide();
//      }
//}

function check_mobile(thisele, mobilevalue){
      var reg1 = /^[1-9]{1}[0-9]{0,20}$/;
      if (!reg1.test(mobilevalue)){
          $(thisele).parent().parent().next().show();
      }else{
          $(thisele).parent().parent().next().hide();
      }
}

function check_null(thisele, value1){
    if (value1==""){
        $(thisele).parent().parent().next().show();
    }else{
        $(thisele).parent().parent().next().hide();
    }
}

function check_num(thisele, value13){
    if (isNaN(value13)){
        $(thisele).parent().parent().next().show();
    }else{
        $(thisele).parent().parent().next().hide();
    }
}

function check_num1(){
    if(isNaN($("#district_num").val()) || isNaN($("#work_num").val()) || isNaN($("#forward").val())){
        $("#phone_num_hit").show();
    }else{
        $("#phone_num_hit").hide();
    }
}