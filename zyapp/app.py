# coding: utf-8
"""
@author: csy
@license: (C) Copyright 2017-2018
@contact: wyzycao@gmail.com
@time: 2018/11/26 
@desc:
"""
from zywsgi.serving import BaseServer


def default(environ, start_response):
    start_response('202 OK', [('Content-Type', 'text/html')])
    return b'404'


def render_static(environ, start_response):
    start_response('200 OK', [('Content-Type', 'image/webp,image/apng,image/*,*/*')])
    path = environ.url[1:]
    with open(path, 'rb') as f:
        return f.read()


class App(object):

    def __init__(self, import_name):
        self.import_name = import_name
        self.application = {
            'default': default,
            'static': render_static,
        }

    def run(self, host='0.0.0.0', port=5001):
        application = self.application

        print('running http://{}:{}'.format(host, port))
        httpd = BaseServer(host, port, application)
        httpd.serve_forever()

    def route(self, path):
        print('path', path)

        def wrapper(func):
            def _wrap(environ, start_response, *args, **kwargs):
                res = func(*args, **kwargs)
                start_response('200 OK', [('Content-Type', 'text/html')])
                return res

            self.application.update({
                path: _wrap,
            })
            return _wrap

        return wrapper
