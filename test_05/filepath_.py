#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-24
@author: Ben
'''
import threading
import os
import mimetypes


ctx = threading.local()
def filefunc(*args):
    fpath = os.path.join(ctx.application.document_root, args[0])
    if not os.path.isfile(fpath):
         raise StandardError('')
    fext = os.path.splitext(fpath)[1]
    ctx.response.content_type = mimetypes().types_map.get(fext.lower(), 'application/octet-stream')
    return ''

filefunc([1, 2, 3])