#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-18
@author: Ben
'''

class Student(object):
    
    def __init__(self):
        self._score = 0
    
    @property
    def score(self):
        return self._score
    
    @score.setter
    def score(self, value):
        
        if not isinstance(value, int):
            raise ValueError('value is not a integer!')
        elif value > 100 or value < 0:
            raise ValueError('value should be between 0 and 100!')
        
        self._score = value
        
s = Student()
print s.score
s.score = 100
print s.score