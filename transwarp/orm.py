#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Created on 2014-12-18
@author: Ben
'''
import logging
import db
# from _pyio import __metaclass__

'''
Database operation module.This module is independent with web module.
'''


class Field(object):
    
    _count = 0
    
    def __init__(self, **kw):
        self.name = kw.get('name', None)
        self._default = kw.get('default', None)
        self.primary_key = kw.get('primary_key', False)
        self.updateable = kw.get('updateable', True)
        self.nullable = kw.get('nullable', False)
        self.insertable = kw.get('insertable', True)
        self.ddl = kw.get('ddl', '')
        self._order = Field._count
        Field._count = Field._count + 1
        
    @property
    def default(self):
        d = self._default
        return d() if callable(d) else d 
    
    def __str__(self):
        s = ['<%s:%s,%s,default(%s),' % (self.__class__.__name__, self.name, self.ddl, self._default)]
        self.nullable and s.append('N,')
        self.insertable and s.append('I,')
        self.updateable and s.append('U,')
        s.append('>')
        return ''.join(s)

# 字符串    
class StringField(Field):
    
    def __init__(self, **kw):
        if not 'defalut' in kw:
            kw['default'] = ''
        if not 'ddl' in kw:
            kw['ddl'] = 'varchar(255)'
        super(StringField, self).__init__(**kw)
        
# 整型
class IntegerField(Field):
    
    def __init__(self, **kw):
        if not 'default' in kw:
            kw['default'] = 0
        if not 'ddl' in kw:
            kw['ddl'] = 'bigint'
        super(IntegerField, self).__init__(**kw)
        
# 浮点型
class FloatField(Field):
    
    def __init__(self, **kw):
        if not 'default' in kw:
            kw['default'] = 0.0
        if not 'ddl' in kw:
            kw['ddl'] = 'real'
        super(FloatField, self).__init__(**kw)
        
# 布尔型
class BooleanField(Field):
    
    def __init__(self, **kw):
        if not 'default' in kw:
            kw['default'] = False
        if not 'ddl' in kw:
            kw['ddl'] = 'bool'
        super(BooleanField, self).__init__(**kw)
        
# 文本类型
class TextField(Field):
    
    def __init__(self, **kw):
        if not 'default' in kw:
            kw['default'] = ''
        if not 'ddl' in kw:
            kw['ddl'] = 'text'
        super(TextField, self).__init__(**kw)
        
# 二进制（存储声音，图片等）
class BlobField(Field):
    
    def __init__(self, **kw):
        if not 'default' in kw:
            kw['default'] = ''
        if not 'ddl' in kw:
            kw['ddl'] = 'blob'
        super(BlobField, self).__init__(**kw)
        
class VersionField(Field):
    
    def __init__(self, name=None):
        super(VersionField, self).__init__(name=name, default=0, ddl='bigint')
   

# 根据表名和键值映射创建表
def _gen_sql(table_name, mapping):
    primary_key = None
    s = ['#generate sql table %s' % table_name, 'create table `%s` (' % table_name]
    # 按照顺序创建表的元素
    for f in sorted(mapping.values(), lambda x, y: cmp(x._order, y._order)):
        if not hasattr(f, 'ddl'):
            raise StandardError('Field %s has not ddl' % f.name)
        ddl = f.ddl
        nullable = f.nullable
        if f.primary_key:
            primary_key = f.name
        s.append(nullable and ' `%s` %s,' % (f.name, ddl) or ' `%s` %s not null,' % (f.name, ddl))
    s.append(' primary key(`%s`)' % primary_key)
    s.append(' );')
    return '\n'.join(s)

# 暂时不知干啥用的？  
_triggers = frozenset(['pre_insert', 'pre_update', 'pre_delete'])       
           
        
# 元类
class ModelMetaclass(type):
    '''
    Metaclass for Model object
    '''
    
    def __new__(cls, name, bases, attrs):
        
        # skip base Model class
        if name == 'Model':
            return super(ModelMetaclass, cls).__new__(cls, name, bases, attrs)
        
        # store all subclass info
        if not hasattr(cls, 'subclasses'):
            cls.subclasses = {}
        if not name in cls.subclasses:
            cls.subclasses[name] = name
        else:
            logging.warning('Refined class:%s' % name)
            
        
        logging.info('Object Relational Mapping class %s...' % name)
        mapping = dict()
        primary_key = None
        # id = StringField()
        # k = id, v = StringField()
        for k, v in attrs.iteritems():
            # 如果v是Field类型的(或者子类)
            if isinstance(v, Field):
                # 设置Field的name属性
                if not v.name:
                    v.name = k 
                logging.info('Found mapping %s=>%s' % (k, v))
                # 对于primary_key处理
                if v.primary_key:
                    if primary_key:
                        raise TypeError(r"class %s can't have more than 1 primary key" % name)
                    if v.updateable:
                        logging.warning('Note:change primary key to un-updateable!')
                        v.updateable = False
                    if v.nullable:
                        logging.warning('Note:change primary key to un-nullable!')
                        v.nullable = False
                    primary_key = v 
                mapping[k] = v
       
        if not primary_key:
            raise TypeError('Primary key is not defined in class %s' % name)
        # 删除类属性        
        for k in mapping.iterkeys():
            attrs.pop(k)
        
        # 数据库表的名字
        if '__table__' not in attrs:
            attrs['__table__'] = name.lower()
        attrs['__mapping__'] = mapping
        attrs['__primary_key__'] = primary_key
        # 创建表
        attrs['__sql__'] = _gen_sql(attrs['__table__'], mapping)
        
        # ?
        for trigger in _triggers:
            if not trigger in attrs:
                attrs[trigger] = None
                
        return super(ModelMetaclass, cls).__new__(cls, name, bases, attrs)
    

class Model(dict):
    '''
    Base class for ORM.
    '''
    
    __metaclass__ = ModelMetaclass
    
    def __init__(self, **kw):
        super(Model, self).__init__(**kw)
        
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r" 'Model' object has no attribute '%s'" % key)
            
    
    def __setattr__(self, key, value):
        self[key] = value
        
        
    @classmethod
    def get(cls, primary_key):
        '''
        get by primary key.
        '''
        d = db.select_one('select * from %s where %s=?' %(cls.__table__, cls.__primary_key__.name), primary_key)
        return cls(**d) if d else None
    
    @classmethod
    def find_first(cls, where, *args):
        '''
        Find by where clause and return one result. If multiple results found, only the first one returned.
        If no result found, return None.
        '''
        d = db.select_one('select * from %s %s' % (cls.__table__, where), *args)
        return cls(**d) if d else None
    
    @classmethod
    def find_by(cls, where, *args):
        '''
         Find by where clause and return a list of results.
        '''
        L = db.select('select * from %s %s' % (cls.__table__, where), *args)
        return [cls(**d) for d in L]
    
    @classmethod
    def find_all(cls, *args):
        '''
        Find all and return list.
        '''
        L = db.select("select * from `%s`" % cls.__table__)
        return [cls(**d) for d in L]
    
    @classmethod
    def count_all(cls):
        '''
        Find by 'select count(pk) from table' and return a integer.
        '''
        return db.select_int('select count (`%s`) from `%s`' % (cls.__primary_key__.name, cls.__table__))
    
    @classmethod
    def count_by(cls, where, *args):
        '''
        Find by 'select count(pk) from table where ...' return int.
        '''
        return db.select_int('select count(`%s`) from `%s` %s' % (cls.__primary_key__.name, cls.__table__, where), *args)
    
    
    def update(self):
        # ?干啥用的，仅仅是为了执行？
        self.pre_update and self.pre_update()
        L = []
        args = []
        for k, v in self.__mapping__.iteritems():
            if v.updateable:
                if hasattr(self, k):
                    arg = k 
                else:
                    arg = v.default 
                    setattr(self, k, arg)
                args.append(arg)
                L.append('`%s`=?' % k)
        pk = self.__primary_key__.name
        args.append(getattr(self, pk))       
        db.update('update %s set %s where %s=?' % (self.__table__, ','.join(L), pk), *args)
        return self
    
    def delete(self):
        self.pre_delete and self.pre_delete()
        pk = self.__primary_key__.name
        args = (getattr(self, pk),)
        db.update('delete from `%s` where `%s`=?' % (self.__table__, pk), *args)
        return self
        
    def insert(self):
        self.pre_insert and self.pre_insert()
        params = {}
        for k, v in self.__mapping__.iteritems():
            if v.insertable:
                if not hasattr(self, k):
                    setattr(self, k, v.default)
                params[k] = getattr(self, k)
        db.insert('%s' % self.__table__, **params)
        return self    
    

if __name__ == '__main__':
    db.create_engine('root', 'root', 'test_python')
    db.update('drop table if exists user')
    db.update('create table user (id int primary key, name text, email text, passwd text, last_modified real)')
    import doctest
    doctest.testmod()