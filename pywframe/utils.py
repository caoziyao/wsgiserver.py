# coding: utf-8

import datetime
import os

# Python 延迟初始化（lazy property）
# 延迟初始化主要用于提高性能，避免浪费计算，并减少程序的内存需求。
# 只在第一次调用时候被计算之后就把结果缓存起来了。这样的好处是在网络编程中，对HTTP协议的解析，
# 通常会把HTTP的header解析成python的一个字典，而在视图函数的时候，可能不知一次的访问这个header，
# 因此把这个header使用描述器缓存起来，可以减少多余的解析
class lazy_property(object):
    """
    Descriptor implementing a "lazy property", i.e. the function
    calculating the property value is called only once.
    """

    def __init__(self, func, name=None, doc=None):
        self.func = func
        self.__name__ = name or func.__name__
        self.__doc__ = doc or func.__doc__

    def __get__(self, obj, type=None):
        """
        执行 request.url 运行
        :param obj:
        :param type:
        :return:
        """
        if obj is None:
            return self
        value = self.func(obj)
        setattr(obj, self.__name__, value)  # 相当于 obj.__dict__[self.__name__] = value
        return value



def log(*args, **kwargs):
    """log 日志"""
    dt = datetime.datetime.now()
    print(dt, *args, **kwargs)




