from django.urls import path

from . import views as authentication_views

urlpatterns = [
    # Authentication related views
    path('login', authentication_views.login_view, name='login'),
    path('register', authentication_views.register_view, name='register'),
    path('logout', authentication_views.logout_view, name='logout'),
]