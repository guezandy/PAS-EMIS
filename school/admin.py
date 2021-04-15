from django.contrib import admin

from .models import (
    Course,
    CourseGrade,
    Subject,
    SubjectGroup,
    Assignment,
    AssignmentGrade,
    Student,
)

admin.site.register(Student)
admin.site.register(Course)
admin.site.register(CourseGrade)
admin.site.register(Subject)
admin.site.register(SubjectGroup)
admin.site.register(Assignment)
admin.site.register(AssignmentGrade)
