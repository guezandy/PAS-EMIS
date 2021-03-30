from django.urls import path

from .views import auth, main, sysadmin

from emis.permissions import init_perm_model_app_label

# Initialize permissions module with the app_name
init_perm_model_app_label(app_label=__package__)

app_name = "web_app"
urlpatterns = [
    # Authentication related views
    path("login", auth.login_view, name="login"),
    path("activate/<str:code>", auth.activation_view, name="activate"),
    path("logout", auth.logout_view, name="logout"),
    path("users/<int:pk>", auth.user_detail, name="user-detail"),
    # System administration views
    path("sysadmin/users/create/", sysadmin.create_user, name="create-user"),
    path(
        "sysadmin/users/<int:pk>/detail", sysadmin.user_detail, name="user-detail-admin"
    ),
    path("sysadmin/users", sysadmin.user_list, name="user-directory"),
    # Main views
    path("foo", main.foo, name="foo"),
    path("rest", main.json_endpoint, name="rest"),
    path("testscore/", main.test_score_form, name="testscore"),
    path("", main.index, name="index"),
]
