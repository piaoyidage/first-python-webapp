#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-23
@author: Ben
'''

# 测试StringIO

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

s = StringIO('A')
s.write('abc')
# 会提示：AttributeError: 'cStringIO.StringI' object has no attribute 'write'
print s.getvalue()


# from StringIO import StringIO

# # 生成一个StringIO对象，当前缓冲区内容为ABCDEF  
# s = StringIO('ABCDEF')
# # 从开头写入，将会覆盖ABC
# s.write('abc')
# # 每次使用read()读取前，必须seek()
# # 定位到开头
# s.seek(0)
# # 将输出abcDEF
# print s.read()
# # 定位到第二个字符c
# s.seek(2)
# # 从当前位置一直读取到结束，将输出cDEF
# print s.read()
# s.seek(3)
# # 从第三个位置读取两个字符，将输出DE
# print s.read(2)
# s.seek(6)
# # 从指定位置写入
# s.write('GH')
# s.seek(0)
# # 将输出abcDEFGH
# print s.read()
# # 如果读取所有内容，可以直接使用getvalue()
# # 将输出abcDEFGH
# print s.getvalue()
    

    