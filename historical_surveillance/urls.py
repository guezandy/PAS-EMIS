from django.urls import path
from . import views

app_name = "surveillance"
urlpatterns = [
    # for the index page
    path("", views.index, name="index"),
    # for the enrollments page
    path("enrollment", views.enrollment, name="enrollment"),
    # to update the created schools
    path(
        "update_enrollment/<int:code>",
        views.update_enrollment,
        name="update-enrollment",
    ),
    # for the enrollment/capacity page
    path("enroll_class", views.enroll_class, name="enroll_class"),
    # to update the enrollment / capacity
    path(
        "update_enroll_class/<int:code>",
        views.update_enroll_class,
        name="update-enroll-class",
    ),
    # for the create district page
    path("district", views.district, name="district"),
    # to update the created district
    path("update_district/<int:code>", views.update_district, name="update-district"),
    # for the create schools page
    path("create_institution", views.create_institution, name="create-school"),
    # to update the created schools
    path(
        "update_institution/<int:code>", views.update_institution, name="update-school"
    ),
    # enrollment/capacity table by district view
    path("enrolled_district", views.enrolled_district, name="enrolled_district"),
    # Visualization of enrollment / Capacity
    path("district_trend", views.district_trend, name="district_trend"),
    path("compare_trends", views.compare_trends, name="compare_trend"),
    path("district_grade", views.district_grade, name="district_grade"),
    # Visualization of enrollment / grade / gender by school
    path(
        "district_grade_school",
        views.district_grade_school,
        name="district_grade_school",
    ),
    # visualizations of enrollment / grade / gender by district
    path(
        "district_category_school",
        views.district_category_school,
        name="district_category_school",
    ),
    # for the National gender based enrollment aggregates.
    path(
        "national_gender_enrollment",
        views.nationalgenderenrollment,
        name="national_gender_enrollment",
    ),
    path(
        "update_national_gender/<int:code>",
        views.update_national_gender,
        name="update-national-gender",
    ),
    # for the national education census.
    path(
        "national_education_census",
        views.national_education_census,
        name="national_education_census",
    ),
    path(
        "update_national_census/<int:code>",
        views.update_national_census,
        name="update-national-census",
    ),
    # for the national expenditure
    path(
        "national_education_expenditure",
        views.national_education_expenditure,
        name="national_education_expenditure",
    ),
    path(
        "update_national_expenditure/<int:code>",
        views.update_national_expenditure,
        name="update-national-expenditure",
    ),
    # for the national student teacher ratio
    path(
        "national_teacher_ratio",
        views.national_teacher_ratio,
        name="national_teacher_ratio",
    ),
    path(
        "update_national_teacher_ratio/<int:code>",
        views.update_national_teacher_ratio,
        name="update-national-teacher-ratio",
    ),
    path(
        "district_performance",
        views.district_performance,
        name ="district_performance")
    ,
    path(
        "upload_scores",
        views.upload_scores,
        name ="upload_scores"),
    # enrollment analysis summary
    path("enrollment_summary", views.enrollment_summary, name="enrollment_summary"),
    # Annual special education questionnaire
    path("special_ed_quest", views.special_ed_quest, name="special_ed_quest"),

    #========================================
    #For outlier detection at district level
    #========================================
    path("outlier_district", views.outlier_district, name="outlier_district"),

    #========================================
    #For outlier detection at national level
    #========================================
    path("outlier_national", views.outlier_national, name="outlier_national"),


    #=========================================
    #For box plots at district level
    #=========================================
    path("boxplot_district", views.boxplot_district, name="boxplot_district"),

    #============================================
    #For box plots at national level
    #============================================
    path("boxplot_national", views.boxplot_national, name="boxplot_national")

    
]
