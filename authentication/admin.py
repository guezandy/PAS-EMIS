from django.contrib import admin

from .models.users import (
    SchoolAdministrator,
    Teacher,
    SchoolPrincipal,
    DistrictEducationOfficer,
    SchoolSuperviser,
    StatisticianAdmin,
    EvaluationAdmin,
    EarlyChildhoodEducator,
    SupportServicesAdmin,
    ExternalAccessor,
)

admin.site.register(SchoolAdministrator)
admin.site.register(Teacher)
admin.site.register(SchoolPrincipal)
admin.site.register(DistrictEducationOfficer)
admin.site.register(SchoolSuperviser)
admin.site.register(StatisticianAdmin)
admin.site.register(EvaluationAdmin)
admin.site.register(EarlyChildhoodEducator)
admin.site.register(SupportServicesAdmin)
admin.site.register(ExternalAccessor)
