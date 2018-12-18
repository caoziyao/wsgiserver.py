# coding: utf-8
"""
@author: csy
@license: (C) Copyright 2017-2018
@contact: wyzycao@gmail.com
@time: 2018/11/24 
@desc:
"""
import os
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World!"


@app.route("/hello")
def hello():
    return render_template('hello.html')


if __name__ == "__main__":
    app.run()
