#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-24
@author: Ben
'''

# 使用yield将函数变为generator
def fabonacci(n):
    index, a, b = 0, 0, 1
    while index < n:
        yield b
        a, b = b, a+b 
        index = index + 1
        
f = fabonacci(6)
for i in f:
    print i