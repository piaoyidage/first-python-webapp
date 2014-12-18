#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-17
@author: Ben
'''

class foobase:
    def a(self):
        print 'foobase'
        
class foo:
    def a(self):
        print 'foo'
    
        
obj = foo()
obj.a()

f = getattr(foobase, 'a')
setattr(foo, 'a', f.im_func)
obj = foo()
obj.a()