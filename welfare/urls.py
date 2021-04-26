from django.urls import path

from . import views

app_name = "welfare"

urlpatterns = [
    path("", views.index, name="welfare_index"),
    path("create_service", views.service_form, name="create_service"),
    path("edit_service/<str:code>", views.service_form, name="edit_service"),
    path("student/<str:uuid>", views.student_view, name="welfare_student"),
]