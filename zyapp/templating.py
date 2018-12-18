# coding: utf-8
"""
@author: csy
@license: (C) Copyright 2017-2018
@contact: wyzycao@gmail.com
@time: 2018/12/18 
@desc:
"""
import os


def render_template(template_name_or_list):
    """
    :param template_name_or_list:
    :return:
    """
    tname = template_name_or_list
    path = os.path.join('templates', tname)
    with open(path, 'rb') as f:
        return f.read()
