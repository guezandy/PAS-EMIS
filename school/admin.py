from django.contrib import admin

from .models import (
    Course,
    CourseOutcome,
    Subject,
    SubjectGroup,
    Student,
)

admin.site.register(Student)
admin.site.register(Course)
admin.site.register(CourseOutcome)
admin.site.register(Subject)
admin.site.register(SubjectGroup)
