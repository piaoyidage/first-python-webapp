#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-29
@author: Ben
'''

# 加载模块
def _load_module(module_name):
    
    last_dot = module_name.rfind('.')
    if last_dot == -1:
        return __import__(module_name, globals(), locals())
    from_name = module_name[:last_dot]
    import_name = module_name[last_dot+1:]
    m = __import__(from_name, globals(), locals(), [import_name])
    return getattr(m, import_name)

m = _load_module('test_05.args_1')
print m
print m.__name__