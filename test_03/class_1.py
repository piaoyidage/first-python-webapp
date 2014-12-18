#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-18
@author: Ben
'''
from _pyio import __metaclass__

class ModelMetaclass(type):
    
    def __new__(cls, name, bases, attrs):
        
        if name == 'Model':
            return super(ModelMetaclass, cls).__new__(cls, name, bases, attrs)
#         for k in attrs.keys():
#             attrs.pop(k)
        attrs.pop('id')
        attrs.pop('username')
        attrs.pop('password')
        print attrs
        return super(ModelMetaclass, cls).__new__(cls, name, bases, attrs)

class Model(dict):
    
    __metaclass__ = ModelMetaclass

    def __init__(self,**kw):
        super(Model, self).__init__(self,**kw)
        
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)
 
    def __setattr__(self, key, value):
        self[key] = value
        
        

class User(Model):
    
    id = 1
    username = 'huge'
    password = 'root'
    
#     def __init__(self, id, username, password):
#         self.id = id
#         self.username = username
#         self.password = password
    
user = User(id=2, username='lisi', password='123')
print user['id']
print user.id
args = []
args.append(getattr(user, 'id'))
args.append(getattr(user, 'username'))
args.append(getattr(user, 'password'))
print args