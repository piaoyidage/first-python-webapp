#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-19
@author: Ben
'''

# 测试db orm sql 


import logging
from www.transwarp import db
from www.models import User


logging.basicConfig(level = logging.DEBUG, 
                    format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt = '%a, %d %b %Y %H:%M:%S',
                    filename = 'info.log',
                    filemode = 'w')

db.create_engine('root', 'root', 'test_python')

u = User(name='test', email='test@example.com', password='123456', image='about:blank')
u.insert()

print u.id

u1 = User.find_first('where email=?', 'test@example.com')
print 'find user\'s name:', u1.name
    
u1.delete()
    
u2 = User.find_first('where email=?', 'test@example.com')
print 'find user:', u2