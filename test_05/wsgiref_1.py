#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-22
@author: Ben
'''

# 使用wsgiref测试http的请求和响应 

from wsgiref.simple_server import make_server

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
#     return '<h1>Hello World!</h1>'
    return environ

# 创建服务器
httpd = make_server('', 8889, application)
print('Serving HTTP on port 8889...')
# 开始监听http请求
httpd.serve_forever()
