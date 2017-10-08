/**
 * Created by yamin on 16-1-8.
 */
var tz_offset={
    //时区
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
    'Asia/Shanghai':8
};


Date.prototype.addHours = function(h)
{//h可以是数字,如果为数字表示小时，可以为字符串,表示为 数字小时.数字分钟.数字秒，h可以是正数，也可以为负数
    var timestamp=Date.parse(this);
    timestamp=timestamp+parseInt(h)*60*60*1000;
    newdate=new Date()
    newdate.setTime(timestamp)
    return newdate
};

Date.prototype.format = function(fmt,tz)
{ //tz为时区的关键字，fmt为格式字符串，该函数以tz时区，fmt格式显示时间，如果tz不存在，则以本地显示时间

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

function date_from_str(value) {
    //日期字符串格式为 年-月-日 时：分：秒
    var pattern = /\d+/g;
    if (typeof (value) == 'string' && pattern.test(value)) {
        var string_list = value.match(pattern);
        if (string_list.length > 1) {
            string_list[1] = (parseInt(string_list[1]) - 1).toString();//月份,由于在Date中使用0～11表示月份，需要进行换算
        }
        date1 = new Date(eval("Date.UTC(" + string_list.join(",") + ")"));
        return date1
    }
    else{
        return value
    }
}

function date_format_utc2t(value,format1){
    //value 不可为空,format1为空则采用默认格式
    //value 是utc时间的字符串形式,一般为 数字年 数字月 数字日 数字小时 数字分钟 数字秒 ；各个数字之间使用非数字的分隔符号
    if (!value){
        return "-"
    }
    date1=date_from_str(value);
    if (typeof(date1)=="object" && date1.constructor==Date){
        return date1.format(format1,site_tz);
    }
    else{
        return value
    }
};

function date_format_date(value,row,index){
    current=date_format_utc2t(value,"yyyy-MM-dd");
    return current;
}

function date_format_time(value,row,index){
    current=date_format_utc2t(value,"yyyy-MM-dd hh:mm:ss");
    return current;
}

function utc2local(){
    $(".datetime_time").each(function(){
        date_text=$(this).text();
        $(this).text(date_format_time(date_text));
    });
    $(".datetime_date").each(function(){
        date_text=$(this).text();
        $(this).text(date_format_date(date_text));
    });
}
