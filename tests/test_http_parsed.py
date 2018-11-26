# coding: utf-8
"""
@author: csy
@license: (C) Copyright 2017-2018
@contact: wyzycao@gmail.com
@time: 2018/11/26 
@desc:
"""

import unittest
from zywsgi.http_parsed import BaseRequest


class IndexHandlerTestCase(unittest.TestCase):

    def test_parsed(self):
        s = 'GET / HTTP/1.1\r\nHost: www.qq.com\r\n\r\n'
        r = BaseRequest(s)

        self.assertEqual('GET', r.method)
        self.assertEqual('HTTP/1.1', r.protocol)
        self.assertEqual('/', r.url)


if __name__ == '__main__':
    unittest.main()
