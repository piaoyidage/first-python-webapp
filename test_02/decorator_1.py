#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-16
@author: Ben
'''

import time
import functools

# 在代码运行期间动态增加功能的方式，称之为“装饰器”（Decorator）

def log(func):
    def wrapper(*args, **kw):
        print 'invoke %s()...' % func.__name__
        return func(*args, **kw)
    return wrapper

def log_2(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print '%s invoke %s()...' % (text, func.__name__)
            return func(*args, **kw)
        return wrapper
    return decorator

def log_3(text):
    def decorator(func):
        #为了使加入装饰器后的函数的__name__属性不变，引入functools模块的wraps
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print '%s invoke %s()...' % (text, func.__name__)
            return func(*args, **kw)
        return wrapper
    return decorator

#log
#log_2('Ben')
@log_3('Ben')
def now():
    print time.asctime()
    
f = now
f()
print f.__name__
    
