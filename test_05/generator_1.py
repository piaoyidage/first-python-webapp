#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-24
@author: Ben
'''

# generator生成器

g = (x*x for x in range(10))
for i in g:
    print i
    
print g.next()