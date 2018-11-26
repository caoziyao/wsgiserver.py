# coding: utf-8
"""
@author: csy
@license: (C) Copyright 2017-2018
@contact: wyzycao@gmail.com
@time: 2018/11/24 
@desc:
"""

from zywsgi.App import App

app = App(__name__)


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run()
