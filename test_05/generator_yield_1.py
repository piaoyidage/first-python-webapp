#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-24
@author: Ben
'''

# yield
# 如果一个函数定义中包含yield关键字，那么这个函数就不再是一个普通函数，而是一个generator：
# 变成generator的函数，在每次调用next()的时候执行，遇到yield语句返回，再次执行时从上次返回的yield语句处继续执行。

def test_yield():
    
    print 'step 1'
    yield 1
    
    print 'step 2'
    yield 2
    
    print 'step 3'
    yield 3
    
t = test_yield()
for i in t:
    print i
# t.next()
# t.next()
# t.next()