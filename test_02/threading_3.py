#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-15
@author: Ben
'''
import threading

'''
线程加锁，以保持同步
'''

# 锁
lock = threading.Lock()

balance = 0
def change(value):
    global balance
    balance = balance + value
    balance = balance - value 
    
def run_thread(value):
    for i in range(10000):
        try:
            # 获取锁
            lock.acquire()
            change(value)
        finally:
            # 释放锁
            lock.release()

t1 = threading.Thread(target=run_thread, args=(5,))
t2 = threading.Thread(target=run_thread, args=(8,))
t1.start()
t2.start()
t1.join()
t2.join()
print 'balance=%d' % balance