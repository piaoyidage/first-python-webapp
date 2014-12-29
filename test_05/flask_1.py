#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-22
@author: Ben
'''
from flask.app import Flask
from flask.globals import request

# 使用web框架`flask`，简单模拟针对不同的url，不同的处理函数


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>Home</h1>'


@app.route('/signin', methods=['GET'])
def signin_form():
    return '''<form action='signin' method='post'>
              <p><input name='username'</p>
              <p><input name='password' type='password'></p>
              <p><button type='submit'>Sign In</button></p>
              </form>'''
    
@app.route('/signin', methods=['POST'])
def signin():
    # 从请求表单上读取数据
    if request.form['username'] == 'admin' and request.form['password'] == '123':
        return '<h3>hello, admin</h3>'
    return '<h3>Bad username or password!</h3>'


if __name__ == '__main__':
    app.run();