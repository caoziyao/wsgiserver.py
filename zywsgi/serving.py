# coding: utf-8
"""
@author: csy
@license: (C) Copyright 2017-2018
@contact: wyzycao@gmail.com
@time: 2018/11/26 
@desc:
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return '<h1>Hello, web!</h1>'
"""

import selectors
import socket
from .http_parsed import BaseRequest


class LevelApp(object):

    def __init__(self, application):
        self.environ = None
        self.response = None

        self.application = application
        self.default_application = application.get('default')
        self.static_application = application.get('static')

    def start_response(self, status, headers_list):
        """
        :return:
        """

        r = 'HTTP/1.1 {}\r\n'.format(status)
        for h in headers_list:
            k = h[0]
            v = h[1]
            r += '{}: {}\r\n'.format(k, v)

        r += '\r\n'

        self.response = r.encode()


class BaseServer(object):

    def __init__(self, host, port, application):
        self.app = LevelApp(application)
        self.selector = selectors.DefaultSelector()
        self.sock = socket.socket()
        self.address = (host, port)
        # self.application = application

        self.request_queue_size = 5

        self.open_socket()

    def accept(self, sock, mask):
        sel = self.selector

        conn, addr = sock.accept()  # Should be ready
        conn.setblocking(False)
        sel.register(conn, selectors.EVENT_READ, self.read)

    def application_from_url(self, url):
        """

        :param url:
        :return:
        """
        app = self.app

        # static
        static = url[1:7]  # /static
        if static == 'static':
            b = app.static_application
        else:
            b = app.application.get(url, app.default_application)

        return b

    def write(self, sock, mask):
        sel = self.selector
        app = self.app
        r = app.environ

        # application = app.application.get(r.url, app.default_application)
        application = self.application_from_url(r.url)

        body = application(app.environ, app.start_response)
        app.response += body
        # data = app.response.encode('ascii')
        data = app.response

        sock.send(data)
        sel.unregister(sock)
        sock.close()

    def read(self, conn, mask):
        sel = self.selector
        app = self.app

        data = conn.recv(1000)  # Should be ready
        if data:
            conn.setblocking(False)
            sel.unregister(conn)

            print('echoing', repr(data))

            s = data.decode('utf-8')
            r = BaseRequest(s)

            app.environ = r

            sel.register(conn, selectors.EVENT_WRITE, self.write)
        else:
            print('closing', conn)
            sel.unregister(conn)
            conn.close()

    def server_close(self):

        self.sock.close()
        self.selector.close()

    def server_bind(self):
        """
        绑定
        """
        sock = self.sock

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(self.address)
        self.server_address = sock.getsockname()

    def server_listen(self):
        """
        监听
        """
        self.sock.listen(self.request_queue_size)

    def open_socket(self):
        sock = self.sock

        self.server_bind()
        self.server_listen()
        sock.setblocking(False)

    def serve_forever(self):
        sock = self.sock
        sel = self.selector

        sel.register(sock, selectors.EVENT_READ, self.accept)
        try:
            while True:
                events = sel.select()
                for key, mask in events:
                    callback = key.data
                    callback(key.fileobj, mask)
        finally:
            print('close')
            self.server_close()
