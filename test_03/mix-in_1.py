#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-17
@author: Ben
'''

class foo:
    pass

class foobase:
    def hello(self):
        print('hello')
        
obj = foo()
foo.__bases__ += (foobase,)
obj.hello()