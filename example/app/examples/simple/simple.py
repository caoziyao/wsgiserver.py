# coding: utf-8

from example.old.server import run_simple
from zywsgi import App
from example.old.templates import render_tempalte

app = App(__name__)

@app.route('/')
def index(environ):
    name = 'cxzy'
    return render_tempalte('index.html', name=name)


@app.route('/hello')
def index(environ):
    return 'hello'

@app.before_request
def before_request():
    print('before request')


if __name__ == '__main__':
    config = dict(
        host='0.0.0.0',
        port=3000,
        debug=True,
    )
    run_simple(**config)