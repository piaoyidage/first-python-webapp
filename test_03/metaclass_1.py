#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-17
@author: Ben
'''
from _pyio import __metaclass__

class ListMetaclass(type):
    
    def __new__(cls, name, bases, attrs):
        print type(attrs)
        attrs['add'] = lambda c, value: c.append(value)
#         print 'cls=%s\n name=%s\n bases=%s\n attrs=%s' %(cls, name, bases, attrs)
        attrs.pop('output')
        print('attrs=%s' % attrs)
        return type.__new__(cls, name, bases, attrs)
    
class MyList(list):
    __metaclass__ = ListMetaclass
    
    name = 'mylist'
    
    def output(self):
        print self.__class__.__name__
    
# li = MyList()
# li.add(1)
# print li
# li.output()