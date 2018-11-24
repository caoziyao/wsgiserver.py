from . import *
from .login import session, User, curr_user, login_required


#
# # @login_required
# def index(request):
#     user = curr_user(request)
#     if user:
#         username = user.username
#     else:
#         username = '游客'
#     body = tempalte('index.html', username=username)
#     return http_response(body)
#
#
# def search(request):
#     print('python search')
#     body = json.dumps({'i': 'j'})
#     return http_response(body)
#
#
# def login(request):
#     """用户登录
#     """
#     response = tempalte('login.html')
#     return http_response(response)
#
#
# route_zhihu = {
#     '/zhihu': index,
#     '/api/zhihu/search': search,
#     '/login': login,
# }
