#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-15
@author: Ben
'''

'''
简单线程
'''
import threading
from time import sleep

def loop():
    print 'Thread %s is running...' % threading.current_thread().name
    n = 0
    while n < 5:
        n = n+1
        print 'Thread %s-%d is running...' % (threading.current_thread().name, n)
        sleep(1)
    print 'Thread %s is ended!' % threading.current_thread().name

# 主线程MainThread
print 'Thread %s is running...' % threading.current_thread().name
# 主线程启动新线程
t = threading.Thread(target=loop, name='LoopThread')
t.start()
t.join()
print 'Thread %s is ended!' % threading.current_thread().name
    
