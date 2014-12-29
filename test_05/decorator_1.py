#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-22
@author: Ben
'''

# 装饰器

import functools

def log(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print('%s 将要调用函数 %s()' %(text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator

@log('Ben')    
def foo():
    print('Hello world!')
    
foo()