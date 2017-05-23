# coding: utf-8

"""
url -> function
example:
    register_url(url, function)

Todo:
    app.register_blueprint(user.mod, url_prefix='/user')
"""
Map = {}




def register_url(*args):
    """
    register url
    每个 url 和 函数 一一对应。
    本质上是一个字典，可以做到一一对应
    当调用
    example:
        d = {
            '/': function
        }
        d2 = {
            '/hello'; hello
        }
        register_url(d, d2)

    """
    # print('args', args)
    for item in args:
        Map.update(item)


