# coding: utf-8

"""
    pywframe.wrappers
    ~~~~~~~~~~~~~~~~~

    This module provides simple wrappers around `environ`,
    `start_response` and `wsgi.input`.


"""
from pywframe.utils import lazy_property

class BaseRequest(object):
    """
    base request class
    """
    def __init__(self, environ):
        self.environ = environ


    def body(self):
        self._body = self.environ.split('\r\n\r\n', 1)[1]
        return self._body

    body = lazy_property(body)

    def protocol(self):
        self._protocol = self.environ.split()[2]
        return self._protocol

    protocol = lazy_property(protocol)

    def method(self):
        self._method = self.environ.split()[0]
        return self._method

    method = lazy_property(method)

    def args(self):
        pass

    def data(self):
        pass

    def form(self):
        pass

    def values(self):
        pass

    def cookies(self):
        pass

    def parsed_url(self, url):
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


    def parsed_headers(self, headers):
        """ 解析 headers """
        query = {}
        for h in headers:
            k, v = h.split(': ', 1)
            query[k] = v
        return query


    def headers(self):
        headers = self.environ.split('\r\n\r\n', 1)[0].split('\r\n')[1:]
        self._headers = self.parsed_headers(headers)
        return self._headers

    headers = lazy_property(headers)

    def path(self):
        url = self.url
        path, query = self.parsed_url(url)
        self._path = path
        return self._path

    path = lazy_property(path)

    def query(self):
        url = self.url
        path, query = self.parsed_url(url)
        self._query = query
        return self._query

    query = lazy_property(query)

    def url(self):
        self._url = self.environ.split()[1]
        return self._url

    # 实例
    """
    加载 class 时运行
    """
    # print('before', requesturl)    # <function BaseRequest.url at 0x108a98ea0>
    url = lazy_property(url)
    # print('uuu', url)   # <pywframe.utils.lazy_property object at 0x108efc9b0>


    def base_url(self):
        pass

    def url_root(self):
        pass

    def host_url(self):
        pass

    def host(self):
        pass


class BaseResponse(object):
    """
    base response class
    """
    pass