from django.contrib import admin

from .models.users import (
    SchoolAdministrator,
    Teacher,
    SchoolPrincipal,
    DistrictEducationOfficer,
    SchoolSupervisionOfficer,
    StatisticianAdmin,
    EvaluationAdmin,
    EarlyChildhoodEducationOfficer,
    SupportServicesAdmin,
    ExternalAssessor,
)

admin.site.register(SchoolAdministrator)
admin.site.register(Teacher)
admin.site.register(SchoolPrincipal)
admin.site.register(DistrictEducationOfficer)
admin.site.register(SchoolSupervisionOfficer)
admin.site.register(StatisticianAdmin)
admin.site.register(EvaluationAdmin)
admin.site.register(EarlyChildhoodEducationOfficer)
admin.site.register(SupportServicesAdmin)
admin.site.register(ExternalAssessor)
