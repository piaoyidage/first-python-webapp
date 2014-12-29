#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-29
@author: Ben
'''
import re

# 模拟拦截器链

_RE_INTERCEPTROR_STARTS_WITH = re.compile(r'^([^\*\?]+)\*?$')
_RE_INTERCEPTROR_ENDS_WITH = re.compile(r'^\*([^\*\?]+)$')

def _build_pattern_fn(pattern):
    m = _RE_INTERCEPTROR_STARTS_WITH.match(pattern)
    if m:
        return lambda p: p.startswith(m.group(1))
    m = _RE_INTERCEPTROR_ENDS_WITH.match(pattern)
    if m:
        return lambda p: p.endswith(m.group(1))
    raise ValueError('Invalid pattern definition in interceptor.')

def interceptor(pattern='/'):
    '''
    An @interceptor decorator.
    @interceptor('/admin/')
    def check_admin(req, resp):
        pass
    '''
    def _decorator(func):
        func.__interceptor__ = _build_pattern_fn(pattern)
        return func
    return _decorator

def _build_interceptor_fn(func, next):
    def _wrapper():
        if func.__interceptor__('/test/abc'):
            return func(next)
        else:
            return next()
    return _wrapper

def _build_interceptor_chain(last_fn, *interceptors):
    
    L = list(interceptors)
    L.reverse()
    fn = last_fn
    for f in L:
        fn = _build_interceptor_fn(f, fn)
    return fn

def target():
    print 'target'
    return 123

@interceptor('/')
def f1(next):
    print 'before f1()'
    return next()

@interceptor('/test/')
def f2(next):
    print 'before f2()'
    try:
        return next()
    finally:
        print 'after f2()'
        
@interceptor('/')
def f3(next):
    print 'before f3()'
    try:
        return next()
    finally:
        print 'after f3()'
        
chain = _build_interceptor_chain(target, f1, f2, f3)
print chain()
