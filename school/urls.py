from django.urls import path

from . import views

from emis.permissions import init_perm_model_app_label

# Initialize permissions module with the app_name
init_perm_model_app_label(app_label=__package__)

app_name = "school"

urlpatterns = [
    path("", views.index, name="school_index"),
    path("teachers", views.teachers, name="teachers"),
    path("students", views.students, name="students"),
    path("classes", views.classes, name="classes"),
    path("subject-groups", views.subject_groups, name="subject_groups"),
    path("subject", views.subject, name="subjects"),
    path("courses", views.courses, name="courses"),
    path("grades", views.grades, name="grades"),
]
