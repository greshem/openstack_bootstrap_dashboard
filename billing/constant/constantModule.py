# -*- coding:utf-8 -*-
'''
Created on 2014-7-18

@author: greshem
'''
class _const: 
    class ConstError(TypeError):pass 
    def __setattr__(self, name, value): 
        if self.__dict__.has_key(name): 
            raise self.ConstError, "Can't rebind const (%s)" %name 
        self.__dict__[name]=value 
import sys 
sys.modules['const'] = _const() 

import constant