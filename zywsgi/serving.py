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


# sel = selectors.DefaultSelector()
# sock = socket.socket()


class LevelApp(object):

    def __init__(self, application=None):
        self.environ = None
        self.application = application
        self.response = None

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

        self.response = r


#
#
# def accept(sock, mask):
#     conn, addr = sock.accept()  # Should be ready
#     conn.setblocking(False)
#     sel.register(conn, selectors.EVENT_READ, read)
#
#
# def write(sock, mask):
#     body = app.application(app.environ, app.start_response)
#     app.response += body
#     # r = 'HTTP/1.1 200 OK\r\nContent-Type: text/html;charset=ISO-8859-1\r\n\r\nhello'
#     data = app.response.encode('ascii')
#
#     sock.send(data)
#     sel.unregister(sock)
#     sock.close()
#
#
# def read(conn, mask):
#     data = conn.recv(1000)  # Should be ready
#     if data:
#         conn.setblocking(False)
#         sel.unregister(conn)
#
#         print('echoing', repr(data))
#
#         s = data.decode('utf-8')
#         r = BaseRequest(s)
#
#         app.environ = r
#
#         sel.register(conn, selectors.EVENT_WRITE, write)
#     else:
#         print('closing', conn)
#         sel.unregister(conn)
#         conn.close()

#
# def run_simple(host, port, application):
#     sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#
#     sock.bind((host, port))
#     sock.listen(100)
#     sock.setblocking(False)
#
#     sel.register(sock, selectors.EVENT_READ, accept)
#     app.application = application
#
#     try:
#         while True:
#             events = sel.select()
#             for key, mask in events:
#                 callback = key.data
#                 callback(key.fileobj, mask)
#     finally:
#         print('close')
#         sock.close()
#         sel.close()


class BaseServer(object):

    def __init__(self, host, port, application):
        self.app = LevelApp()
        self.selector = selectors.DefaultSelector()
        self.sock = socket.socket()
        self.address = (host, port)
        # self.application = application
        self.app.application = application

    def accept(self, sock, mask):
        sel = self.selector

        conn, addr = sock.accept()  # Should be ready
        conn.setblocking(False)
        sel.register(conn, selectors.EVENT_READ, self.read)

    def write(self, sock, mask):
        sel = self.selector
        app = self.app

        body = app.application(app.environ, app.start_response)
        app.response += body
        # r = 'HTTP/1.1 200 OK\r\nContent-Type: text/html;charset=ISO-8859-1\r\n\r\nhello'
        data = app.response.encode('ascii')

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

    def serve_forever(self):
        sock = self.sock
        sel = self.selector

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock.bind(self.address)
        sock.listen(100)
        sock.setblocking(False)

        sel.register(sock, selectors.EVENT_READ, self.accept)
        # app.application = application

        try:
            while True:
                events = sel.select()
                for key, mask in events:
                    callback = key.data
                    callback(key.fileobj, mask)
        finally:
            print('close')
            sock.close()
            sel.close()
