#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-23
@author: Ben
'''

# zip的简单使用

names = ('a', 'b', 'c')
values = (1, 2, 3)

print zip(names, values)    
print dict(zip(names, values))