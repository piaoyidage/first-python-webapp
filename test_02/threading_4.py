#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-15
@author: Ben
'''
import threading

'''
ThreadLocal对象，方便用于处理线程的局部对象
'''

# local对象，对于不同线程，都有各自的局部对象
local_school = threading.local();

def process_student():
    print 'Student %s in %s...' % (local_school.student, threading.current_thread().name)
    
def process_thread(name):
    local_school.student = name
    process_student()
    
t1 = threading.Thread(target=process_thread, args=('Ben',), name='Thread-A')
t2 = threading.Thread(target=process_thread, args=('Robert',), name='Thread-B')
t1.start()
t2.start()
t1.join()
t2.join()

