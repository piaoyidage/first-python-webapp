#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-15
@author: Ben
'''

import logging


logging.basicConfig(level = logging.DEBUG, 
                    format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt = '%a, %d %b %Y %H:%M:%S',
                    filename = 'test_02.log',
                    filemode = 'w')

logging.debug("This is a debug message")
logging.info("This is a info message")
logging.warning("This is a warning message")
logging.error("This is a error message")
logging.critical("This is a critical message")
