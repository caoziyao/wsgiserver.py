# coding: utf-8

from zywsgi.session import session
from zywsgi.server import run_simple
from zywsgi.App import App
from zywsgi.templates import render_tempalte

app = App(__name__)

@app.route('/')
def index(environ):
    name = 'cxzy'
    print('index')
    return render_tempalte('index.html', name=name)


@app.route('/hello')
def index(environ):
    print('environ', environ)
    session['123'] = 456

    session['soo'] = 'viii'

    s = ''
    c = environ.get('cookie')
    for k, data in environ.get('cookie'):
        s += '{}={}'.format(k, data)

    return 'hello ' + s


@app.before_request
def before_request():
    print('before request')


if __name__ == '__main__':
    config = dict(
        host='0.0.0.0',
        port=4000,
        debug=True,
    )
    run_simple(**config)
