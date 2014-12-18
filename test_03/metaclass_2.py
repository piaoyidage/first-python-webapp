#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-18
@author: Ben
'''
from _pyio import __metaclass__


# 将该模块所有的类的属性名都改成大写
# __metaclass__未必是类，可以是方法

def upper_attr(name, bases, attrs):
    # 选择所有不以‘__’开头的属性
    attrs = ((key, value) for key, value in attrs.items() if not key.startswith('__'))
    upper_attrs = dict((key.upper(), value) for key, value in attrs)
    return type(name, bases, upper_attrs)

# 作用于整个模块
# __metaclass__ = upper_attr

class Foo:
    # 仅仅作用于Foo类
    __metaclass__ = upper_attr
    
    alpha = 'A'
    
    def output(self):
        pass
    
class Hi:
    beta = 'B'
    
    def output(self):
        pass

foo = Foo()
print hasattr(foo, 'alpha')
print hasattr(foo, 'ALPHA')
print hasattr(foo, 'output')
print hasattr(foo, 'OUTPUT')


hi = Hi()
print hasattr(hi, 'beta')
print hasattr(hi, 'BETA')