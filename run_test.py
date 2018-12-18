# coding: utf-8
"""
@author: csy
@license: (C) Copyright 2017-2018
@contact: wyzycao@gmail.com
@time: 2018/11/21
@desc:
"""
import os

import coverage
import unittest
from tests.test_http_parsed import IndexHandlerTestCase


def get_covdir():
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'tmp/coverage')
    return covdir


def run_test():
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(IndexHandlerTestCase))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


def cov_start():
    cov = coverage.coverage(branch=True, include=['zyapp/*', 'zywsgi/*'])
    cov.start()
    return cov


def cov_end(cov):
    cov.stop()
    cov.save()
    cov.report()
    covdir = get_covdir()
    cov.html_report(directory=covdir)
    print('HTML version: file://%s/index.html' % covdir)
    cov.erase()


def main():
    cov = cov_start()
    run_test()
    cov_end(cov)


if __name__ == '__main__':
    main()
