#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-18
@author: Ben
'''

from _pyio import __metaclass__

class ListMetaclass(type):
    
    def __new__(cls, name, bases, attrs):
        print type(attrs)
        attrs['add'] = lambda c, value: c.append(value)
        mapping = dict()
#         for k, v in attrs.iteritems():
#             mapping[k] = v 
        mapping['name'] = 'MyList'
        print('mapping=%s' % mapping)
        attrs.pop('name')
#         for k in mapping.iterkeys():    
#             attrs.pop(k)
        print('attrs=%s' % attrs)
        attrs['mapping'] = mapping
        print('attrs=%s' % attrs)
        return type.__new__(cls, name, bases, attrs)
    
class MyList(list):
    __metaclass__ = ListMetaclass
    
    name = 'mylist'
    
    def output(self):
        print self.__class__.__name__
        
    def show_args(self):
        args = []
        for k in self.mapping.iterkeys():
            args.append(getattr(self, k, None))
        print('args=%s' % args)

li = MyList()
li.show_args()
