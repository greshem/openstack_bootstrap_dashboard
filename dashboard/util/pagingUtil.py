# -*- coding: utf-8 -*-
'''
Created on 2016年11月17日

@author: zzg
'''

def paginate(result, search_opts):
    offset = int(search_opts['offset'])
    limit = int(search_opts['limit'])
    total = int(result['total'])
    assert total > offset
    
    if total - offset >= limit:
        rows = result['rows'][offset:offset + limit]
    else:
        rows = result['rows'][offset:]
        
    ret = {}
    ret['total'] = total
    ret['rows'] = rows
    return ret
