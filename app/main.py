# coding: utf-8

import socket
import _thread
from app.route.api.weather import route_api
from app.route.login import route_ajax
from pywframe.routing import Map, register_url
from pywframe.server import run_simple, route_static
from route.index import index


def route():
    """根据 path 回应客户端"""
    # static?file=zhihu.js
    r = {
        '/': index,
        '/static': route_static,
    }
    # r.update(route_todo)
    # r.update(route_api)
    # r.update(route_zhihu)
    # r.update(route_ajax)
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    """
    Map.update(r)


route()

if __name__ == '__main__':
    config = dict(
        host='0.0.0.0',
        port=3000,
        debug=True,
    )
    run_simple(**config)
