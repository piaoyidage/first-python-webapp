#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-29
@author: Ben
'''
from www import config_default, config_override

class Dict(dict):
    '''
    Simple dict but support access as x.y style.
    '''
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v
            
    def __getattr__(self, k):
        try:
            return self[k]
        except KeyError:
            raise AttributeError(r"'Dict' has no attribute '%s'" % k)
        
    def __setattr__(self, k, v):
        self[k] = v 
        
        
def merge(default, override):
    r = {}
    for k, v in default.iteritems():
        if k in override:
            if isinstance(v, dict):
                r[k] = merge(v, override[k])
            else:
                r[k] = override[k]
        else:
            r[k] = v 
    return r

def toDict(d):
    D = Dict() 
    for k, v in d.iteritems():
        D[k] = toDict(v) if isinstance(v, dict) else v 
    return D

configs = config_default.configs

try:
    import config_override
    configs = merge(configs, config_override.configs)
except ImportError:
    pass

# print configs
configs = toDict(configs)
# print configs