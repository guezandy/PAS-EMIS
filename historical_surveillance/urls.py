from django.urls import path
from . import views

app_name = "surveillance"
urlpatterns = [
    # for the index page
    path("", views.index, name="index"),

    # District urls
    # for the viewing districts
    path("districts", views.district, name="districts"),
    # for creating districts
    path("districts/create", views.edit_district, name="create-district"),
    # to update the created district
    path("districts/<int:code>",
         views.edit_district, name="update-district"),

    # School urls
    # for viewing schools
    path("schools", views.school, name="schools"),
    # for creating schools
    path("schools/create", views.edit_school, name="create-school"),
    # to update the created schools
    path(
        "schools/<int:code>", views.edit_school, name="update-school"
    ),

    # Enrollment urls
    # for the enrollments page
    path("enrollments", views.enrollment, name="enrollments"),
    # to update an existing enrollment record
    path(
        "enrollments/<int:code>",
        views.update_enrollment,
        name="update-enrollment",
    ),

    path(
        "enrollments/create",
        views.update_enrollment,
        name="create-enrollment",
    ),

    # Enrollment/Capacity page
    # for the enrollment/capacity page
    path("aggregate-enrollments", views.aggregate_enrollment, name="aggregate-enrollments"),
    # to update the enrollment / capacity
    path(
        "aggregate-enrollments/<int:code>",
        views.update_aggregate_enrollment,
        name="update-aggregate-enrollment",
    ),
    # to create a new enrollment / capacity record
    path(
        "aggregate-enrollment/create",
        views.update_aggregate_enrollment,
        name="create-aggregate-enrollment",
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
        name="district_performance"),
    path(
        "upload_scores",
        views.upload_scores,
        name ="upload_scores"),

    # Grade 6 national examination
    path(
        "cee_results",
        views.cee_results,
        name="cee-results"),
    path(
        "update_cee/<int:id>",
        views.update_cee,
        name="update-cee"),

    path(
        "cee_results/create",
        views.update_cee,
        name="create-cee"),

    #Form 5 National Examination
    path(
        "csec_results",
        views.csec_results,
        name="csec-results"),

    path(
        "update_csec/<int:id>",
        views.update_csec,
        name="update-csec"),

    path(
        "csec_results/create",
        views.update_csec,
        name="create-csec"),

    path(
        "examination_summary",
        views.examination_summary,
        name="examination summary"),

    # enrollment analysis summary
    path("enrollment_summary", views.enrollment_summary, name="enrollment_summary"),
    # Annual special education questionnaire
    # path("special_ed_quest", views.special_ed_quest, name="special_ed_quest"),

    # ========================================
    # For outlier detection at district level
    # ========================================
    path("outlier_district", views.outlier_district, name="outlier_district"),

    # ========================================
    # For outlier detection at national level
    # ========================================
    path("outlier_national", views.outlier_national, name="outlier_national"),

    # =========================================
    # For box plots at district level
    # =========================================
    path("boxplot_district", views.boxplot_district, name="boxplot_district"),

    # ============================================
    # For box plots at national level
    # ============================================
    path("boxplot_national", views.boxplot_national, name="boxplot_national")

]