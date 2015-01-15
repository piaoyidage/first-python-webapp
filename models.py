#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-18
@author: Ben
'''
from transwarp.orm import Model, StringField, BooleanField, FloatField, TextField
from transwarp.db import next_id
import time
import logging
from transwarp import db

'''
Models for user, comment, blog
'''

class User(Model):
    
    __table__ = 'users'
    
    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    email = StringField(updateable=False, ddl='varchar(50')
    password = StringField(ddl='varchar(50)')
    admin = BooleanField()
    name = StringField(ddl='varchar(50)')
    image = StringField(ddl='varchar(500)')
    created_at = FloatField(updateable=False, default=time.time)
    
    
class Blog(Model):
    
    __table__ = 'blogs'
    
    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    user_id = StringField(updateable=False, ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    name = StringField(ddl='varchar(50)')
    summary = StringField(ddl='varchar(200)')
    content = TextField()
    created_at = FloatField(updateable=False, default=time.time)
    

class Comment(Model):
    
    __table__ = 'comments'
    
    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    blog_id = StringField(updateable=False, ddl='varchar(50)')
    user_id = StringField(updateable=False, ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    content = TextField()
    created_at = FloatField(updateable=False, default=time.time)
    


# 测试
if __name__ == '__main__':
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
