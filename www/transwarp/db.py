#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-15
@author: Ben
'''
import logging
import threading
import functools
import time

'''
Database operation module.
'''

# Dict object
class Dict(dict):
    
    '''
    Simple dict but also support access as x.y style.

    >>> d1 = Dict()
    >>> d1['x'] = 100
    >>> d1.x
    100
    >>> d1.y = 200
    >>> d1['y']
    200
    >>> d2 = Dict(a=1, b=2, c='3')
    >>> d2.c
    '3'
    >>> d2['empty']
    Traceback (most recent call last):
        ...
    KeyError: 'empty'
    >>> d2.empty
    Traceback (most recent call last):
        ...
    AttributeError: 'Dict' object has no attribute 'empty'
    >>> d3 = Dict(('a', 'b', 'c'), (1, 2, 3))
    >>> d3.a
    1
    >>> d3.b
    2
    >>> d3.c
    3
    '''
    
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        # 使其支持自定义初始化
        for k, v in zip(names, values):
            self[k] = v
    
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)
        
    def __setattr__(self, key, value):
        self[key] = value
        

#DBError
class DBError(Exception):
    pass

class MultiColumnError(DBError):
    pass
        
# global engine object
engine = None
# class used for generate engine
class _Engine(object):
    
    def __init__(self, connect):
        self._connect = connect
        
    def connect(self):
        return self._connect()

# create engine
def create_engine(user, password, database, host='127.0.0.1', port=3306, **kw):
    import mysql.connector
    global engine
    if not engine is None:
        raise DBError('engine is already initilized.')
    params = dict(user=user, password=password, database=database, host=host, port=port)
    defaults = dict(use_unicode=True, charset='utf8', collation='utf8_general_ci', autocommit=False)
    for k, v in defaults.iteritems():
        params[k] = kw.pop(k, v)
    params.update(kw)
    params['buffered'] = True
    engine = _Engine(lambda: mysql.connector.connect(**params))
    # test_02 connection...
    logging.info("Init MySQL engine <%s> ok." % hex(id(engine)))
    
# _LasyConnection()的作用是，直到运行SQL时才真正打开数据库连接。如果一个请求没有连接数据库，_LasyConnection()不会有真正的数据库连接。
class _LasyConnection(object):
    
    def __init__(self):
        self.connection = None
        
    def cursor(self):
        if self.connection is None:
            connection = engine.connect()
            logging.info('open connection <%s>...' % hex(id(connection)))
            self.connection = connection
        return self.connection.cursor()
    
    def commit(self):
        return self.connection.commit()
    
    def rollback(self):
        return self.connection.rollback()
    
    def cleanup(self):
        if self.connection:
            connection = self.connection
            self.connection = None
            logging.info('close connection <%s>...' % hex(id(connection)))
            connection.close()
    

class _DbCtx(threading.local):
    '''
    Thread local object that holds connection info.
    '''
    
    def __init__(self):
        self.connection = None
        self.transactions = 0
        
    def is_init(self):
        return not self.connection is None
    
    def init(self):
        logging.info('Open lasy connection ...')
        self.connection = _LasyConnection()
        self.transactions = 0
        
        
    def cleanup(self):
        self.connection.cleanup()
        self.connection = None
    
    def cursor(self):
        return self.connection.cursor()
    
_db_ctx = _DbCtx()

# 数据库连接的上下文，目的是自动获取和释放连接
class _ConnectionCtx(object):
    '''
    _ConnectionCtx object that can open and close connection context. _ConnectionCtx object that can be nested and only the most 
    outer connection has effect.
    
    with connection():
        pass
        with connection():
            pass
    '''
    
    def __enter__(self):
        global _db_ctx
        self.should_cleanup = False
        if not _db_ctx.is_init():
            _db_ctx.init()
            self.should_cleanup = True
        return self
    
    def __exit__(self,exc_type, exc_value, traceback):
        global _db_ctx
        if self.should_cleanup:
            _db_ctx.cleanup()
            
def connection():
    '''
    Return _ConnectionCtx object that can be used by 'with' statement
    
    with connection():
        pass
    '''
    return _ConnectionCtx()

def with_connection(func):
    '''
    Decorator for reuse connection.
    
    @with_connection
    def foo(*args, **kw):
        f1()
        f2()
    ...
        
    '''
    @functools.wraps(func)
    def wrapper(*args, **kw):
        with connection():
            return func(*args, **kw)
    return wrapper 

class _TransactionCtx(object):
    '''
    Transaction object that holds transactions info.
    
    with _TransactionCtx():
        pass
    '''
    
    def __enter__(self):
        global _db_ctx
        self.should_close_conn = False
        if not _db_ctx.is_init():
            _db_ctx.init()
            self.should_close_conn = True
        _db_ctx.transactions = _db_ctx.transactions + 1
        logging.info('init transaction...' if _db_ctx.transactions == 1 else 'join current transaction...')
        return self
    
    def __exit(self, exctype, excvalue, traceback):
        global _db_ctx
        _db_ctx.transactions = _db_ctx.transactions - 1
        try:
            if _db_ctx.transactions == 0:
                if exctype == None:
                    self.commit()
                else:
                    self.rollback()
        finally:
            if self.should_close_conn:
                _db_ctx.cleanup()
    
    def commit(self):
        logging.info('commit transaction...')
        global _db_ctx
        try:
            _db_ctx.connection.commit()
            logging.info('commit ok.')
        except:
            logging.warning('comit failed,try rollback...')
            _db_ctx.connection.rollback()
            logging.warning('rollback ok.')
            raise
        
    def rollback(self):
        global _db_ctx
        logging.warning('rollback transaction...')
        _db_ctx.connection.rollback()
        logging.info('rollback ok.')

def transaction():
    return _TransactionCtx()
        
def _profiling(start, sql=''):
    t = time.time() - start
    if t < 0.1:
        logging.info('[PROFILING][DB] %s:%s' % (t, sql))
    else:
        logging.warning('[PROFILING][DB] %s:%s' % (t, sql))
        
def with_transaction(func):
    '''
    
    '''
    @functools.wraps(func)
    def wrapper(*args, **kw):
        start = time.time()
        with _TransactionCtx():
            return func(*args, **kw)
        _profiling(start)
    return wrapper


def _select(sql, first, *args):
    '''
    Execute select SQL return unique result or a list of results.
    '''
    
    global _db_ctx
    cursor = None
    sql = sql.replace('?', '%s')
    logging.info('SQL:%s, ARGS:%s' % (sql, args))
    try:
        cursor = _db_ctx.connection.cursor()
        cursor.execute(sql, *args)
        if cursor.description:
            # get column's name for each column
            names = [x[0] for x in cursor.description]
        if first:
            values = cursor.fetchone()
            if not values:
                return None
            return Dict(names, values)
        return [Dict(names, values) for values in cursor.fetchall()]
    finally:
        if cursor:
            cursor.close()

@with_connection            
def select_one(sql, *args):
    '''
    Execute select SQL and return expected one result.
    if no result found, return None.
    if multiple results found, the first one returned.
    '''
    return _select(sql, True, *args)

@with_connection
def select(sql, *args):
    '''
    Execute select SQL and return a list of results or empty list if no result.
    '''
    return _select(sql, False, *args)

@with_connection
def select_int(sql, *args):
    '''
    Execute select SQL and expected one int and only one int result. 
    '''
    d = _select(sql, True, *args)
    if len(d) != 1:
        raise MultiColumnError('Except only one column.')
    return d.values()[0]
    

@with_connection
def _update(sql, *args):
    '''
    '''
    global _db_ctx
    cursor = None
    sql = sql.replace('?', '%s')
    logging.info('SQL:%s, ARGS:%s' % (sql, args))
    try:
        cursor = _db_ctx.connection.cursor()
        cursor.execute(sql, *args)
        r = cursor.rowcount
        if _db_ctx.transactions == 0:
            # no transaction environment
            _db_ctx.connection.commit()
            logging.info('auto commmit...')
        return r 
    finally:
        if cursor:
            cursor.close()


def insert(table, **kw):
    '''
    '''
    cols, args = zip(*kw.iteritems())
    sql = 'insert into `%s` (%s) values (%s)' % (table, ','.join(['`%s`' % col for col in cols]), ','.join(['?' % i for i in range(len(cols))]))
    _update(sql, *args)
    
def update(sql, *args):
    '''
    '''
    return _update(sql, *args)

if __name__ == '__main__':
    create_engine('root', 'root', 'test_python')
    update('drop table if exists user')
    update('create table user(id int primary key, name text, passwd text, last_modified real)')
    import doctest
    doctest.testmod()