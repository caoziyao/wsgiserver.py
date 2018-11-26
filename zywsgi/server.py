# coding: utf-8
# -*- coding: utf-8 -*-


import socket
from zywsgi.utils import log
from zywsgi.wrappers import BaseRequest
from zywsgi.routing import Map
from zywsgi.templates import render_tempalte
from zywsgi.session import session

"""
WSGI server所做的工作：
1.将从客户端收到的请求传递给WSGI application，
2.然后将WSGI application的返回值作为响应传给客户端
"""

# WSGI server
"""
处理一个HTTP请求的逻辑:
iterable = application(environ, start_response)
for data in iterable:
   # send data to client
"""


def error(code=404):
    body = render_tempalte('404.html')
    return body


# 中间件（Middleware）
class Middleware:
    def __init__(self, app):
        self.wrapped_app = app

    def __call__(self, environ, start_response):
        for data in self.wrapped_app(environ, start_response):
            yield data


class Application():

    # WSGI application接口
    @classmethod
    def application(cls, environ, start_response):
        """
        :param environ: 请求上下文，包含了客户端请求的信息以及其他信息
        :param start_response: 用于发送HTTP响应状态（HTTP status ）、响应头（HTTP headers）的回调函数
        :return:
        """
        response_body = 'Request method: {}'.format(environ['REQUEST_METHOD'])

        # HTTP 响应状态
        status = '200 OK'

        # HTTP 响应头，注意格式
        response_headers = [
            ('Content-Type', 'text/plain'),
            ('Content-Lenght', str(len(response_body)))
        ]

        # 将响应状态和响应头交给 WSGI server，start_response 作用是保存 status 和 headers
        # 参考源码 wsgiref.handlers.start_response
        start_response(status, response_headers)

        # 返回响应正文
        # register_url(route_todo)
        path = environ['PATH']
        response = Map.get(path, error)

        # 路由对应的函数
        html = response(environ)

        # 返回值
        response_body = html
        return [response_body]


class Server():

    def get_application(self):
        pass

    def hander(self):
        pass

    # 请求前, 执行预处理工作中:
    def preprocess_request(self):
        from example import app
        for func in app.before_request_funcs:
            rv = func()
            if rv is not None:
                return rv

    def get_environ(self, request):
        env = {}
        env['SERVER_PROTOCOL'] = request.protocol
        env['REQUEST_METHOD'] = request.method
        env['QUERY_STRING'] = request.query
        env['PATH'] = request.path

        # 自定义 env
        env.setdefault('form', {}).update({})
        env.setdefault('cookie', {}).update(request.cookie)

        return env

    @classmethod
    def start_response(cls, status, response_headers):

        # 请求前, 执行预处理工作中:
        cls.preprocess_request(cls)


class Request(BaseRequest):
    """
    原始 http 请求
    """

    def __init__(self, environ):
        super(Request, self).__init__(environ)


def http_response(body, headers=None, code=200):
    """
    headers 是可选的字典格式的 HTTP 头
    """
    # from werkzeug.contrib.securecookie import SecureCookie
    header = 'HTTP/1.1 {} OK\r\nContent-Type: text/html; text/css; charset=UTF-8\r\n'.format(code)
    if headers is not None:
        header += ''.join(['{}: {}\r\n'.format(k, v)
                           for k, v in headers.items()])

    if session:
        # customer=huangxp; path=/foo; domain=.ibm.com;
        for k, v in session.items():
            s = '{}={};'.format(k, v)
            header += 'Set-Cookie: {}\r\n'.format(s)
    return header + '\r\n' + body


def route_static(request):
    """
    静态资源的处理函数, 读取静态文件并生成响应返回
    """
    query = request['QUERY_STRING']
    filename = query.get('file', '')
    path = 'static/' + filename
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        return content


def parsed_headers(headers):
    """ 解析 headers """
    query = {}
    for h in headers:
        k, v = h.split(': ', 1)
        query[k] = v
    return query


def parsed_url(url):
    # /static?file=zhihu.js&author=gua
    """
    {
        'file': 'zhihu.js',
        'author': 'gua'
    }
    """
    index = url.find('?')
    if index == -1:
        return url, {}
    else:
        path, query_string = url.split('?')
        args = query_string.split('&')
        query = {}
        for arg in args:
            k, v = arg.split('=')
            query[k] = v
        return path, query


def parsed_request(r):
    """第一步解析整个请求
    返回 method header body
    """
    request = Request(r)
    # request.add_cookies()
    return request


def redirect(location):
    """
    重定向
    :param url:
    :return:
    """
    headers = {
        'Location': location
    }
    body = '{}'
    return body


def process_request(connection):
    """ 接收处理数据线程"""
    r = connection.recv(1024)
    r = r.decode('utf-8')
    # 因为 chrome 会发送空请求导致 split 得到空 list
    # 所以这里判断一下防止程序崩溃
    if len(r.split()) < 2:
        connection.close()
        return

    # r 是客户端发送过来的数据
    # request 解析后的数据
    request = parsed_request(r)

    # wsgi server
    server = Server()
    env = server.get_environ(request)
    start_response = Server.start_response

    # wsgi application
    app = Application.application
    app = Middleware(app)
    for data in app(env, start_response):
        # send data to client
        response = http_response(data)
        connection.sendall(response.encode(encoding='utf-8'))

    # print(response.encode(encoding='utf-8'))
    connection.close()


def run_simple(host='0.0.0.0', port=3000, debug=False):
    """
    Start an application
    """
    hostname = host or '0.0.0.0'
    log('* Running on http://{}:{}/'.format(hostname, port))

    def inner():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(5)
        return s

    s = inner()

    try:
        while True:
            # 接收一个连接
            connection, addr = s.accept()
            print('connection from {}'.format(addr))
            # 开一个新的线程来处理请求, 第二个参数是传给新函数的参数列表, 必须是 tuple
            # tuple 如果只有一个值 必须带逗号
            # _thread.start_new_thread(process_request, (connection,))
            # process_request(connection)
            process_request(connection)
    except KeyboardInterrupt as e:
        log('keybord interrupt', e)
