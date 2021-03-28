from django.urls import path

from .views import main

app_name = "sysadmin"
urlpatterns = [
    # system admin views
    path("users/create/", main.create_user, name="create-user"),
    path("users/<int:pk>/detail", main.user_detail, name="user-detail"),
    path("users", main.user_list, name="user-directory"),
]
