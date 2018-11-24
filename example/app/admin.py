# coding: utf-8


# class MyAdminView(admin.BaseView):
#     @admin.expose('/')
#     def index(self):
#         return self.render('myadmin.html')
#
#
# def add_admin(app):
#     # Create admin interface
#     admin = admin.Admin()
#     admin.add_view(MyAdminView(category='Test'))
#     admin.add_view(AnotherAdminView(category='Test'))
#     admin.init_app(app)