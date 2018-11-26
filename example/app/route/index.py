# coding: utf-8


from example.old.templates import render_tempalte

def index(request):
    name = 'cxzy'
    return render_tempalte('index.html', name=name)