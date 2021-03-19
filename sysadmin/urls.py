from django.urls import path

from .views import main

urlpatterns = [
    # system admin views
    path('user-directory', main.user_directory, name='user-directory')
]