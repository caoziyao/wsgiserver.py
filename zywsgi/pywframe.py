# coding: utf-8

from zywsgi.routing import Map
from zywsgi.server import run_simple, route_static

class PYWFrame(object):
    """
    app = PYWFrame(__name__)

    @app.route('/')
    def index(environ):
        return 'hello'
    """

    def __init__(self, name):
        # name: __main__
        print('name', name)
        self.before_request_funcs = []


    def regist_route(self, path, func):
        num = path.split('/<')

        r = {
            path: func,
            '/static': route_static,
        }
        Map.update(r)


    def route(self, path):
        """
        @app.route('/')
        def index(environ):
            return 'hello'
        """

        def wrapper(func):
            # 注册路由函数
            self.regist_route(path, func)

            def _wrapper(*args, **kwargs):
                # ret = func(*args, **kwargs)    # 这里进行原函数的计算
                return func
            return _wrapper
        return wrapper


    def before_request(self, func):
        """
        @app.before_request
            def before_request():
                do something
        """
        self.before_request_funcs.append(func)
