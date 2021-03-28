from django.urls import path
from . import views

app_name = 'surveillance'
urlpatterns = [

    # for the index page
    path('', views.index, name='index'),

    # for the enrollments page
    path('enrollment', views.enrollment, name='enrollment'),

    # for the enrollment/capacity page
    path('enroll_class', views.enroll_class, name='enroll_class'),

    # for the create district page
    path('district', views.district, name='district'),

    # for the create schools page
    path('school', views.school, name='school'),

    # to
    path('enrolled', views.enrolled, name='enrolled'),
    path('district_1', views.enrolled_trend_district_1, name='enrolled_trend_1'),
    path('district_2', views.enrolled_trend_district_2, name='enrolled_trend_2'),
    path('district_3', views.enrolled_trend_district_3, name='enrolled_trend_3'),
    path('district_4', views.enrolled_trend_district_4, name='enrolled_trend_4'),
    path('district_5', views.enrolled_trend_district_5, name='enrolled_trend_5'),
    path('district_6', views.enrolled_trend_district_6, name='enrolled_trend_6'),
    path('district_7', views.enrolled_trend_district_7, name='enrolled_trend_7'),
    path('district_8', views.enrolled_trend_district_8, name='enrolled_trend_8'),
    path('district_1_trend', views.district_1_trend, name='district_1_trend'),
    path('district_2_trend', views.district_2_trend, name='district_2_trend'),
    path('district_3_trend', views.district_3_trend, name='district_3_trend'),

]
