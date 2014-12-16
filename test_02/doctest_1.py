#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-15
@author: Ben
'''

'''
doctest 文档测试
'''

def abs(n):
    '''
    Function to get absolute value of number.
    
    Example:
    
    >>> abs(1)
    1
    >>> abs(-1)
    1
    >>> abs(0)
    0
    
    '''
    
    return n if n >= 0 else -n 


class Dict(dict):
    
    '''
    Simple dict but also support access as x.y style.

    >>> d1 = Dict()
    >>> d1['x'] = 100
    >>> d1.x
    100
    >>> d1.y = 200
    >>> d1['y']
    200
    >>> d2 = Dict(a=1, b=2, c='3')
    >>> d2.c
    '3'
    >>> d2['empty']
    Traceback (most recent call last):
        ...
    KeyError: 'empty'
    >>> d2.empty
    Traceback (most recent call last):
        ...
    AttributeError: 'Dict' object has no attribute 'empty'
    '''
    
    def __init__(self, **kw):
        super(Dict, self).__init__(**kw)
    
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s' " % key)
    
    def __setattr__(self, key, value):
        self[key] = value
        



if __name__ == '__main__':
    import doctest
    doctest.testmod()
