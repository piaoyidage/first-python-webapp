#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-29
@author: Ben
'''
import re

_RE_INTERCEPTROR_STARTS_WITH = re.compile(r'^([^\*\?]+)\*?$')
_RE_INTERCEPTROR_ENDS_WITH = re.compile(r'^\*([^\*\?]+)$')

s1 = '/admin/'
s1 = '//'
s = _RE_INTERCEPTROR_STARTS_WITH.match(s1)
print(s.groups())