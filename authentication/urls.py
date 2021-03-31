from django.urls import path

from .views import auth, sysadmin

from emis.permissions import init_perm_model_app_label

# Initialize permissions module with the app_name
init_perm_model_app_label(app_label=__package__)

app_name = "authentication"

urlpatterns = [
    # Authentication related views
    path("login", auth.login_view, name="login"),
    path("register", auth.register_view, name="register"),
    path("logout", auth.logout_view, name="logout"),
    path("users/<int:pk>", auth.user_detail, name="user-detail"),
    path("activate/<str:code>", auth.activation_view, name="activate"),
    # System administration views
    path("sysadmin/users/create/", sysadmin.create_user, name="create-user"),
    path(
        "sysadmin/users/<int:pk>/detail", sysadmin.user_detail, name="user-detail-admin"
    ),
    path("sysadmin/users", sysadmin.user_list, name="user-directory"),
]
