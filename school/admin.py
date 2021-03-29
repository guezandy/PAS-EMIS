from django.contrib import admin

from django.contrib import admin
from .models import (
    District,
    School,
    Teacher,
    Class,
    Course,
    Subject,
    SubjectGroup,
    Grade,
)


class DistrictAdmin(admin.ModelAdmin):
    pass


class TeacherAdmin(admin.ModelAdmin):
    pass


class ClassAdmin(admin.ModelAdmin):
    pass


class CourseAdmin(admin.ModelAdmin):
    pass


class SubjectAdmin(admin.ModelAdmin):
    pass


class SubjectGroupAdmin(admin.ModelAdmin):
    pass


class GradeAdmin(admin.ModelAdmin):
    pass


admin.site.register(District, DistrictAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(SubjectGroup, SubjectGroupAdmin)
admin.site.register(Grade, GradeAdmin)
