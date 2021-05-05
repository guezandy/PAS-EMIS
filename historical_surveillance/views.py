
import json


import pandas as pd
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.utils.datetime_safe import date

from django.http import HttpResponse

from .forms import *
from .models import *
from .utils import *


# This is the view for the home page of this app
def index(request):
    return render(request, 'surv_home.html', {})


def district(request, code=None):
    data = District.objects.all()
    if code:
        district_query = District.objects.filter(district_code=code)
        # Invalid district code
        if not district_query.exists():
            return redirect("/historical/district")
        instance = district_query.first()
    else:
        instance = District(
            created_by=request.user.username,
            updated_by=request.user.username,
            created_at=date.today().strftime("%Y-%m-%d"),
            updated_at=date.today().strftime("%Y-%m-%d")
        )
    form = DistrictForms(request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            # check if the district name already exist, then don't insert into the database
            district_name = form.cleaned_data['district_name']
            if not District.objects.filter(district_name=district_name).exists():
                form.save()
            return redirect("/historical/district")
    context = {"form": form, "district_created": data}
    return render(request, "district.html", context)


def update_district(request, code=None):
    district_to_update = get_object_or_404(District, pk=code)
    if request.method == 'POST':
        form = DistrictForms(request.POST)
        if form.is_valid():
            district_to_update.district_name = form.cleaned_data['district_name']
            district_to_update.district_code = form.cleaned_data['district_code']
            district_to_update.updated_at = date.today().strftime("%Y-%m-%d")
            district_to_update.updated_by = request.user.username
            district_to_update.save()
        return redirect("/historical/district")
    return render(request, 'edit_district.html', {'district_to_update': district_to_update})


# This function controls the schools creation form view and process form data for save into the database
def create_institution(request):
    data = School.objects.all()
    instance = School(
        created_by=request.user.username,
        updated_by=request.user.username
    )
    form = SchoolForms(request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            school_name = form.cleaned_data['school_name']
            if not School.objects.filter(school_name=school_name).exists():
                form.save()
            return redirect("/historical/create_institution")
    context = {"form": form, "name_of_school": data}
    return render(request, "create_school.html", context)


# View for the update of a school
# To-Do
# work on the form.is_valid for Foreign Key and allow update of district
def update_institution(request, code=None):
    school_to_update = get_object_or_404(School, pk=code)
    if request.method == 'POST':
        form = SchoolForms(request.POST)
        if not form.is_valid():
            school_to_update.school_name = form.cleaned_data['school_name']
            school_to_update.school_code = form.cleaned_data['school_code']
            school_to_update.category_of_school = form.cleaned_data['category_of_school']
            school_to_update.updated_at = date.today().strftime("%Y-%m-%d")
            school_to_update.updated_by = request.user.username
            school_to_update.save()
        return redirect("/historical/create_institution")
    return render(request, 'edit_school.html', {'school_to_update': school_to_update})


# Enrollment by grade and sex
def enrollment(request):
    data = Enrollment.objects.all()
    districts_names = District.objects.values('district_code', 'district_name')
    instance = Enrollment(
        created_by=request.user.username,
        updated_by=request.user.username
    )
    form = EnrollmentForms(request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            school = form.cleaned_data['school']
            grade = form.cleaned_data['grade']
            sex = form.cleaned_data['sex']
            year = form.cleaned_data['year']
            if not Enrollment.objects.filter(school=school,
                                             grade=grade,
                                             sex=sex,
                                             year=year).exists():
                form.save()
            return redirect("/historical/enrollment")
    context = {"form": form, "district_names": districts_names, "name_of_school": data}
    return render(request, "enrollment.html", context)


# update enrollment by grade and sex
def update_enrollment(request, code=None):
    school_to_update = get_object_or_404(Enrollment, pk=code)
    if request.method == 'POST':
        form = EnrollmentForms(request.POST)
        if not form.is_valid():
            school_to_update.grade = form.cleaned_data['grade']
            school_to_update.enrollment = form.cleaned_data['enrollment']
            school_to_update.sex = form.cleaned_data['sex']
            school_to_update.minimum_age = form.cleaned_data['minimum_age']
            school_to_update.maximum_age = form.cleaned_data['maximum_age']
            school_to_update.updated_at = date.today().strftime("%Y-%m-%d")
            school_to_update.updated_by = request.user.username
            school_to_update.save()
        return redirect("/historical/enrollment")
    return render(request, 'edit_enrollment.html', {'school_to_update': school_to_update})


# This function controls the total enrollment and school capacity form

def enroll_class(request):
    data = AggregateEnrollment.objects.all()
    instance = AggregateEnrollment(
        created_by=request.user.username,
        updated_by=request.user.username
    )
    form = AggregateEnrollmentForms(request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            name_of_school = form.cleaned_data['name_of_school']
            academic_year = form.cleaned_data['academic_year']
            if not AggregateEnrollment.objects.filter(name_of_school=name_of_school,
                                                      academic_year=academic_year).exists():
                form.save()
            return redirect("/historical/enroll_class")
    context = {"form": form, "name_of_school": data}
    return render(request, "enroll_class.html", context)


# used to update the enrollment versus class capacity entries
def update_enroll_class(request, code=None):
    school_to_update = get_object_or_404(AggregateEnrollment, pk=code)
    if request.method == 'POST':
        form = AggregateEnrollmentForms(request.POST)
        if not form.is_valid():
            school_to_update.academic_year = form.cleaned_data['academic_year']
            school_to_update.capacity_of_school = form.cleaned_data['capacity_of_school']
            school_to_update.total_enrollment = form.cleaned_data['total_enrollment']
            school_to_update.minimum_age = form.cleaned_data['minimum_age']
            school_to_update.maximum_age = form.cleaned_data['maximum_age']
            school_to_update.updated_at = date.today().strftime("%Y-%m-%d")
            school_to_update.updated_by = request.user.username
            school_to_update.save()
        return redirect("/historical/enroll_class")
    return render(request, 'update_enroll_class.html', {'school_to_update': school_to_update})


# change this to get a form to select the district and pass it as a parameter to present filter the table and present
# the data for each district
def enrolled_district(request):
    error_message = None

    districts_names = District.objects.values('id', 'district_name')

    if len(districts_names) > 0:
        if request.method == 'POST':
            district_selected = request.POST.get('district_name', False)
            if not district_selected:
                error_message = "Please select a chart type and school"
            else:
                if district_selected is not False:
                    data = AggregateEnrollment.objects.all().filter(district_of_school_id=district_selected)
                stu = {
                    "error_message": error_message,
                    "districts_names": districts_names,
                    "district_selected": district_selected,
                    "data": data,
                }
                return render(request, 'enrolled_district.html', stu)
        else:
            return render(request, 'enrolled_district.html', {"districts_names": districts_names})


def district_trend(request):
    error_message = None
    graph = None
    districts_lists = District.objects.values('district_code', 'district_name')
    schools = School.objects.values('id', 'school_name')

    if len(schools) > 0:
        if request.method == 'POST':
            chart = request.POST.get('chart', False)
            selected_school = request.POST.get('school_name', None)
            if not chart:
                if not selected_school:
                    error_message = "Please select a chart type and school"
            else:
                if chart is not False:
                    if selected_school is not None:
                        select_school_df = pd.DataFrame(AggregateEnrollment.objects.all().
                                                        filter(name_of_school=selected_school).values())
                        select_school_df.sort_values(by=['academic_year'], inplace=True)
                        select_school_df = select_school_df.tail(10)
                        # function to get the graph
                        graph = get_plot(chart, z=select_school_df['capacity_of_school'],
                                         y=select_school_df['total_enrollment'],
                                         x=select_school_df['academic_year'],
                                         data=select_school_df,
                                         # change this to reflect the name of the school
                                         name_of_school=selected_school)
    else:
        error_message = "No records found"

    stu = {
        "graph": graph,
        "error_message": error_message,
        "schools": schools,
        "districts_lists": districts_lists,

    }
    return render(request, 'district_trend.html', stu)


def compare_trends(request):
    error_message = None
    graph = None
    district_df = District.objects.values('id', 'district_name')
    year_df = pd.DataFrame(AggregateEnrollment.objects.values('academic_year'))
    year_list = year_df['academic_year'].unique()
    if len(district_df) > 0:
        if request.method == 'POST':
            selected_district = request.POST.get('district_name', False)
            year = request.POST.get('year', False)
            if not selected_district:
                if not year:
                    error_message = "Please select a chart type and school"
            else:
                if selected_district is not False:
                    if year is not False:
                        aggregate_df = pd.DataFrame(AggregateEnrollment.objects.all().
                                                    filter(district_of_school=selected_district,
                                                           academic_year=year).values())
                        schools_df = pd.DataFrame(School.objects.all().values())
                        df = pd.merge(left=aggregate_df, right=schools_df,
                                      left_on='name_of_school_id', right_on='id')
                        # function to get the graph
                        graph = get_pairs(x=df['total_enrollment'],
                                          y=df['capacity_of_school'],
                                          data=df,
                                          academic_year=year,
                                          district_name=selected_district,
                                          name_of_school=df['school_name'])
    else:
        error_message = "No records found"

    stu = {
        "graph": graph,
        "error_message": error_message,
        "districts_lists": district_df,
        "year_list": year_list,

    }
    return render(request, 'compare_trends.html', stu)


def district_grade(request):
    error_message = None
    districts_names = District.objects.values('id', 'district_name')

    if len(districts_names) > 0:
        if request.method == 'POST':
            district_selected = request.POST.get('district_name', False)
            if not district_selected:
                error_message = "Please select a chart type and school"
            else:
                if district_selected is not False:
                    data = Enrollment.objects.all().filter(district_id=district_selected)
                stu = {
                    "error_message": error_message,
                    "districts_names": districts_names,
                    "district_selected": district_selected,
                    "data": data,
                }
                return render(request, 'district_grade.html', stu)
        else:
            return render(request, 'district_grade.html', {"districts_names": districts_names})


def district_grade_school(request):
    error_message = None
    graph = None
    schools = School.objects.values('id', 'school_name')
    year_list = Enrollment.objects.distinct().values_list('year', flat=True)
    if len(schools) > 0:
        if request.method == 'POST':
            selected_school = request.POST.get('school_name', None)
            selected_year = request.POST.get('year', None)
            if not selected_school and not selected_year:
                error_message = "Please select a school and an academic year"
            else:
                enrollment_df = pd.DataFrame(Enrollment.objects.values().filter(school=selected_school,
                                                                                year=selected_year))
                enrollment_df.sort_values(by='sex', inplace=True)
                if enrollment_df.empty:
                    error_message = "No record was found for the selected school in the selected year"
                else:

                    # function to get the graph
                    graph = get_grade_plot(x=enrollment_df['enrollment'],
                                           z=enrollment_df['grade'],
                                           data=enrollment_df,
                                           academic_year=selected_year,
                                           name_of_school=selected_school)
    else:
        error_message = "No records found"

    stu = {
        "graph": graph,
        "error_message": error_message,
        "schools": schools,
        "year_list": year_list,

    }
    return render(request, 'district_grade_school.html', stu)


def district_category_school(request):
    error_message = None
    district_df = District.objects.values('id', 'district_name')
    year_list = Enrollment.objects.distinct().values('year')
    grade_list = Enrollment.objects.distinct().values('grade')
    if request.method == 'POST':
        selected_district = request.POST.get('district_name', False)
        selected_year = request.POST.get('year', False)
        selected_grade = request.POST.get('grade', False)
        if not selected_district or not selected_grade or not selected_year:
            error_message = "Please select a chart type and school"
        else:
            enrollment_grade_df = pd.DataFrame(Enrollment.objects.all().filter(grade=selected_grade,
                                                                               year=selected_year,
                                                                               district=selected_district).values())
            if enrollment_grade_df.empty:
                error_message = "No data found"

            else:
                schools_df = pd.DataFrame(School.objects.all().values())
                df = pd.merge(left=enrollment_grade_df, right=schools_df,
                              left_on='school_id', right_on='id')
                enrollment_grade_df.sort_values(by='sex', inplace=True)

                # function to get the graph
                # function to get the graph
                graph = get_district_grade_plot(x=df['enrollment'],
                                                z=selected_grade,
                                                data=df,
                                                academic_year=selected_year,
                                                name_of_school=df['school_name'],
                                                district=selected_district)
                stu = {
                    "graph": graph,
                    "error_message": error_message,
                    "district_list": district_df,
                    "year_list": year_list,
                    "grade_list": grade_list,

                }
                return render(request, 'district_category_school.html', stu)
    dat = {
        "error_message": error_message,
        "district_list": district_df,
        "year_list": year_list,
        "grade_list": grade_list,

    }

    return render(request, 'district_category_school.html', dat)


def nationalgenderenrollment(request):
    data = NationalGenderEnrollment.objects.all()
    instance = NationalGenderEnrollment(
        created_by=request.user.username,
        updated_by=request.user.username
    )
    form = NationalGenderEnrollmentForms(request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            academic_year = form.cleaned_data['academic_year']
            sex = form.cleaned_data['sex']
            category_of_school = form.cleaned_data['category_of_school']
            if not NationalGenderEnrollment.objects.filter(academic_year=academic_year,
                                                           sex=sex,
                                                           category_of_school=category_of_school).exists():
                form.save()
            return redirect("/historical/national_gender_enrollment")
    context = {"form": form, "name_of_school": data}
    return render(request, "national_gender.html", context)


def update_national_gender(request, code=None):
    data_to_update = get_object_or_404(NationalGenderEnrollment, pk=code)
    if request.method == 'POST':
        form = NationalGenderEnrollmentForms(request.POST)
        if not form.is_valid():
            data_to_update.academic_year = form.cleaned_data['academic_year']
            data_to_update.sex = request.POST.get('sex', False)
            # data_to_update.sex = form.cleaned_data[ request.POST.get('sex', False)]
            data_to_update.enrollment = form.cleaned_data['enrollment']
            data_to_update.category_of_school = form.cleaned_data['category_of_school']
            data_to_update.updated_at = date.today().strftime("%Y-%m-%d")
            data_to_update.updated_by = request.user.username
            data_to_update.save()
        return redirect("/historical/national_gender_enrollment")
    return render(request, 'update_national_gender.html', {'data_to_update': data_to_update})


def national_education_census(request):
    data = NationalEducationCensus.objects.all()
    instance = NationalEducationCensus(
        created_by=request.user.username,
        updated_by=request.user.username
    )
    form = NationalEducationCensusForms(request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            academic_year = form.cleaned_data['academic_year']
            if not NationalEducationCensus.objects.filter(academic_year=academic_year).exists():
                form.save()
            return redirect("/historical/national_education_census")
    context = {"form": form, "census_data": data}
    return render(request, "national_education_census.html", context)


def update_national_census(request, code=None):
    data_to_update = get_object_or_404(NationalEducationCensus, pk=code)
    if request.method == 'POST':
        form = NationalEducationCensusForms(request.POST)
        if not form.is_valid():
            data_to_update.academic_year = form.cleaned_data['academic_year']
            data_to_update.age_3_to_4_years = request.POST.get('age_3_to_4', False)
            data_to_update.age_5_to_11_years = request.POST.get('age_5_to_11', False)
            data_to_update.age_12_to_16_years = request.POST.get('age_12_to_16', False)
            data_to_update.updated_at = date.today().strftime("%Y-%m-%d")
            data_to_update.updated_by = request.user.username
            data_to_update.save()
        return redirect("/historical/national_education_census")
    return render(request, 'update_national_census.html', {'data_to_update': data_to_update})


def national_education_expenditure(request):
    data = NationalExpenditure.objects.all()
    instance = NationalExpenditure(
        created_by=request.user.username,
        updated_by=request.user.username
    )
    form = NationalExpenditureForms(request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            academic_year = form.cleaned_data['academic_year']
            if not NationalExpenditure.objects.filter(academic_year=academic_year).exists():
                form.save()
            return redirect("/historical/national_education_expenditure")
    context = {"form": form, "expenditure_data": data}
    return render(request, "national_education_expenditure.html", context)


def update_national_expenditure(request, code=None):
    data_to_update = get_object_or_404(NationalExpenditure, pk=code)
    if request.method == 'POST':
        form = NationalExpenditureForms(request.POST)
        if not form.is_valid():
            data_to_update.academic_year = form.cleaned_data['academic_year']
            data_to_update.educational_expenditure = request.POST.get('educational_expenditure', False)
            data_to_update.gdp_millions = request.POST.get('gdp_millions', False)
            data_to_update.government_expenditure = request.POST.get('government_expenditure', False)
            data_to_update.primary_school_expenditure = request.POST.get('primary_school_expenditure', False)
            data_to_update.secondary_school_expenditure = request.POST.get('secondary_school_expenditure', False)
            data_to_update.updated_at = date.today().strftime("%Y-%m-%d")
            data_to_update.updated_by = request.user.username
            data_to_update.save()
        return redirect("/historical/national_education_expenditure")
    return render(request, 'update_national_expenditure.html', {'data_to_update': data_to_update})


def national_teacher_ratio(request):
    data = NationalStudentTeacherRatio.objects.all()
    instance = NationalStudentTeacherRatio(
        created_by=request.user.username,
        updated_by=request.user.username
    )
    form = NationalTeachersRatioForms(request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            academic_year = form.cleaned_data['academic_year']
            category_of_school = form.cleaned_data['category_of_school']
            if not NationalStudentTeacherRatio.objects.filter(academic_year=academic_year,
                                                              category_of_school=category_of_school).exists():
                form.save()
            return redirect("/historical/national_teacher_ratio")
    context = {"form": form, "ratio_data": data}
    return render(request, "national_teacher_ratio.html", context)


def update_national_teacher_ratio(request, code=None):
    data_to_update = get_object_or_404(NationalStudentTeacherRatio, pk=code)
    if request.method == 'POST':
        form = NationalTeachersRatioForms(request.POST)
        if not form.is_valid():
            data_to_update.academic_year = form.cleaned_data['academic_year']
            data_to_update.total_enrollment = request.POST.get('total_enrollment', False)
            data_to_update.number_of_trained_male_teachers = request.POST.get('number_of_trained_male_teachers', False)
            data_to_update.number_of_trained_female_teachers = request.POST.get('number_of_trained_female_teachers',
                                                                                False)
            data_to_update.number_of_untrained_male_teachers = request.POST.get('number_of_untrained_male_teachers',
                                                                                False)
            data_to_update.number_of_untrained_female_teachers = request.POST.get('number_of_untrained_female_teachers',
                                                                                  False)
            data_to_update.total_number_of_teachers = request.POST.get('total_number_of_teachers', False)
            data_to_update.updated_at = date.today().strftime("%Y-%m-%d")
            data_to_update.updated_by = request.user.username
            data_to_update.save()
        return redirect("/historical/national_teacher_ratio")
    return render(request, 'update_national_teacher_ratio.html', {'data_to_update': data_to_update})


def enrollment_summary(request):
    enrollments = pd.DataFrame(NationalGenderEnrollment.objects.values().all())
    census = pd.DataFrame(NationalEducationCensus.objects.
                          values('academic_year', 'age_5_to_11_years', 'age_12_to_16_years').all())
    df = pd.merge(left=enrollments, right=census, on='academic_year')
    json_records = df.reset_index().to_json(orient='records')
    data = json.loads(json_records)
    context = {'d': data}
    if 'ger_primary' in request.POST:
        df1 = df.query("sex=='male' and category_of_school == 'primary'")
        data_boys_1 = df1[['academic_year', 'sex', 'enrollment', 'age_5_to_11_years']]
        json_records = data_boys_1.reset_index().to_json(orient='records')
        data_boys_primary = json.loads(json_records)
        # function to get the graph
        graph_boys_primary = get_plot_boys_primary(data=data_boys_1)

        df2 = df.query("sex=='female' and category_of_school == 'primary'")
        data_girls_1 = df2[['academic_year', 'sex', 'enrollment', 'age_5_to_11_years']]
        json_records = data_girls_1.reset_index().to_json(orient='records')
        data_girls_primary = json.loads(json_records)
        # function to get the graph
        graph_girls_primary = get_plot_girls_primary(data=data_girls_1)

        df3 = df.query("category_of_school == 'primary'")
        data_both_primary = df3[['academic_year', 'sex', 'enrollment', 'age_5_to_11_years']]
        json_records = data_both_primary.reset_index().to_json(orient='records')
        all_data_primary = json.loads(json_records)
        graph_all_primary = get_plot_primary(data=data_both_primary,
                                             data_boys=data_boys_1,
                                             data_girls=data_girls_1)
        data_all_primary = {'d_boys': data_boys_primary,
                            'd_primary': all_data_primary,
                            'd_girls_primary': data_girls_primary,
                            'graph_boys_primary': graph_boys_primary,
                            'graph_all_primary': graph_all_primary,
                            'graph_girls_primary': graph_girls_primary}
        return render(request, 'ger.html', data_all_primary)
    if 'ger_secondary' in request.POST:
        df1 = df.query("sex=='male' and category_of_school == 'secondary'")
        data_boys_1 = df1[['academic_year', 'sex', 'enrollment', 'age_12_to_16_years']]
        json_records = data_boys_1.reset_index().to_json(orient='records')
        data_boys_secondary = json.loads(json_records)
        # function to get the graph
        graph_boys_secondary = get_plot_boys_secondary(data=data_boys_1)

        df2 = df.query("sex=='female' and category_of_school == 'secondary'")
        data_girls_1 = df2[['academic_year', 'sex', 'enrollment', 'age_12_to_16_years']]
        json_records = data_girls_1.reset_index().to_json(orient='records')
        data_girls_secondary = json.loads(json_records)
        # function to get the graph
        graph_girls_secondary = get_plot_girls_secondary(data=data_girls_1)

        df3 = df.query("category_of_school == 'secondary'")
        data_both_secondary = df3[['academic_year', 'sex', 'enrollment', 'age_12_to_16_years']]
        json_records = data_both_secondary.reset_index().to_json(orient='records')
        all_data_secondary = json.loads(json_records)
        graph_all_secondary = get_plot_secondary(data=data_both_secondary,
                                                 data_boys=data_boys_1,
                                                 data_girls=data_girls_1)
        data_all_secondary = {'d_boys': data_boys_secondary,
                              'd_secondary': all_data_secondary,
                              'd_girls_secondary': data_girls_secondary,
                              'graph_boys_secondary': graph_boys_secondary,
                              'graph_all_secondary': graph_all_secondary,
                              'graph_girls_secondary': graph_girls_secondary}
        return render(request, 'ger_secondary.html', data_all_secondary)
    if 'ger_gdp' in request.POST:
        expenditure = pd.DataFrame(NationalExpenditure.objects.
                                   values('academic_year', 'gdp_millions').all())
        df_regression = pd.merge(left=df, right=expenditure, on='academic_year')
        json_records = df_regression.reset_index().to_json(orient='records')
        data_regression = json.loads(json_records)

        df1 = df_regression.query("sex=='male' and category_of_school == 'primary'")
        data_boys_1 = df1[['academic_year', 'sex', 'enrollment', 'age_5_to_11_years', 'gdp_millions']]
        data_boys_1 = data_boys_1[(data_boys_1[['age_5_to_11_years', 'gdp_millions']] != 0).all(axis=1)]
        data_boys_1['ger'] = (data_boys_1['enrollment'] / data_boys_1['age_5_to_11_years']) * 100
        data_boys_1['ger'] = data_boys_1['ger'].replace(np.inf, 0)
        data_boys_1['ger'].astype(float)
        json_records = data_boys_1.reset_index().to_json(orient='records')
        data_boys_primary = json.loads(json_records)

        df2 = df_regression.query("sex=='female' and category_of_school == 'primary'")
        data_girls_1 = df2[['academic_year', 'sex', 'enrollment', 'age_5_to_11_years', 'gdp_millions']]
        json_records = data_girls_1.reset_index().to_json(orient='records')
        data_girls_primary = json.loads(json_records)

        df1 = df_regression.query("sex=='male' and category_of_school == 'secondary'")
        data_boys_1_secondary = df1[['academic_year', 'sex', 'enrollment', 'age_12_to_16_years', 'gdp_millions']]
        json_records = data_boys_1_secondary.reset_index().to_json(orient='records')
        data_boys_secondary = json.loads(json_records)
        # function to get the graph

        df2 = df_regression.query("sex=='female' and category_of_school == 'secondary'")
        data_girls_1_secondary = df2[['academic_year', 'sex', 'enrollment', 'age_12_to_16_years', 'gdp_millions']]
        json_records = data_girls_1_secondary.reset_index().to_json(orient='records')
        data_girls_secondary = json.loads(json_records)
        # function to get the graph

        graph_all = get_plot_regression(data=df_regression,
                                        data_boys_primary=data_boys_1,
                                        data_girls_primary=data_girls_1,
                                        data_boys_secondary=data_boys_1_secondary,
                                        data_girls_secondary=data_girls_1_secondary
                                        )
        context = {'d_boys': data_boys_primary,
                   'd': data_regression,
                   'd_girls_primary': data_girls_primary,
                   'd_girls_secondary': data_girls_secondary,
                   'd_boys_primary': data_boys_secondary,
                   'd_boys_secondary': data_girls_secondary,
                   'graph_all': graph_all
                   }

        return render(request, 'ger_regression.html', context)

    return render(request, 'enrollment_summary.html', context)


def special_ed_quest(request):
    form1 = SpecialEdForms1(request.GET)
    form2 = SpecialEdForms2(request.GET)
    form3 = SpecialEdForms3(request.GET)
    form4 = SpecialEdForms4(request.GET)

    data_forms = {
        "form1": form1,
        "form2": form2,
        "form3": form3,
        "form4": form4,

    }

    return render(request, 'special_ed_quest.html', data_forms)


#==============================================
#View for outlier detection at district level
#==============================================

def outlier_district(request):
    #return HttpResponse('In outlier detection at district level')

    error_message = None
    graph = None

    districts_names = District.objects.values('id', 'district_name')
    year_list = Enrollment.objects.distinct().values_list('year', flat=True)
    school_categories = Enrollment.objects.distinct().values_list('category_of_school', flat=True)

    if (len(districts_names) > 0 and len(school_categories)> 0):
        if ((request.method) == 'POST'):

            district_selected  = request.POST.get('district_name', None)
            selected_year = request.POST.get('year', None)
            selected_school_type = request.POST.get('school_type', None)

            if (not district_selected or not selected_year or not selected_school_type):
                error_message = "Please select all variables"
            else:
                #enrollment_df = pd.DataFrame(AggregateEnrollment.objects.values().filter(district_of_school=district_selected, academic_year = selected_year))
                enrollment_df = pd.DataFrame(AggregateEnrollment.objects.all().filter(category_of_school = selected_school_type,
                                                                                      district_of_school=district_selected, 
                                                                                      academic_year=selected_year).values())

                if (enrollment_df.empty):
                    error_message = "No record was found for the selected district and academic year"

                else:

                    schools_df = pd.DataFrame(School.objects.all().values())
                    final_df = pd.merge(left = enrollment_df, right = schools_df,
                                        left_on='name_of_school_id', right_on='id')
                    
                    enrollment_mean = final_df['total_enrollment'].mean()
                    
                    enrollment_median = final_df['total_enrollment'].median()

                    mean_list = []
                    
                    x = range(0,len(final_df['school_name']))

                    for a in x:
                        mean_list.append(enrollment_mean)

                    data_mean = pd.DataFrame(mean_list, columns=['Mean'])

                    graph = get_outlier_district_plot(x=final_df['total_enrollment'],
                                                      y = final_df['school_name'],
                                                      data = final_df,
                                                      academic_year = selected_year,
                                                      data_mean  = data_mean,   
                                                      input_school_type = selected_school_type, 
                                                      input_district = district_selected                             
                                                      )
    else:
        error_message = "No records found"

        
    
    stu = {
        "graph" : graph,
        "error_message" : error_message,
        "districts_name" : districts_names,
        "year_list" : year_list,
        "school_list" : school_categories

    }
    
    return render(request, 'outlier_district_page.html', stu)
    

#==============================================
#View for outlier detection at national level
#==============================================

def outlier_national(request):
    
    error_message = None
    graph = None
    selected_school_type = ''
    selected_year = ''

    year_list = Enrollment.objects.distinct().values_list('year', flat=True)
    school_categories = Enrollment.objects.distinct().values_list('category_of_school', flat=True)

    if (len(year_list) > 0 and len(school_categories) > 0):
        if ((request.method) == 'POST'):
            
            selected_school_type = request.POST.get('school_type', None)
            selected_year = request.POST.get('year', None)

            if (not selected_year or not selected_school_type):
                error_message = "Please select an academic year"
            else:
                #enrollment_df = pd.DataFrame(AggregateEnrollment.objects.values().filter(district_of_school=district_selected, academic_year = selected_year))
                enrollment_df = pd.DataFrame(AggregateEnrollment.objects.all().filter(category_of_school = selected_school_type, academic_year=selected_year).values())

                if (enrollment_df.empty):
                    error_message = "No record was found for the academic year"

                else:
                    schools_df = pd.DataFrame(School.objects.all().values())
                    final_df = pd.merge(left = enrollment_df, right = schools_df,
                                        left_on='name_of_school_id', right_on='id')
                    

                    
                    enrollment_mean = final_df['total_enrollment'].mean()
                    

                    mean_list = []
                    
                    x = range(0,len(final_df['school_name']))

                    for a in x:
                        mean_list.append(enrollment_mean)

                    data_mean = pd.DataFrame(mean_list, columns=['Mean'])
                    graph = get_outlier_national_plot(x=final_df['total_enrollment'],
                                                      y = final_df['school_name'],
                                                      data = final_df,
                                                      academic_year = selected_year,
                                                      data_mean  = data_mean, 
                                                      input_school_type = selected_school_type
                                                                                        
                                                      )
    else:
        error_message = "No records found"

       
    
    stu = {
        "graph" : graph,
        "error_message" : error_message,
        "year_list" : year_list,
        "school_list" : school_categories

    }


    return render(request, 'outlier_national_page.html', stu)


def district_performance(request):
    graph = None
    error_message = None
    districts_names = District.objects.values('id', 'district_name')
    context = {"districts_names": districts_names}

    districts_names = District.objects.values('id', 'district_name')

    if len(districts_names) > 0:
        if request.method == 'POST':
            # Compare all districts
            if request.POST['submit']=='Compare All Districts (CEE)':
                chart_title = "CEE Comparison, All Districts"
                context['chart_title'] = chart_title
                data = PrimaryPerformance.objects.all()
                [graph, heatmap] = primary_performance_plot(data, None, None)
                context['graph'] = graph
                context['heatmap'] = heatmap
                return render(request, 'district_performance.html', context)
            if request.POST['submit']=='Compare All Districts (CSEC)':
                chart_title = "CSEC Comparison, All Districts"
                context['chart_title'] = chart_title
                data = CSECResults.objects.all()
                [graph, heatmap, left_out] = csec_performance_plot(data, None, None)
                context['graph'] = graph
                context['heatmap'] = heatmap
                if len(left_out):
                    context['left_out'] = left_out
                return render(request, 'district_performance.html', context)

            # Compare CEE between 2 districts
            if request.POST['submit']=='Compare CEE Results':
                district_1 = request.POST.get('district_1_name', False)
                district_2 = request.POST.get('district_2_name', False)
                if not (district_1 and district_2) or district_1 == district_2:
                    error_message = "Please select 2 different districts to compare."
                    context['error_message'] = error_message
                    return render(request, 'district_performance.html', context)
                if request.POST['submit']=='Compare CEE Results':
                    chart_title = "CEE Comparison, Districts " + district_1 + " and " + district_2
                    context['chart_title'] = chart_title
                    data = PrimaryPerformance.objects.all()
                    [graph, heatmap] = primary_performance_plot(data, int(district_1), int(district_2))
                    context['graph'] = graph
                    context['heatmap'] = heatmap
                    return render(request, 'district_performance.html', context)

            # Compare CSEC between 2 districts
            district_3 = request.POST.get('district_3_name', False)
            district_4 = request.POST.get('district_4_name', False)
            if not (district_3 and district_4) or district_3 == district_4:
                error_message = "Please select 2 different districts to compare."
                context['error_message'] = error_message
                return render(request, 'district_performance.html', context)
            if request.POST['submit']=='Compare CSEC Results':
                chart_title = "CSEC Comparison, Districts " + district_3 + " and " + district_4
                context['chart_title'] = chart_title
                data = CSECResults.objects.all()
                [graph, heatmap, left_out] = csec_performance_plot(data, int(district_3), int(district_4))
                context['graph'] = graph
                context['heatmap'] = heatmap
                if len(left_out):
                    context['left_out'] = left_out
                return render(request, 'district_performance.html', context)
        else:
            return render(request, 'district_performance.html', context)

UNIVERSAL_FIELDS = {'id', 'created_at', 'created_by', 'updated_at', 'updated_by'}

def upload_scores(request):
    context = {}
    cee_field_names = CEEResults._meta.get_fields()
    cee_field_names = [str(f).split('.')[-1] for f in cee_field_names] 
    cee_field_names = list(set(cee_field_names) - UNIVERSAL_FIELDS)
    cee_field_names.sort()

    csec_field_names = CSECResults._meta.get_fields()
    csec_field_names = [str(f).split('.')[-1] for f in csec_field_names] 
    csec_field_names = list(set(csec_field_names) - UNIVERSAL_FIELDS)
    csec_field_names.sort()
    context['cee_field_names'] = cee_field_names
    context['csec_field_names'] = csec_field_names

    context['cee_count'] = CEEResults.objects.count()
    context['csec_count'] = CSECResults.objects.count()
    context['cee_by_year'] = [item['test_yr'] for item in CEEResults.objects.values('test_yr').distinct()]
    context['csec_by_year'] = [item['EXAM_PERIOD'] for item in CSECResults.objects.values('EXAM_PERIOD').distinct()]

    if "GET" == request.method:
        return render(request, "upload_scores.html", context)
    type = "CEE"
    field_names = []
    csv_file = None
    if request.POST['submit']=='Upload CSEC Scores':
        field_names = csec_field_names
        if not "csec_file" in request.FILES:
            context['error_message'] = 'Please select a file to upload.'
            return render(request, "upload_scores.html", context)
        csv_file = request.FILES["csec_file"]
        type = "CSEC"
    elif request.POST['submit']=='Upload CEE Scores':
        field_names = cee_field_names
        if not "cee_file" in request.FILES:
            context['error_message'] = 'Please select a file to upload.'
            return render(request, "upload_scores.html", context)
        csv_file = request.FILES["cee_file"]


    if request.POST['submit'].startswith("delete_cee"):
        time_period = request.POST['submit'][10:]
        CEEResults.objects.filter(test_yr=time_period).delete()
    elif request.POST['submit'].startswith("delete_csec"):
        time_period = request.POST['submit'][10:]
        CSECResults.objects.filter(EXAM_PERIOD=time_period).delete()
    else:
        if not csv_file.name.endswith('.csv'):
            context['error_message'] = 'Could not upload file. File must be CSV type.'
            return render(request, "upload_scores.html", context)
        scores = csv_file.read().decode("utf-8", 'ignore')
        user_data = {'created_by': request.user.username,
                    'updated_by': request.user.username,
                    'created_at': date.today().strftime("%Y-%m-%d"),
                    'updated_at': date.today().strftime("%Y-%m-%d")}
        result = store_scores(scores, field_names, user_data, type)
        if 'error_message' in result:
            context['error_message'] = result['error_message']
        if 'missing_fields' in result:
            context['missing_fields'] = result['missing_fields']
        n_scores = 0
        if 'n_scores' in result:
            context['n_scores'] = result['n_scores']
        if 'failed' in result:
            context['failed'] = result['failed']


    context['cee_count'] = CEEResults.objects.count()
    context['csec_count'] = CSECResults.objects.count()
    context['cee_by_year'] = [item['test_yr'] for item in CEEResults.objects.values('test_yr').distinct()]
    context['csec_by_year'] = [item['EXAM_PERIOD'] for item in CSECResults.objects.values('EXAM_PERIOD').distinct()]
    return render(request, "upload_scores.html", context)

def csec_exam(request):
    context = {}
    data = CSECResults.objects.all()
    context['graph'] = csec_summary(data)
    return render(request, "csec_exam.html", context)