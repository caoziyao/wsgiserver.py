# coding: utf-8
"""
    werkzeug.templates
    ~~~~~~~~~~~~~~~~~~

    A very simple Python "Template Engine". In fact it just recognizes
    PHP like blocks and executes the code in them::

        t = Template('<% for u in users %>${u['username']}\n<% endfor %>')
        t.render(users=[{'username': 'John'},
                        {'username': 'Jane'}])

    would result in::

        John
        Jane

    You can also create templates from files::

        t = Template.from_file('test.html')

    The syntax elements are a mixture of django, genshi text and mod_python
    templates and used internally in werkzeug components.

    We do not recommend using this template engine in a real environment
    because is quite slow and does not provide any advanced features.  For
    simple applications (cgi script like) this can however be sufficient.


    Syntax Elements
    ---------------

    Printing Variables::

        $variable
        $variable.attribute[item](some, function)(calls)
        ${expression} or <%py print expression %>

    Keep in mind that the print statement adds a newline after the call or
    a whitespace if it ends with a comma.

    For Loops::

        <% for item in seq %>
            ...
        <% endfor %>

    While Loops::

        <% while expression %>
            <%py break / continue %>
        <% endwhile %>

    If Conditions::

        <% if expression %>
            ...
        <% elif expression %>
            ...
        <% else %>
            ...
        <% endif %>

    Python Expressions::

        <%py
            ...
        %>

        <%python
            ...
        %>

    Note on python expressions:  You cannot start a loop in a python block
    and continue it in another one.  This example does *not* work::

        <%python
            for item in seq:
        %>
            ...

    Comments::

        <%#
            This is a comment
        %>


    Missing Variables
    -----------------

    If you try to access a missing variable you will get back an `Undefined`
    object.  You can iterate over such an object or print it and it won't
    fail.  However every other operation will raise an error.  To test if a
    variable is undefined you can use this expression::

        <% if variable is Undefined %>
            ...
        <% endif %>

    Copyright notice: The `parse_data` method uses the string interpolation
    algorithm by Ka-Ping Yee which originally was part of `ltpl20.py`_

    .. _ltipl20.py: http://lfw.org/python/Itpl20.py


    :copyright: 2006 by Armin Ronacher, Ka-Ping Yee.
    :license: BSD License.
"""