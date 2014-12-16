#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-16
@author: Ben
'''

def cal(*args):
    sum = 0
    for x in args:
        sum = sum + x
    print 'sum = %s' % sum
    return sum 

def run_cal(*args):
    cal(*args)
    
args = (1, 2, 3)
run_cal(*args)
