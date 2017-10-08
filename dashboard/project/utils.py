# -*- coding: utf-8 -*-

import hashlib  
def output_info(info_dict,interface,key_list=None):
    '''
    将info_dict的信息按照kwargs中的字段收集起来，进行INTERFACE字典转换
    :param info_dict:内部信息字典
    :param key_list:本模块内部使用的key,用来过滤所需要的信息
    :param interface:内部key到外部key的映射
    :return:
    '''
    #out_key 不能重复

    if key_list:
        return  {out_key:info_dict[key] for key ,out_key in interface if key in key_list and key in info_dict}
    else:
        return  {out_key:info_dict[key] for key ,out_key in interface if key in info_dict}



def collect_info(info_dict,interface,key_list=None):
    '''
    将info_dict中的信息按照kwargs中的字段收集起来,进行INTERFACE字典转换
    :param info_dict:外部信息字典
    :param key_list:本模块内部使用的key,用来过滤所需要的信息
    :param interface:内部key到外部key的映射
    :return:
    '''
    #key 不能重复

    if  key_list:
        return  {key:info_dict[out_key] for key,out_key in interface if key in key_list and out_key in info_dict}
    else:
        return  {key:info_dict[out_key] for key,out_key in interface if  out_key in info_dict}

def filter_dict(info_dict,key_list):
    if key_list:
        return {key:info_dict[key] for key in key_list if key in info_dict}
    else:
        return info_dict

def month_add(year,month,num):
    addedyear=year+(month+num)/12 #整年数
    addedmonth=(month+num)%12 #不到一年的月数
    if (addedmonth)>12:
        return (addedyear+1,addedmonth-12)
    elif 0<(addedmonth)<=12:
        return (addedyear,addedmonth)
    else:
        return (addedyear-1,addedmonth+12)

def getMD5(str):
    m2 = hashlib.md5()   
    m2.update(str)
    return m2.hexdigest()

if __name__=="__main__":
    print month_add(2015,12,1)