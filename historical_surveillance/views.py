import datetime
from datetime import datetime
import pandas as pd
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.utils.datetime_safe import date

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


# This function controls the enrollment by school,
# grade and gender form view, processes the and submits form data to the database
# This view is a place holder and still under construction
def enrollment(request):
    form = EnrollmentForms()
    districts_names = District.objects.values('district_code', 'district_name')
    return render(request, 'enrollment.html', {'form': form, 'district_names': districts_names})


# This function controls the total enrollment and school capacity form, processes the form data and submits
# it to the database
# This view is still under construction
def enroll_class(request):
    form = AggregateEnrollmentForms()
    if request.method == 'POST':
        form = AggregateEnrollmentForms(request.POST)
        if form.is_valid():
            school_form = form.cleaned_data['name_of_school']
            academic_year_form = form.cleaned_data['academic_year']
            district_form = form.cleaned_data['district_of_school']
            if not AggregateEnrollment.objects.filter(name_of_school=school_form, academic_year=academic_year_form,
                                                      district_of_school=district_form).exists():
                form.save()
                return redirect("/")
        else:
            messages.add_message(request, messages.INFO, 'Data has been entered previously')

    return render(request, 'enroll_class.html', {'form': form})


# This view controls the enrollment / Capacity views table
def enrolled(request):
    data = AggregateEnrollment.objects.all()

    stu = {
        "name_of_school": data
    }
    return render(request, 'enrolled.html', stu)


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


# This view controls the enrollment / Capacity views table
def enrolled_grade(request):
    data = Enrollment.objects.all()

    stu = {
        "name_of_school": data
    }
    return render(request, 'enrolled_grade.html', stu)


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


def enrollment_summary(request):
    return render(request, 'enrollment_summary.html', {})


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
