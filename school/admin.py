from django.contrib import admin

from .models import Course, CourseOutcome, Student, PrincipalAppraisal, TeacherAppraisal

admin.site.register(Student)
admin.site.register(Course)
admin.site.register(CourseOutcome)
admin.site.register(PrincipalAppraisal)
admin.site.register(TeacherAppraisal)
