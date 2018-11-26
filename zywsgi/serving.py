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

sel = selectors.DefaultSelector()
sock = socket.socket()


def accept(sock, mask):
    conn, addr = sock.accept()  # Should be ready
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)


def write(sock, mask):
    r = 'HTTP/1.1 200 OK\r\nContent-Type: text/html;charset=ISO-8859-1\r\n\r\nhello'
    data = r.encode('ascii')

    sock.send(data)
    sel.unregister(sock)
    sock.close()


def read(conn, mask):
    data = conn.recv(1000)  # Should be ready
    if data:
        conn.setblocking(False)
        sel.unregister(conn)

        print('echoing', repr(data))

        s = data.decode('utf-8')
        r = BaseRequest(s)

        if r.url == '/':
            pass

        sel.register(conn, selectors.EVENT_WRITE, write)
    else:
        print('closing', conn)
        sel.unregister(conn)
        conn.close()


def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return '<h1>Hello, web!</h1>'


def run_simple(host, port, applications):
    sock.bind((host, port))
    sock.listen(100)
    sock.setblocking(False)

    sel.register(sock, selectors.EVENT_READ, accept)

    while True:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)

    sel.close()
