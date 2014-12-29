#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-29
@author: Ben
'''

def foo(*interceptors):
    L = list(interceptors)
    L.reverse()
    return L 

f = foo(1, 2, 3)
print f
    