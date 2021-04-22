from django.urls import path

from . import views

app_name = "welfare"

urlpatterns = [
    path("", views.index, name="welfare_index"),
    path("student/<str:uuid>", views.student_view, name="welfare_student"),
]