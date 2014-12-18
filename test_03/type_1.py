#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-17
@author: Ben
'''

# 使用type(name,bases, dict)动态创建类
def func(self, name):
    print 'hello, %s' % name 
    
H = type('Hello', (object,), dict(hello=func))
h = H()
h.hello('Ben')
