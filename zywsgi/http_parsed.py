# coding: utf-8
"""
@author: csy
@license: (C) Copyright 2017-2018
@contact: wyzycao@gmail.com
@time: 2018/11/26 
@desc:
"""


class BaseRequest(object):
    """
    base request class
    """

    def __init__(self, request):
        self.request = request
        self._parsed_request()

    def _parsed_request(self):
        """
        解析 request
        :param request:
        :return:
        """
        self._parsed_header()
        self._parsed_body()

    def _parsed_header(self):
        """
        解析 header
        :param request:
        :return:
        """
        headers = self.request.split('\r\n\r\n', 1)[0].split('\r\n')[1:]

        query = {}
        for h in headers:
            k, v = h.split(': ', 1)
            query[k] = v

        self.headers = query

    def _parsed_body(self):
        """
        解析body
        :param request:
        :return:
        """
        self.body = self.request.split('\r\n\r\n', 1)[1]

    def get_cookies(self):
        cookie = {}
        headers = self.headers
        cookies = headers.get('Cookie', '')
        kvs = cookies.split('; ')
        for kv in kvs:
            if '=' in kv:
                k, v = kv.split('=')
                cookie[k] = v
        return cookie

    @property
    def method(self):
        self._method = self.request.split()[0]
        return self._method

    @property
    def url(self):
        self._url = self.request.split()[1]
        return self._url

    @property
    def protocol(self):
        self._protocol = self.request.split()[2]
        return self._protocol

    # def parsed_url(self, url):
    #     # /static?file=zhihu.js&author=gua
    #     """
    #     {
    #         'file': 'zhihu.js',
    #         'author': 'gua'
    #     }
    #     """
    #     index = url.find('?')
    #     if index == -1:
    #         return url, {}
    #     else:
    #         path, query_string = url.split('?')
    #         args = query_string.split('&')
    #         query = {}
    #         for arg in args:
    #             k, v = arg.split('=')
    #             query[k] = v
    #         return path, query

    # def path(self):
    #     url = self.url
    #     path, query = self.parsed_url(url)
    #     self._path = path
    #     return self._path
    #
    # def query(self):
    #     url = self.url
    #     path, query = self.parsed_url(url)
    #     self._query = query
    #     return self._query
