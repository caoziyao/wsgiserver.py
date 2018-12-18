# coding: utf-8
"""
@author: csy
@license: (C) Copyright 2017-2018
@contact: wyzycao@gmail.com
@time: 2018/11/24 
@desc:
"""

from zyapp import App, render_template

app = App(__name__)


@app.route("/")
def hello():
    return b"Hello hello"


@app.route("/1")
def htest1():
    return render_template('index.html')


def main():
    config = dict(
        host='0.0.0.0',
        port=5002,
    )
    app.run(**config)


if __name__ == "__main__":
    main()
