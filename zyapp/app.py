# coding: utf-8
"""
@author: csy
@license: (C) Copyright 2017-2018
@contact: wyzycao@gmail.com
@time: 2018/11/26 
@desc:
"""
# from zywsgi.serving import run_simple
from zywsgi.serving import BaseServer


#
# def decorator(name):
#     def wrapper(func):
#         print("在这里也可用装饰器的name参数：", name)
#
#         def _wrapper(*args, **kwargs):
#             print("这里还可使用装饰器的name参数：", name)
#             ret = func(*args, **kwargs)  # 这里进行原函数的计算
#             return ret * 2
#
#         return _wrapper  # 返回可调用对象，_wrapper可以接受原函数的参数
#
#     return wrapper  # 返回真正的装饰器，接受原函数作为第一个参数
#
#
# # 相当于 wait_for_deco = decorator(args)(x, y)
# @decorator('haha')
# def wait_for_deco(x, y):
#     return x + y




class App(object):

    def __init__(self, import_name):
        self.import_name = import_name

    def run(self, host='0.0.0.0', port=5001):

        def application(environ, start_response):
            start_response('202 OK', [('Content-Type', 'text/html')])
            return 'Hello a, web!'

        httpd = BaseServer(host, port, application)
        httpd.serve_forever()
        # run_simple(host, port, application)


    def route(self, path):
        print('path', path)

        def wrapper(func):
            def _wrap(*args, **kwargs):
                res = func(*args, **kwargs)
                return res

            return _wrap

        return wrapper
