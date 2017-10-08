function total(value, row) {
    var totalcost=0;
    for (var key in row) {
        if (key!="type") {
            number_v=parseFloat(row[key]);
            if (!isNaN(number_v)){
                totalcost+=number_v;
            }
        }
    }

    return money_formatter(totalcost);
}

function table_filter(current){
    $("#comsumptionlist").bootstrapTable('refresh', {
        'onPageChange':function(number, size){
        }
    });
    return false;
}



function search(){
    $("#abc").bootstrapTable('selectPage',1);
    return false;
}

function money_format(value, row) {
    return  parseFloat(value).toFixed(2)
};

function cal_format(value,row){
    switch (value){
        case 'hour':return '小时';
        case 'day':return '天';
        case 'month':return '月';
        case 'year':return '年';
    }
};



function date_format1(value,row,index,format1){
    var pattern =/\d+/g;
    if (typeof (value)=='string' && pattern.test(value)){
        var string_list=value.match(pattern);
        if (!format1){
            format1="yy-mm-dd";
        }
        var date_string=format1;
        if (date_string.indexOf("yy")>-1){
            date_string=date_string.replace('yy',string_list[0]);
        }
        if (date_string.indexOf("mm")>-1){
            date_string=date_string.replace('mm',string_list[1]);
        }
        if (date_string.indexOf("dd")>-1){
            date_string=date_string.replace('dd',string_list[2]);
        }
        if (date_string.indexOf("hh")>-1){
            date_string=date_string.replace('hh',string_list[3]);
        }
        if (date_string.indexOf("MM")>-1){
            date_string=date_string.replace('MM',string_list[4]);
        }
        if (date_string.indexOf("ss")>-1){
            date_string=date_string.replace('ss',string_list[5]);
        }
        return date_string;
    }
    else {
        if (typeof (value)=='Date'){
            return value.format(format1);
        }
        else{
            return value;
        }
    }
}


var tz_offset={
    'east0':0,
    'east1':1,
    'east2':2,
    'east3':3,
    'east4':4,
    'east5':5,
    'east6':6,
    'east7':7,
    'east8':8,
    'east9':9,
    'east10':10,
    'east11':11,
    'east12':12,
    'west1':-1,
    'west2':-2,
    'west3':-3,
    'west4':-4,
    'west5':-5,
    'west6':-6,
    'west7':-7,
    'west8':-8,
    'west9':-9,
    'west10':-10,
    'west11':-11,
    'west12':-12,
    'Asia/Shanghai':"8"
};

Date.prototype.addHours = function(h)
{//h可以是数字,如果为数字表示小时，可以为字符串,表示为 数字小时.数字分钟.数字秒，h可以是正数，也可以为负数
    var timestamp=Date.parse(this);
    timestamp=timestamp+parseInt(h)*60*60*1000;
    newdate=new Date()
    newdate.setTime(timestamp)
    return newdate
};

// (new Date()).Format("yyyy-M-d h:m:s.S")      ==> 2006-7-2 8:9:4.18
Date.prototype.format = function(fmt,tz)
{ //author: meizz
    //如果没有tz时区指示符号,则使用本地时区
    if (!tz){
        var o = {
            "M+" : this.getMonth()+1,                 //月份
            "d+" : this.getDate(),                    //日
            "h+" : this.getHours(),                   //小时
            "m+" : this.getMinutes(),                 //分
            "s+" : this.getSeconds(),                 //秒
            "q+" : Math.floor((this.getMonth()+3)/3), //季度
            "S"  : this.getMilliseconds()             //毫秒
        };
    }
    else{
        tz_time=this.addHours(tz_offset[tz]);
        var o = {
            "M+" : tz_time.getUTCMonth()+1,                 //月份
            "d+" : tz_time.getUTCDate(),                    //日
            "h+" : tz_time.getUTCHours(),                   //小时
            "m+" : tz_time.getUTCMinutes(),                 //分
            "s+" : tz_time.getUTCSeconds(),                 //秒
            "q+" : Math.floor((tz_time.getUTCMonth()+3)/3), //季度
            "S"  : tz_time.getUTCMilliseconds()             //毫秒
        };
    }
    if(/(y+)/.test(fmt))
        fmt=fmt.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));
    for(var k in o)
        if(new RegExp("("+ k +")").test(fmt))
            fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));
    return fmt;
} ;

function t2utc(value,tz){
    //value为tz的时间，通过加减时区偏移量，转化为UTC的时间，tz为空默认为本地时区
    _day=new Date(value);
    if (!tz){
        d=new Date();
        offset=-d.getTimezoneOffset(); //获得当地时间偏移

    }
    else{
        offset="-"+tz_offset[tz]; //获得时区相对于零区的偏移，偏移或者是整数,或者是字符串
    }
    _day.addHours(offset);
    return _day;
};


function utc2t(value,tz){
    //value为utc时间，通过加减时区偏移量，转化为tz时区的时间，tz为空默认为本地时区
    _day=new Date(value);
    if (!tz){
        d=new Date();
        offset=d.getTimezoneOffset(); //获得当地时间偏移

    }
    else{
        offset=tz_offset[tz]; //获得时区相对于零区的偏移，偏移或者是整数,或者是字符串
    }
    _day.addHours(offset);
    return _day ;
};


function date_format_utc2t(value,format1){
    //value 不可为空,format1为空则采用默认格式
    //value 是utc时间的字符串形式,一般为 数字年 数字月 数字日 数字小时 数字分钟 数字秒 ；各个数字之间使用非数字的分隔符号
    var pattern =/\d+/g;
    if (typeof (value)=='string' && pattern.test(value)) {
        var string_list = value.match(pattern);
        if (!format1) {
            format1 = "yyyy-MM-dd";
        }
        if (string_list.length>1){
            string_list[1]=(parseInt(string_list[1])-1).toString();//月份,由于在Date中使用0～11表示月份，需要进行换算
        }
        date1=new Date(eval("Date.UTC("+string_list.join(",")+")"));
        return date1.format(format1,site_tz);//site_tz为配置文件中获取的时区字符串
        /*if (string_list.length>5){//包括小时，分钟，秒

         string_list[3]=(parseInt(string_list[3])-1).toString();//小时
         string_list[4]=(parseInt(string_list[4])-1).toString();//分钟
         string_list[5]=(parseInt(string_list[5])-1).toString();//秒

         }
         else {//日期，不包括小时,分钟，秒
         string_list[1]=(parseInt(string_list[1])-1).toString();//月份
         date1=new Date(eval("Date.UTC("+string_list.join(",")+")"))
         }*/

    }
    else{//如果value不是字符格式，默认为Date格式.
        if (typeof (value)=="Date"){
            return value.format(format1,site_tz);
        }
        else{
            return value
        }
    }
};


function date_format_t2utc(value,row,index,format1){
    var pattern =/\d+/g;
    if (typeof (value)=='string' && pattern.test(value)) {
        var string_list = value.match(pattern);
        if (!format1) {
            format1 = "yyyy-MM-dd hh:mm:ss";
        }
        if (string_list.length>5){
            string_list[1]=(parseInt(string_list[1])-1).toString();
            //string_list[3]=(parseInt(string_list[3])-1).toString();
            string_list[4]=(parseInt(string_list[4])-1).toString();
            string_list[5]=(parseInt(string_list[5])-1).toString();
            date1=eval("new Date("+string_list.join(",")+")")
        }
        else {
            string_list[1]=(parseInt(string_list[1])-1).toString();
            date1=eval("new Date("+string_list.join(",")+")")
        }

    }
    else{
        return value;
    }
};

function date_format_recentcost(value,row,index){
    return date_format_utc2t(value,"yyyy-MM-dd hh:00:00")
}

function date_format_date(value,row,index){
    return date_format_utc2t(value,"yyyy-MM-dd")
}

function date_format_time(value,row,index){
    return date_format_utc2t(value,"yyyy-MM-dd hh:mm:ss")
}

function mergedict(){
    var numargs = arguments.length;
    return_dict={};
    for (var i=0;i<numargs;i++){
        current=arguments[i];
        for (key in current){
            return_dict[key]=current[key];
        }
    }
    return return_dict
}
function get_def(){
    datatext=$.ajax({url:constant_root_url+"/center/datarequest",async:false}).responseText;
    data=JSON.parse(datatext);
    constant_def=mergedict(constant.account_type,constant.resource_type,constant.payment_type,data.region_list);
    return constant_def
}

constant_value= get_def();
function valueformat(value, row){
    //constant.account_type.concat(constant.discount_item).concat(constant.payment_type).concat(constant.resource_type)
    if (value in constant_value){
        return  constant_value[value]
    }
    else{
        if (value=='RegionCdn') {
            return '-'
        }
        return value
    }
}
//function current_day(){
//    var myDate = new Date();
//    var date_str= $.sprintf("%d-%d-%d",myDate.getFullYear(),myDate.getMonth()+1,myDate.getDate());
//    $(this).value=date_str;
//};


function reset_pagination(){
    var page_innerhtml=$(".fixed-table-pagination").html();
    $(".fixed-table-header").innerHTML=page_innerhtml;
    $(".fixed-table-pagination").empty();
}

function load_input_select(){
    for (key in constant.resource_type){
        if (key !='cpu' && key !='memory'&& key !='cdnflow'&& key !='cdnbandwidth'){
            option_html="<option value='"+key+ "'>"+constant.resource_type[key]+"</option>"
            $("#input1").append(option_html)
        }

    }
};


