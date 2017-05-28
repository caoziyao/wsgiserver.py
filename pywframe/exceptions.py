# coding: utf-8
"""
    pywframe.exceptions
    ~~~~~~~~~~~~~~~~~~~

    This module implements exceptions for the most important HTTP status
    codes.  Each exception is a small WSGI application you can return
    in views.  Simple usage example would look like this::

        from werkzeug.exceptions import HTTPException, NotFound

        def application(environ, start_response):
            request = Request(environ)
            try:
                response = view_func(request)
            except NotFound:
                response = get_not_found_response(request)
            except HTTPException, e:
                response = e
            return response(environ, start_response)

    :copyright: 2007 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

class HTTPException(Exception):
    """
    Baseclass for all HTTP exceptions.
    """
    pass