#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-22
@author: Ben
'''
from flask.app import Flask
from flask.templating import render_template
from flask.globals import request

# 使用'flask'web框架和jinja2模版，模拟简单的MVC模式


app = Flask('app_test')

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/signin', methods=['GET'])
def signin_form():
    return render_template('form.html')

@app.route('/signin', methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == '123':
        return render_template('sign_ok.html', username=username)
    return render_template('form.html', message='Bad username or password!', username=username)

if __name__ == '__main__':
    app.run()

