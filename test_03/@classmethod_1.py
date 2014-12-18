#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-18
@author: Ben
'''

class Foo(object):
    
    @classmethod
    def output(cls):
        print cls
        
Foo.output()
f = Foo()
print f
print Foo