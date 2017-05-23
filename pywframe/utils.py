# coding: utf-8

# Python 延迟初始化（lazy property）
# 延迟初始化主要用于提高性能，避免浪费计算，并减少程序的内存需求。
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
        # print(obj) <app.models.request.Request object at 0x105dd2c50>
        value = self.func(obj)
        # print('value', obj, value)   # <app.models.request.Request object at 0x10dfd3b38> /
        # print('name', self.__name__)    # url
        setattr(obj, self.__name__, value)
        return value





