from django.urls import path

from .views import main

urlpatterns = [
    # system admin views
    path('users', main.IndexView.as_view(), name='user-directory')
]