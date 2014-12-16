#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-16
@author: Ben
'''

# If you need to determine whether an exception was raised but don’t intend to handle it,
#  a simpler form of the raise statement allows you to re-raise the exception:
# 如果你需要明确一个异常是否被抛出，但是不准备去处理它，一个简单的raise语法格式可以让你重新抛出异常
try:
    raise NameError('Hi, come here.')
except NameError:
    print 'An Exception flew by.'
    raise
finally:
    print 'finally...'