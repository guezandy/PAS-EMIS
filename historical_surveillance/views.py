from historical_surveillance.tables import *
import json
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django_tables2 import RequestConfig
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.datetime_safe import date
from .forms import *
from .models import *
from .utils import *

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2.export import ExportMixin


# This is the view for the home page of this app
def index(request):
    return render(request, 'surv_home.html', {})


# This is for showing a list of all districts
class FilteredDistrictListView(ExportMixin, SingleTableMixin, FilterView):
    table_class = DistrictTable
    model = District
    template_name = "data_list.html"
    filterset_class = DistrictFilter
    table_pagination = {
        "per_page": 10
    }
    extra_context = {"listTitle": "Districts",
                     "createButtonName": "Create District",
                     "createViewName": "surveillance:create-district",
                     "export_formats": ["csv"]}


# This is for creating and editing a district
def edit_district(request, code=None):
    # Render edit form
    if code:
        instance = get_object_or_404(District, pk=code)
    # Render create form
    else:
        instance = District(created_by=request.user.username,
                            updated_by=request.user.username)
    form = DistrictForms(request.POST or None, instance=instance)
    # Process submit
    if request.method == "POST":
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.updated_by = request.user.username
            model_instance.save()
            return HttpResponseRedirect(reverse("surveillance:districts"))
    context = {
        "header": "Edit District" if code else "Create District", "form": form}
    # context = _add_side_navigation_context(request.user, context)
    return render(request, "historical_form.html", context)


# This is for showing a list of all schools
class FilteredSchoolListView(ExportMixin, SingleTableMixin, FilterView):
    table_class = SchoolTable
    model = School
    template_name = "data_list.html"
    filterset_class = SchoolFilter
    table_pagination = {
        "per_page": 10
    }
    extra_context = {"listTitle": "School",
                     "createButtonName": "Create School",
                     "createViewName": "surveillance:create-school",
                     "export_formats": ["csv"]}


# This is for creating and editing a school
def edit_school(request, code=None):
    # Render edit form
    if code:
        instance = get_object_or_404(School, pk=code)
    # Render create form
    else:
        instance = School(created_by=request.user.username,
                          updated_by=request.user.username)
    form = SchoolForms(request.POST or None, instance=instance)
    # Process submit
    if request.method == 'POST':
        form = SchoolForms(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.updated_by = request.user.username
            model_instance.save()
            return HttpResponseRedirect(reverse("surveillance:schools"))
    context = {"header": "Edit School" if code else "Create School", "form": form}
    return render(request, 'historical_form.html', context)


class FilteredEnrollmentListView(ExportMixin, SingleTableMixin, FilterView):
    table_class = EnrollmentTable
    model = Enrollment
    template_name = "data_list.html"
    filterset_class = EnrollmentFilter
    table_pagination = {
        "per_page": 10
    }
    extra_context = {"listTitle": "National Enrollment by Grade and Sex",
                     "createButtonName": "Add Record",
                     "createViewName": "surveillance:create-enrollment",
                     "export_formats": ["csv"]}


# update enrollment by grade and sex
def update_enrollment(request, code=None):
    # Render edit form
    if code:
        instance = get_object_or_404(Enrollment, pk=code)
    # Render create form
    else:
        instance = Enrollment(created_by=request.user.username,
                              updated_by=request.user.username)
    form = EnrollmentForms(request.POST or None, instance=instance)
    # Process submit
    if request.method == 'POST':
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.updated_by = request.user.username
            model_instance.save()
            return HttpResponseRedirect(reverse("surveillance:enrollments"))
    context = {
        "header": "Edit Enrollment" if code else "Add Enrollment Record", "form": form}
    return render(request, 'historical_form.html', context)


class FilteredAggregateEnrollmentListView(ExportMixin, SingleTableMixin, FilterView):
    table_class = AggregateEnrollmentTable
    model = AggregateEnrollment
    template_name = "data_list.html"
    filterset_class = AggregateEnrollmentFilter
    table_pagination = {
        "per_page": 10
    }
    extra_context = {"listTitle": "National Enrollment and School Capacity",
                     "createButtonName": "Add Record",
                     "createViewName": "surveillance:create-aggregate-enrollment",
                     "export_formats": ["csv"]}


# used to update the enrollment versus class capacity entries
def update_aggregate_enrollment(request, code=None):
    if code:
        instance = get_object_or_404(AggregateEnrollment, pk=code)
    # Render create form
    else:
        instance = AggregateEnrollment(created_by=request.user.username,
                                       updated_by=request.user.username)
    form = AggregateEnrollmentForms(request.POST or None, instance=instance)
    # Process submit
    if request.method == 'POST':
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.updated_by = request.user.username
            model_instance.save()
            return HttpResponseRedirect(reverse("surveillance:aggregate-enrollments"))
    context = {
        "header": "Edit National Enrollment and School Capacity" if code else "Add National Enrollment and School Capacity",
        "form": form}
    return render(request, 'historical_form.html', context)


class CeeListView(ExportMixin, SingleTableMixin, FilterView):
    table_class = CeeTable
    model = CEE
    template_name = "data_list.html"
    filterset_class = CeeFilter
    table_pagination = {
        "per_page": 10
    }
    extra_context = {"listTitle": "Grade 6 National Examination",
                     "createButtonName": "Add Record",
                     "createViewName": "surveillance:create-cee",
                     "export_formats": ["csv"]}


def update_cee(request, id=None):
    # Render edit form
    if id:
        instance = get_object_or_404(CEE, pk=id)
    # Render create form
    else:
        instance = CEE(created_by=request.user.username,
                       updated_by=request.user.username)
    form = ceeForms(request.POST or None, instance=instance)
    # Process submit
    if request.method == "POST":
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.updated_by = request.user.username
            model_instance.save()
            return HttpResponseRedirect(reverse("surveillance:cee-results"))
    context = {
        "header": "Edit Grade 6 National Examination" if id else "Create Grade 6 National Examination Record",
        "form": form}
    # context = _add_side_navigation_context(request.user, context)
    return render(request, "historical_form.html", context)


class CsecListView(ExportMixin, SingleTableMixin, FilterView):
    table_class = CsecTable
    model = CSEC
    template_name = "data_list.html"
    filterset_class = CsecFilter
    table_pagination = {
        "per_page": 10
    }
    extra_context = {"listTitle": "Form 5 Exit Examination",
                     "createButtonName": "Add Record",
                     "createViewName": "surveillance:create-csec",
                     "export_formats": ["csv"]}


# This is for creating and editing a csec record
def update_csec(request, id=None):
    # Render edit form
    if id:
        instance = get_object_or_404(CSEC, pk=id)
    # Render create form
    else:
        instance = CSEC(created_by=request.user.username,
                        updated_by=request.user.username)
    form = csecForms(request.POST or None, instance=instance)
    # Process submit
    if request.method == "POST":
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.updated_by = request.user.username
            model_instance.save()
            return HttpResponseRedirect(reverse("surveillance:csec-results"))
    context = {
        "header": "Edit Form 5 Exit Examination Record" if id else "Create Form 5 Exit Examination Record",
        "form": form}
    # context = _add_side_navigation_context(request.user, context)
    return render(request, "historical_form.html", context)


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
                    data = AggregateEnrollment.objects.all().filter(
                        district_of_school_id=district_selected)
                stu = {
                    "error_message": error_message,
                    "districts_names": districts_names,
                    "district_selected": district_selected,
                    "data": data,
                }
                return render(request, 'enrolled_district.html', stu)
        else:
            return render(request, 'enrolled_district.html', {"districts_names": districts_names})


# Get the trend of enrollment versus capacity for each selected school by the selected school and the type of chart
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
                        select_school_df.sort_values(
                            by=['academic_year'], inplace=True)
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


# This view present a page for comparing the trends of enrollment within schools in a select district in a select academic year
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
                        schools_df = pd.DataFrame(
                            School.objects.all().values())
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


# Get enrollment for each class in a select school for a select academic year
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

                enrollment_df_girls = pd.DataFrame(Enrollment.objects.values('year', 'grade', 'sex', 'enrollment').
                                                   filter(school=selected_school, year=selected_year, sex='female'))
                if len(enrollment_df_girls) > 0:
                    enrollment_df_girls = enrollment_df_girls
                else:
                    pass

                enrollment_df_boys = pd.DataFrame(
                    Enrollment.objects.values('grade', 'enrollment').filter(school=selected_school,
                                                                            year=selected_year,
                                                                            sex='male'))
                if len(enrollment_df_boys) > 0:
                    enrollment_df_boys = enrollment_df_boys
                else:
                    pass

                enrollment_df = pd.DataFrame(
                    Enrollment.objects.values('grade', 'enrollment').filter(school=selected_school,
                                                                            year=selected_year,
                                                                            sex=''))
                if len(enrollment_df) > 0:
                    enrollment_df = enrollment_df

                else:
                    pass

                # function to get the graph
                graph = get_grade_plot(
                    data=enrollment_df,
                    data_boys=enrollment_df_boys,
                    data_girls=enrollment_df_girls,
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
            schools_df = pd.DataFrame(School.objects.all().values())
            enrollment_grade_df_girls = pd.DataFrame(Enrollment.objects.all().filter(grade=selected_grade,
                                                                                     year=selected_year,
                                                                                     district=selected_district,
                                                                                     sex='female').values())
            enrollment_grade_df_boys = pd.DataFrame(Enrollment.objects.all().filter(grade=selected_grade,
                                                                                    year=selected_year,
                                                                                    district=selected_district,
                                                                                    sex='male').values())
            enrollment_grade_df_none = pd.DataFrame(Enrollment.objects.all().filter(grade=selected_grade,
                                                                                    year=selected_year,

                                                                                    district=selected_district,
                                                                                    sex='').values())

            if len(enrollment_grade_df_girls) > 0:
                df_girls = pd.merge(left=enrollment_grade_df_girls, right=schools_df,
                                    left_on='school_id', right_on='id')
                graph_girls = get_district_grade_plot_girls(
                    data_girls=df_girls,
                    grade=selected_grade,
                    academic_year=selected_year,
                    district=selected_district,
                    school_girls=df_girls['school_name'])

            else:
                graph_girls = "No data to display"

            if len(enrollment_grade_df_boys) > 0:
                df_boys = pd.merge(left=enrollment_grade_df_boys, right=schools_df,
                                   left_on='school_id', right_on='id')
                graph_boys = get_district_grade_plot_boys(
                    data_boys=df_boys,
                    grade=selected_grade,
                    academic_year=selected_year,
                    district=selected_district,
                    school_boys=df_boys['school_name']
                )

            else:
                graph_boys = "No data to display"
                pass

            if len(enrollment_grade_df_none) > 0:
                df_none = pd.merge(left=enrollment_grade_df_none, right=schools_df,
                                   left_on='school_id', right_on='id')
                graph = get_district_grade_plot_none(data_none=df_none,
                                                     grade=selected_grade,
                                                     academic_year=selected_year,
                                                     district=selected_district,
                                                     school_none=df_none['school_name'])

            else:
                graph = "No data to display"
                pass

                # function to get the graph

            stu = {
                "graph": graph,
                "graph_boys": graph_boys,
                "graph_girls": graph_girls,
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
    form = NationalGenderEnrollmentForms(
        request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            academic_year = request.POST.get('academic_year', False)
            sex = form.cleaned_data['sex']
            category_of_school = form.cleaned_data['category_of_school']
            if not NationalGenderEnrollment.objects.filter(academic_year=academic_year,
                                                           sex=sex,
                                                           category_of_school=category_of_school).exists():
                form.save()
            return redirect("/historical/national_gender_enrollment")
    if 'national_enrollment_trend' in request.POST:
        data = pd.DataFrame(NationalGenderEnrollment.objects.values().all())
        data_male_primary = pd.DataFrame(NationalGenderEnrollment.objects. \
                                         filter(sex='males', category_of_school='primary').all().values())

        data_male_secondary = pd.DataFrame(NationalGenderEnrollment.objects.filter(sex='males',
                                                                                   category_of_school='secondary'). \
                                           all().values())

        data_female_primary = pd.DataFrame(NationalGenderEnrollment.objects.filter(sex='females',
                                                                                   category_of_school='primary'). \
                                           all().values())

        data_female_secondary = pd.DataFrame(NationalGenderEnrollment.objects.filter(sex='females',
                                                                                     category_of_school='secondary'). \
                                             all().values())

        # function to get the graph

        graph_all = plot_national_gender_enrollment(
            data_boys_primary=data_male_primary,
            data_girls_primary=data_female_primary,
            data_boys_secondary=data_male_secondary,
            data_girls_secondary=data_female_secondary
        )
        graph_hist = national_gender_enrollment_hist(
            data=data,
            data_boys_primary=data_male_primary,
            data_girls_primary=data_female_primary,
            data_boys_secondary=data_male_secondary,
            data_girls_secondary=data_female_secondary

        )
        graph_all = {
            "graph": graph_all,
            'data': data,
            'data_boys_primary': data_male_primary,
            'data_girls_primary': data_female_primary,
            'data_boys_secondary': data_male_secondary,
            'data_girls_secondary': data_female_secondary,
            'graph_hist': graph_hist,
        }

        return render(request, "national_gender_enrollment_trend.html", graph_all)
    context = {"form": form, "name_of_school": data}
    return render(request, "national_gender.html", context)


def update_national_gender(request, code=None):
    data_to_update = get_object_or_404(NationalGenderEnrollment, pk=code)
    if request.method == 'POST':
        form = NationalGenderEnrollmentForms(request.POST)
        if not form.is_valid():
            data_to_update.academic_year = request.POST.get('academic_year', False)
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
    form = NationalEducationCensusForms(
        request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            academic_year = form.cleaned_data['academic_year']
            if not NationalEducationCensus.objects.filter(academic_year=academic_year).exists():
                form.save()
            return redirect("/historical/national_education_census")
    if 'national_census_trend' in request.POST:
        data = pd.DataFrame(NationalEducationCensus.objects.values().all())
        # function to get the graph

        graph_all = plot_national_education_census(data=data)
        graph_hist = national_education_census_hist(data=data)
        graph_all = {
            "graph": graph_all,
            'data': data,
            'graph_hist': graph_hist,
        }

        return render(request, "national_education_census_trend.html", graph_all)
    context = {"form": form, "census_data": data}
    return render(request, "national_education_census.html", context)


def update_national_census(request, code=None):
    data_to_update = get_object_or_404(NationalEducationCensus, pk=code)
    if request.method == 'POST':
        form = NationalEducationCensusForms(request.POST)
        if not form.is_valid():
            data_to_update.academic_year = request.POST.get('academic_year', False)
            data_to_update.age_3_to_4_years = request.POST.get(
                'age_3_to_4', False)
            data_to_update.age_5_to_11_years = request.POST.get(
                'age_5_to_11', False)
            data_to_update.age_12_to_16_years = request.POST.get(
                'age_12_to_16', False)
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
            academic_year = request.POST.get('academic_year', False)
            if not NationalExpenditure.objects.filter(academic_year=academic_year).exists():
                form.save()
            return redirect("/historical/national_education_expenditure")

    if 'national_expenditure_trend' in request.POST:
        data = pd.DataFrame(NationalExpenditure.objects.values().all())
        # function to get the graph
        graph_all = plot_national_expenditure(data=data)
        graph_hist = national_expenditure_hist(data=data)
        graph_all = {
            "graph": graph_all,
            'data': data,
            'graph_hist': graph_hist,
        }

        return render(request, "national_expenditure_trend.html", graph_all)
    context = {"form": form, "expenditure_data": data}
    return render(request, "national_education_expenditure.html", context)


def update_national_expenditure(request, code=None):
    data_to_update = get_object_or_404(NationalExpenditure, pk=code)
    if request.method == 'POST':
        form = NationalExpenditureForms(request.POST)
        if not form.is_valid():
            data_to_update.academic_year = request.POST.get('academic_year', False)
            data_to_update.educational_expenditure = request.POST.get(
                'educational_expenditure', False)
            data_to_update.gdp_millions = request.POST.get(
                'gdp_millions', False)
            data_to_update.government_expenditure = request.POST.get(
                'government_expenditure', False)
            data_to_update.primary_school_expenditure = request.POST.get(
                'primary_school_expenditure', False)
            data_to_update.secondary_school_expenditure = request.POST.get(
                'secondary_school_expenditure', False)
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
            academic_year = request.POST.get('academic_year', False)
            category_of_school = form.cleaned_data['category_of_school']
            if not NationalStudentTeacherRatio.objects.filter(academic_year=academic_year,
                                                              category_of_school=category_of_school).exists():
                form.save()
            return redirect("/historical/national_teacher_ratio")

        if 'national_ratio_trend' in request.POST:
            data = pd.DataFrame(
                NationalStudentTeacherRatio.objects.values().all())
            data_primary = pd.DataFrame(
                NationalStudentTeacherRatio.objects.filter(category_of_school='primary').values().all())
            data_secondary = pd.DataFrame(
                NationalStudentTeacherRatio.objects.filter(category_of_school='secondary').values().all())

            # function to get the graph
            # for _ in range(data[data.columns[0]].count()):
            graph_primary = plot_national_ratio_trend_primary(data_primary=data_primary)

            graph_secondary = plot_national_ratio_trend(data_secondary=data_secondary)
            graph_hist = national_ratio_hist(data=data)
            graph_all = {
                "graph": graph_secondary,
                "graph_primary": graph_primary,
                "graph_secondary": graph_secondary,
                'data_primary': data_primary,
                'data_secondary': data_secondary,
                'graph_hist': graph_hist,

            }

        return render(request, "national_teacher_student_ratio.html", graph_all)

    context = {"form": form, "ratio_data": data}
    return render(request, "national_teacher_ratio.html", context)


def update_national_teacher_ratio(request, code=None):
    data_to_update = get_object_or_404(NationalStudentTeacherRatio, pk=code)
    if request.method == 'POST':
        form = NationalTeachersRatioForms(request.POST)
        if not form.is_valid():
            data_to_update.academic_year = request.POST.get('academic_year', False)
            data_to_update.total_enrollment = request.POST.get(
                'total_enrollment', False)
            data_to_update.number_of_trained_male_teachers = request.POST.get(
                'number_of_trained_male_teachers', False)
            data_to_update.number_of_trained_female_teachers = request.POST.get('number_of_trained_female_teachers',
                                                                                False)
            data_to_update.number_of_untrained_male_teachers = request.POST.get('number_of_untrained_male_teachers',
                                                                                False)
            data_to_update.number_of_untrained_female_teachers = request.POST.get('number_of_untrained_female_teachers',
                                                                                  False)
            data_to_update.total_number_of_teachers = request.POST.get(
                'total_number_of_teachers', False)
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
        data_boys_1 = df.query("sex=='males' and category_of_school == 'primary'")
        json_records = data_boys_1.reset_index().to_json(orient='records')
        data_boys_primary = json.loads(json_records)
        # function to get the graph
        graph_boys_primary = get_plot_boys_primary(data=data_boys_1)

        data_girls_1 = df.query("sex=='females' and category_of_school == 'primary'")
        json_records = data_girls_1.reset_index().to_json(orient='records')
        data_girls_primary = json.loads(json_records)
        # function to get the graph
        graph_girls_primary = get_plot_girls_primary(data=data_girls_1)

        data_both_primary = df.query("category_of_school == 'primary'")

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
        data_boys_1 = df.query("sex=='males' and category_of_school == 'secondary'")

        json_records = data_boys_1.reset_index().to_json(orient='records')
        data_boys_secondary = json.loads(json_records)
        # function to get the graph
        graph_boys_secondary = get_plot_boys_secondary(data=data_boys_1)

        data_girls_1 = df.query("sex=='females' and category_of_school == 'secondary'")

        json_records = data_girls_1.reset_index().to_json(orient='records')
        data_girls_secondary = json.loads(json_records)
        # function to get the graph
        graph_girls_secondary = get_plot_girls_secondary(data=data_girls_1)

        data_both_secondary = df.query("category_of_school == 'secondary'")

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
                                   values().all())
        df_regression = pd.merge(
            left=df, right=expenditure, on='academic_year')
        json_records = df_regression.reset_index().to_json(orient='records')
        data_regression = json.loads(json_records)

        data_boys_1 = df_regression.query(
            "sex=='male' and category_of_school == 'primary'")

        data_boys_1 = data_boys_1[(
                data_boys_1[['age_5_to_11_years', 'gdp_millions']] != 0).all(axis=1)]
        data_boys_1['ger'] = (data_boys_1['enrollment'] /
                              data_boys_1['age_5_to_11_years']) * 100
        data_boys_1['ger'] = data_boys_1['ger'].replace(np.inf, 0)
        data_boys_1['ger'].astype(float)
        json_records = data_boys_1.reset_index().to_json(orient='records')
        data_boys_primary = json.loads(json_records)

        data_girls_1 = df_regression.query(
            "sex=='female' and category_of_school == 'primary'")

        json_records = data_girls_1.reset_index().to_json(orient='records')
        data_girls_primary = json.loads(json_records)

        data_boys_1_secondary = df_regression.query(
            "sex=='male' and category_of_school == 'secondary'")
        json_records = data_boys_1_secondary.reset_index().to_json(orient='records')
        data_boys_secondary = json.loads(json_records)
        # function to get the graph

        data_girls_1_secondary = df_regression.query(
            "sex=='female' and category_of_school == 'secondary'")

        json_records = data_girls_1_secondary.reset_index().to_json(orient='records')
        data_girls_secondary = json.loads(json_records)
        # function to get the graph

        graph_all = get_plot_regression(data=df_regression)
        graph_stats = get_kernel_density(data=df_regression)
        graph_gdp_reg = get_plot_gdp_regress(data=df_regression)
        graph_pearsons = get_enrollment_joint_pearsons(data=df_regression)
        graph_spearman = get_enrollment_joint_spearman(data=df_regression)
        graph_multicollinear = get_enrollment_multicollinearity(data=df_regression)

        context = {'d_boys': data_boys_primary,
                   'd': data_regression,
                   'd_girls_primary': data_girls_primary,
                   'd_girls_secondary': data_girls_secondary,
                   'd_boys_primary': data_boys_secondary,
                   'd_boys_secondary': data_girls_secondary,
                   'graph_all': graph_all,
                   'graph_stats': graph_stats,
                   'graph_pearsons': graph_pearsons,
                   'graph_spearman': graph_spearman,
                   'graph_gdp_reg': graph_gdp_reg,
                   'graph_multicollinear': graph_multicollinear

                   }

        return render(request, 'ger_regression.html', context)

    return render(request, 'enrollment_summary.html', context)


# ==============================================
# View for outlier detection at district level
# ==============================================

def outlier_district(request):
    # return HttpResponse('In outlier detection at district level')

    error_message = None
    graph = None

    districts_names = District.objects.values('id', 'district_name')
    year_list = Enrollment.objects.distinct().values_list('year', flat=True)
    school_categories = Enrollment.objects.distinct(
    ).values_list('category_of_school', flat=True)

    if len(districts_names) > 0 and len(school_categories) > 0:
        if request.method == 'POST':

            district_selected = request.POST.get('district_name', None)
            selected_year = request.POST.get('year', None)
            selected_school_type = request.POST.get('school_type', None)

            if not district_selected or not selected_year or not selected_school_type:
                error_message = "Please select all variables"
            else:
                # enrollment_df = pd.DataFrame(AggregateEnrollment.objects.values().filter(district_of_school=district_selected, academic_year = selected_year))
                enrollment_df = pd.DataFrame(
                    AggregateEnrollment.objects.all().filter(category_of_school=selected_school_type,
                                                             district_of_school=district_selected,
                                                             academic_year=selected_year).values())

                if (enrollment_df.empty):
                    error_message = "No record was found for the selected district and academic year"

                else:

                    schools_df = pd.DataFrame(School.objects.all().values())
                    final_df = pd.merge(left=enrollment_df, right=schools_df,
                                        left_on='name_of_school_id', right_on='id')

                    enrollment_mean = final_df['total_enrollment'].mean()

                    enrollment_median = final_df['total_enrollment'].median()

                    mean_list = []

                    x = range(0, len(final_df['school_name']))

                    for a in x:
                        mean_list.append(enrollment_mean)

                    data_mean = pd.DataFrame(mean_list, columns=['Mean'])

                    graph = get_outlier_district_plot(x=final_df['total_enrollment'],
                                                      y=final_df['school_name'],
                                                      data=final_df,
                                                      academic_year=selected_year,
                                                      data_mean=data_mean,
                                                      input_school_type=selected_school_type,
                                                      input_district=district_selected
                                                      )
    else:
        error_message = "No records found"

    stu = {
        "graph": graph,
        "error_message": error_message,
        "districts_name": districts_names,
        "year_list": year_list,
        "school_list": school_categories

    }

    return render(request, 'outlier_district_page.html', stu)


# ==============================================
# View for outlier detection at national level
# ==============================================

def outlier_national(request):
    error_message = None
    graph = None
    selected_school_type = ''
    selected_year = ''

    year_list = Enrollment.objects.distinct().values_list('year', flat=True)
    school_categories = Enrollment.objects.distinct(
    ).values_list('category_of_school', flat=True)

    if (len(year_list) > 0 and len(school_categories) > 0):
        if ((request.method) == 'POST'):

            selected_school_type = request.POST.get('school_type', None)
            selected_year = request.POST.get('year', None)

            if (not selected_year or not selected_school_type):
                error_message = "Please select an academic year"
            else:
                # enrollment_df = pd.DataFrame(AggregateEnrollment.objects.values().filter(district_of_school=district_selected, academic_year = selected_year))
                enrollment_df = pd.DataFrame(AggregateEnrollment.objects.all().filter(
                    category_of_school=selected_school_type, academic_year=selected_year).values())

                if (enrollment_df.empty):
                    error_message = "No record was found for the academic year"

                else:
                    schools_df = pd.DataFrame(School.objects.all().values())
                    final_df = pd.merge(left=enrollment_df, right=schools_df,
                                        left_on='name_of_school_id', right_on='id')

                    enrollment_mean = final_df['total_enrollment'].mean()

                    mean_list = []

                    x = range(0, len(final_df['school_name']))

                    for a in x:
                        mean_list.append(enrollment_mean)

                    data_mean = pd.DataFrame(mean_list, columns=['Mean'])
                    graph = get_outlier_national_plot(x=final_df['total_enrollment'],
                                                      y=final_df['school_name'],
                                                      data=final_df,
                                                      academic_year=selected_year,
                                                      data_mean=data_mean,
                                                      input_school_type=selected_school_type

                                                      )
    else:
        error_message = "No records found"

    stu = {
        "graph": graph,
        "error_message": error_message,
        "year_list": year_list,
        "school_list": school_categories

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
            if request.POST['submit'] == 'Compare All Districts (CEE)':
                chart_title = "CEE Comparison, All Districts"
                context['chart_title'] = chart_title
                data = PrimaryPerformance.objects.all()
                [graph, heatmap] = primary_performance_plot(data, None, None)
                context['graph'] = graph
                context['heatmap'] = heatmap
                return render(request, 'district_performance.html', context)
            if request.POST['submit'] == 'Compare All Districts (CSEC)':
                chart_title = "CSEC Comparison, All Districts"
                context['chart_title'] = chart_title
                data = CSEC.objects.all()
                if not data:
                    context['error_message'] = "No data available."
                    return render(request, 'district_performance.html', context)
                [graph, heatmap, left_out] = csec_performance_plot(data, None, None)
                context['graph'] = graph
                context['heatmap'] = heatmap
                return render(request, 'district_performance.html', context)

            if request.POST['submit'] == 'Compare CEE Results':
                # Compare CEE between 2 districts
                district_1 = request.POST.get('district_1_name', False)
                district_2 = request.POST.get('district_2_name', False)
                if not (district_1 and district_2) or district_1 == district_2:
                    error_message = "Please select 2 different districts to compare."
                    context['error_message'] = error_message
                    return render(request, 'district_performance.html', context)
                else:
                    chart_title = "CEE Comparison, Districts " + district_1 + " and " + district_2
                    context['chart_title'] = chart_title
                    data = PrimaryPerformance.objects.all()
                    [graph, heatmap] = primary_performance_plot(data, int(district_1), int(district_2))
                    context['graph'] = graph
                    context['heatmap'] = heatmap
                    return render(request, 'district_performance.html', context)

            if request.POST['submit'] == 'Compare CSEC Results':
                # Compare CSEC between 2 districts
                district_3 = request.POST.get('district_3_name', False)
                district_4 = request.POST.get('district_4_name', False)
                if not (district_3 and district_4) or district_3 == district_4:
                    error_message = "Please select 2 different districts to compare."
                    context['error_message'] = error_message
                    return render(request, 'district_performance.html', context)
                if request.POST['submit'] == 'Compare CSEC Results':
                    chart_title = "CSEC Comparison, Districts " + district_3 + " and " + district_4
                    context['chart_title'] = chart_title
                    data = CSEC.objects.all()
                    if not data:
                        context['error_message'] = "No data available."
                        return render(request, 'district_performance.html', context)
                    [graph, heatmap, left_out] = csec_performance_plot(data, int(district_3), int(district_4))
                    context['graph'] = graph
                    context['heatmap'] = heatmap
                    return render(request, 'district_performance.html', context)
        else:
            return render(request, 'district_performance.html', context)


UNIVERSAL_FIELDS = {'id', 'created_at', 'created_by', 'updated_at', 'updated_by'}


def primary_performance(request):
    context = {}
    if request.method == 'POST':
        # Compare all districts
        if request.POST['submit'] == 'Generate Correlation Table':
            chart_title = "Correlation"
            context['chart_title'] = chart_title
            data = PrimaryPerformance.objects.values().all()
            graph = correlations(data, UNIVERSAL_FIELDS)
            context['graph'] = graph
            return render(request, 'primary_performance.html', context)
        if request.POST['submit'] == 'Build Model':
            chart_title = "Random Forest Regression"
            context['chart_title'] = chart_title
            data = PrimaryPerformance.objects.all()
            [graph, acc] = rf_model(data, UNIVERSAL_FIELDS, False)
            context['graph'] = graph
            context['accuracy'] = acc
    return render(request, 'primary_performance.html', context)


def upload_scores(request):
    context = {}
    cee_field_names = CEE._meta.get_fields()
    cee_field_names = [str(f).split('.')[-1] for f in cee_field_names]
    cee_field_names = set(cee_field_names) - UNIVERSAL_FIELDS
    cee_field_names = list(cee_field_names - set(["primsch", "secsch", "district"]))
    cee_field_names += ["primsch_id", "secsch_id", "district_id"]
    cee_field_names.sort()

    csec_field_names = CSEC._meta.get_fields()
    csec_field_names = [str(f).split('.')[-1] for f in csec_field_names]
    csec_field_names = list(set(csec_field_names) - UNIVERSAL_FIELDS)
    csec_field_names.remove("school")
    csec_field_names.append("school_id")
    csec_field_names.sort()
    context['cee_field_names'] = cee_field_names
    context['csec_field_names'] = csec_field_names

    context['cee_count'] = CEE.objects.count()
    context['csec_count'] = CSEC.objects.count()

    cee_by_year = [item['test_yr'] for item in CEE.objects.values('test_yr').distinct()]
    csec_by_year = [item['year'] for item in CSEC.objects.values('year').distinct()]
    cee_by_year.sort()
    csec_by_year.sort()
    context['cee_by_year'] = cee_by_year
    context['csec_by_year'] = csec_by_year

    if "GET" == request.method:
        return render(request, "upload_scores.html", context)
    type = "CEE"
    field_names = []
    csv_file = None
    if request.POST['submit'] == 'Upload CSEC Scores':
        field_names = csec_field_names
        if not "csec_file" in request.FILES:
            context['error_message'] = 'Please select a file to upload.'
            return render(request, "upload_scores.html", context)
        csv_file = request.FILES["csec_file"]
        type = "CSEC"
    elif request.POST['submit'] == 'Upload CEE Scores':
        field_names = cee_field_names
        if not "cee_file" in request.FILES:
            context['error_message'] = 'Please select a file to upload.'
            return render(request, "upload_scores.html", context)
        csv_file = request.FILES["cee_file"]

    if request.POST['submit'].startswith("delete_cee"):
        time_period = request.POST['submit'][10:]
        CEE.objects.filter(test_yr=int(time_period)).delete()
    elif request.POST['submit'].startswith("delete_csec"):
        time_period = request.POST['submit'][11:]
        CSEC.objects.filter(year=time_period).delete()
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
    context['cee_count'] = CEE.objects.count()
    context['csec_count'] = CSEC.objects.count()
    context['cee_by_year'] = [item['test_yr'] for item in CEE.objects.values('test_yr').distinct()]
    context['csec_by_year'] = [item['year'] for item in CSEC.objects.values('year').distinct()]

    return render(request, "upload_scores.html", context)


# ======================================================================
# View for box plots at district level
# ======================================================================

def boxplot_district(request):
    error_message = None
    graph = None

    districts_names = District.objects.values('id', 'district_name')
    year_list = Enrollment.objects.distinct().values_list('year', flat=True)
    school_categories = Enrollment.objects.distinct().values_list('category_of_school', flat=True)

    if len(districts_names) > 0 and len(school_categories) > 0:

        if request.method == 'POST':

            district_selected = request.POST.get('district_name', None)
            selected_year = request.POST.get('year', None)
            selected_school_type = request.POST.get('school_type', None)

            if (not district_selected or not selected_year or not selected_school_type):
                error_message = "Please select all variables"
            else:
                enrollment_df = pd.DataFrame(
                    AggregateEnrollment.objects.all().filter(category_of_school=selected_school_type,
                                                             district_of_school=district_selected,
                                                             academic_year=selected_year).values())

                if (enrollment_df.empty):
                    error_message = "No record was found for the selected district and academic year"

                else:

                    schools_df = pd.DataFrame(School.objects.all().values())
                    final_df = pd.merge(left=enrollment_df, right=schools_df,
                                        left_on='name_of_school_id', right_on='id')

                    graph = get_boxplot_district_plot(x=final_df['total_enrollment'],
                                                      y=final_df['school_name'],
                                                      data=final_df,
                                                      academic_year=selected_year,
                                                      input_school_type=selected_school_type,
                                                      input_district=district_selected
                                                      )

    else:
        error_message = "No records found"

    stu = {
        "graph": graph,
        "error_message": error_message,
        "districts_name": districts_names,
        "year_list": year_list,
        "school_list": school_categories

    }

    return render(request, 'boxplots_district_page.html', stu)


# ====================================================================
# View for box plots at national level
# ====================================================================

def boxplot_national(request):
    error_message = None
    graph = None

    year_list = Enrollment.objects.distinct().values_list('year', flat=True)
    school_categories = Enrollment.objects.distinct().values_list('category_of_school', flat=True)

    if len(year_list) > 0 and len(school_categories) > 0:
        if request.method == 'POST':

            selected_school_type = request.POST.get('school_type', None)
            selected_year = request.POST.get('year', None)

            if not selected_year or not selected_school_type:
                error_message = "Please select an academic year"
            else:

                enrollment_df = pd.DataFrame(
                    AggregateEnrollment.objects.all().filter(category_of_school=selected_school_type,
                                                             academic_year=selected_year).values())

                if enrollment_df.empty:
                    error_message = "No record was found for the academic year"

                else:
                    schools_df = pd.DataFrame(School.objects.all().values())
                    final_df = pd.merge(left=enrollment_df, right=schools_df,
                                        left_on='name_of_school_id', right_on='id')

                    graph = get_boxplot_national_plot(x=final_df['total_enrollment'],
                                                      y=final_df['school_name'],
                                                      data=final_df,
                                                      academic_year=selected_year,
                                                      input_school_type=selected_school_type

                                                      )
    else:
        error_message = "No records found"

    stu = {
        "graph": graph,
        "error_message": error_message,
        "year_list": year_list,
        "school_list": school_categories

    }

    return render(request, 'boxplots_national_page.html', stu)


# This is the examination Analysis
def examination_summary(request):
    cee_data = pd.DataFrame(CEE.objects.values().all())
    csec_data = pd.DataFrame(CSEC.objects.values().all())
    corv = csec_data[['subject', 'proficiency', 'profile1', 'profile2', 'profile3', 'profile4', 'overall_grade']]
    # graph = covariance(corv=corv)
    context = {'d': cee_data.to_html(),
               'summary_age': cee_data[['age_at_test']].describe().to_html(),
               'summary_engcomp': cee_data[['engcomp']].astype(float).describe().to_html(),
               'summary_mathcomp': cee_data[['mathcomp']].astype(float).describe().to_html(),
               'summary_gpcomp': cee_data[['gpcomp']].astype(float).describe().to_html(),
               'summary_totcomp': cee_data[['totcomp']].astype(float).describe().to_html(),
               'summary_sex': cee_data[['sex']].describe().to_html(),
               'score_corr': cee_data[['engcomp', 'mathcomp', 'gpcomp', 'totcomp']].astype(float).corr().to_html(),
               'summary_sex_secondary': csec_data[['sex']].describe().to_html(),
               'summary_subject_secondary': csec_data[['subject']].describe().to_html(),
               'summary_proficiency_secondary': csec_data[['proficiency']].describe().to_html(),
               'summary_profile1_secondary': csec_data[['profile1']].describe().to_html(),
               'summary_profile2_secondary': csec_data[['profile2']].describe().to_html(),
               'summary_profile3_secondary': csec_data[['profile3']].describe().to_html(),
               'summary_profile4_secondary': csec_data[['profile4']].describe().to_html(),
               # 'graph' : graph,

               }

    return render(request, 'examination_summary.html', context)
