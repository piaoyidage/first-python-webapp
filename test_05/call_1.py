#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-24
@author: Ben
'''

class Foo(object):
    
    def __call__(self, name):
        print('hello, %s' % name)
        
obj = Foo()
obj('Robert')
# 输出 hello, Robert