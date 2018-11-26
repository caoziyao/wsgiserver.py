# coding: utf-8

import os
from jinja2 import Environment, FileSystemLoader

# __file__ 指的是本文件的名字
# 得到用于加载模板的目录
path = os.path.abspath(os.path.join('templates'))

# 创建一个加载器, jinja2 会从这个目录中加载模板
loader = FileSystemLoader(path)
# 用加载器创建一个环境, 有了它才能读取模板文件
env = Environment(loader=loader)


def render_tempalte(path, **kwargs):
    """
    本函数接受一个路径和一系列参数
    读取模板并渲染返回
    """
    t = env.get_template(path)
    return t.render(**kwargs)
