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

    # to update the created district
    path('update_district/<int:code>'  , views.update_district, name='update-district'),

    # for the create schools page
    path('create_institution', views.create_institution, name='create-school'),

    # to update the created schools
    path('update_institution/<int:code>' , views.update_institution, name='update-school'),

    # National enrollment /capacity table view
    path('enrolled', views.enrolled, name='enrolled'),

    # enrollment/capacity table by district view
    path('enrolled_district', views.enrolled_district, name='enrolled_district'),

    # Visualization of enrollment / Capacity
    path('district_trend', views.district_trend, name='district_trend'),
    path('compare_trends', views.compare_trends, name='compare_trend'),

    # enrollment / grade / gender
    path('enrolled_grade', views.enrolled_grade, name='enrolled_grade'),
    path('district_grade', views.district_grade, name='district_grade'),

    # Visualization of enrollment / grade / gender by school
    path('district_grade_school', views.district_grade_school, name='district_grade_school'),

    # visualizations of enrollment / grade / gender by district
    path('district_category_school', views.district_category_school, name='district_category_school'),

    # enrollment analysis summary
    path('enrollment_summary', views.enrollment_summary, name='enrollment_summary'),

    # Annual special education questionnnaire
    path('special_ed_quest', views.special_ed_quest, name='special_ed_quest'),

]
