/**
 * Created by yamin on 15-10-13.
 */
//<!--将form中的值转换为键值对。-->
function getFormJson(frm) {
    var o = {};
    var a = $(frm).serializeArray();
    $.each(a, function () {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });

    return o;
}

//<!--将form转为AJAX提交。-->　　　　　　　　
//<!--fn为返回后的回调函数，可以为空-->
function ajaxSubmit(frm, fn) {
    var dataPara = getFormJson(frm);
    var ajax_para={};
    ajax_para['data']=dataPara;
    if (!frm.attr('action') ){
        ajax_para['url']=this.location.pathname;
    }
    else{
        ajax_para['url']=frm.attr('action');
    }
    ajax_para['type']=frm.attr('method');
    if (!frm.attr('method')){
        ajax_para['type']='GET';
    }

    if (fn) {
        ajax_para['success']=fn;
    }
    htmlobj=$.ajax(ajax_para);
    return htmlobj;
}