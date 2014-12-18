#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-18
@author: Ben
'''
from _pyio import __metaclass__

class UpperAttrMetaclass(type):
    
    def __new__(cls, name, bases, attrs):
        # 选择不以'__'开头的属性
        attrs = ((key, value) for key, value in attrs.iteritems() if not key.startswith('__'))
        upper_attrs = dict((key.upper(), value) for key, value in attrs)
        return super(UpperAttrMetaclass, cls).__new__(cls, name, bases, upper_attrs)


class Foo:
    __metaclass__ = UpperAttrMetaclass
    
    id = 1
    username = 'huge'
    passwd = 'root'
    
print Foo.ID