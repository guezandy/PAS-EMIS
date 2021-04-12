from django.contrib import admin

from .models import Class, Course, Subject, SubjectGroup, Grade, Student

admin.site.register(Student)
admin.site.register(Class)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(SubjectGroup)
admin.site.register(Grade)
