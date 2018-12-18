# coding: utf-8
"""
@author: csy
@license: (C) Copyright 2017-2018
@contact: wyzycao@gmail.com
@time: 2018/11/26 
@desc:
"""


import click
# from common.utils import log


@click.group()
def cli():
    pass


@cli.command()
@click.option('-h', '--host', 'host', default='0.0.0.0', show_default=True, help='server host')
@click.option('-p', '--port', 'port', default='8888',  show_default=True,  help='server port')
def runserver(host, port):
    from run_app import main
    main()


@cli.command()
@click.option('--coverage', 'coverage', is_flag=True,  show_default=True, help='Make a HTML coverage report.')
@click.option('--test_dir', 'test_dir', default='tests', show_default=True, help='The directory to discover testcases. Example: tests/test_api.')
def test(coverage, test_dir):
    log('test', coverage, test_dir)
    from run_test import run_test, cov_end, cov_start

    def run_cov():
        cov = cov_start()
        run_test()
        cov_end(cov)

    if coverage:
        run_cov()
    else:
        run_test()


if __name__ == '__main__':
    cli()
