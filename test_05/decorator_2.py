#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-24
@author: Ben
'''

# 测试decorator模式

def get(path):
    def _decorator(func):
        func.__web_route__ = path 
        func.__web_method__ = 'GET'
        return func
    return _decorator 

@get('/')
def test():
    return '200 OK'

test()
print test.__web_route__
print test.__web_method__
