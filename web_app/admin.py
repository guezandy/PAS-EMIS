from django.contrib import admin
from web_app.models.main import TestScore

class TestScoreAdmin(admin.ModelAdmin):
    pass
admin.site.register(TestScore, TestScoreAdmin)