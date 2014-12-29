#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-24
@author: Ben
'''
import re

_re_route = re.compile(r'(\:[a-zA-Z_]\w*)')

s = '/:user/:comments/list'
print _re_route.split(s)
print _re_route.match(s)
print _re_route.search(s)