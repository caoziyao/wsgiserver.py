# coding: utf-8

from pywframe.session import session
from pywframe.server import run_simple
from pywframe.pywframe import PYWFrame
from pywframe.templates import render_tempalte

app = PYWFrame(__name__)

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
        port=3000,
        debug=True,
    )
    run_simple(**config)
