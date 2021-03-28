from django.urls import path

from .views import auth, main

from emis.permissions import init_perm_model_app_label

# Initialize permissions module with the app_name
init_perm_model_app_label(app_label=__package__)

# PRS TODO: remove debug lines
# from django.contrib.auth.models import Permission
# print('permissions: ' + ', '.join([x.codename for x in Permission.objects.all()]))

urlpatterns = [
    # Authentication related views
    path('login', auth.login_view, name='login'),
    path('register', auth.register_view, name='register'),
    path('logout', auth.logout_view, name='logout'),
    
    # Main views
    path('foo', main.foo, name='foo'),
    path('rest', main.json_endpoint, name='rest'),
    path('testscore/', main.test_score_form, name='testscore'),
    path('', main.index, name='index'),
]
