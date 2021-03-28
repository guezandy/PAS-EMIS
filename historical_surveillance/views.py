from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Count
from .forms import AggregateEnrollmentForms, DistrictForms, SchoolForms, EnrollmentForms
from .models import AggregateEnrollment
import pandas as pd
from .utils import get_plot


def district(request):
    form = DistrictForms()
    if request.method == 'POST':
        form = DistrictForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, 'district.html', {'form': form})


def school(request):
    form = SchoolForms()
    if request.method == 'POST':
        form = SchoolForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, 'school.html', {'form': form})


# links to the home page for this app
def index(request):
    return render(request, 'surv_home.html', {})


# links to the enrollment
def enrollment(request):
    form = EnrollmentForms()
    return render(request, 'enrollment.html', {'form': form})


# Links to view the enrollment versus Class size table
def enrolled(request):
    data = AggregateEnrollment.objects.all()

    stu = {
        "name_of_school": data
    }
    return render(request, 'enrolled.html', stu)


# Links to data entry for enrollment versus class size
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


def enrolled_trend_district_1(request):
    data = AggregateEnrollment.objects.all().filter(district_of_school=1)

    stu = {
        "name_of_school": data
    }
    return render(request, 'district_1.html', stu)


def enrolled_trend_district_2(request):
    data = AggregateEnrollment.objects.all().filter(district_of_school=2)

    stu = {
        "name_of_school": data
    }
    return render(request, 'district_2.html', stu)


def enrolled_trend_district_3(request):
    data = AggregateEnrollment.objects.all().filter(district_of_school=3)

    stu = {
        "name_of_school": data
    }
    return render(request, 'district_3.html', stu)


def enrolled_trend_district_4(request):
    data = AggregateEnrollment.objects.all().filter(district_of_school=4)

    stu = {
        "name_of_school": data
    }
    return render(request, 'district_4.html', stu)


def enrolled_trend_district_5(request):
    data = AggregateEnrollment.objects.all().filter(district_of_school=5)

    stu = {
        "name_of_school": data
    }
    return render(request, 'district_5.html', stu)


def enrolled_trend_district_6(request):
    data = AggregateEnrollment.objects.all().filter(district_of_school=6)

    stu = {
        "name_of_school": data
    }
    return render(request, 'district_6.html', stu)


def enrolled_trend_district_7(request):
    data = AggregateEnrollment.objects.all().filter(district_of_school=7)

    stu = {
        "name_of_school": data
    }
    return render(request, 'district_7.html', stu)


def enrolled_trend_district_8(request):
    data = AggregateEnrollment.objects.all().filter(district_of_school=8)

    stu = {
        "name_of_school": data
    }
    return render(request, 'district_8.html', stu)


def district_1_trend(request):
    error_message = None
    graph = None
    df = None
    data = AggregateEnrollment.objects.all().filter(district_of_school=1). \
        values('name_of_school', 'category_of_school').distinct().annotate(total=Count('name_of_school')) \
        .order_by('category_of_school')
    schools_df = pd.DataFrame(AggregateEnrollment.objects.all().filter(district_of_school=1).values())
    schools = schools_df['name_of_school'].unique()

    if schools_df.shape[0] > 0:
        if request.method == 'POST':
            chart = request.POST.get('chart', False)
            selected_school = request.POST.get('school_name', None)
            if not chart:
                if not selected_school:
                    error_message = "Please select a chart type and school"

            else:
                if chart is not False:
                    if selected_school is not None:
                        select_school_df = pd.DataFrame(AggregateEnrollment.objects.all().\
                                                        filter(name_of_school=selected_school).values())
                        select_school_df.sort_values(by=['academic_year'], inplace=True)
                        select_school_df = select_school_df.tail(10)
                        # function to get the graph
                        graph = get_plot(chart, z = select_school_df['capacity_of_school'],
                                         y=select_school_df['total_enrollment'],
                                         x=select_school_df['academic_year'],
                                         data=select_school_df,
                                         name_of_school=selected_school)
    else:
        error_message = "No records found"

    stu = {
        "graph": graph,
        "error_message": error_message,
        "name_of_school": data,
        "schools": schools,
        "schools_df": schools_df,

    }
    return render(request, 'district_1_trend.html', stu)


def district_2_trend(request):
    error_message = None
    graph = None
    df = None
    data = AggregateEnrollment.objects.all().filter(district_of_school=2). \
        values('name_of_school', 'category_of_school').distinct().annotate(total=Count('name_of_school')) \
        .order_by('category_of_school')
    schools_df = pd.DataFrame(AggregateEnrollment.objects.all().filter(district_of_school=2).values())
    schools = schools_df['name_of_school'].unique()

    if schools_df.shape[0] > 0:
        if request.method == 'POST':
            chart = request.POST.get('chart', False)
            selected_school = request.POST.get('school_name', None)
            if not chart:
                if not selected_school:
                    error_message = "Please select a chart type and school"

            else:
                if chart is not False:
                    if selected_school is not None:
                        select_school_df = pd.DataFrame(AggregateEnrollment.objects.all().\
                                                        filter(name_of_school=selected_school).values())
                        select_school_df.sort_values(by=['academic_year'], inplace=True)
                        select_school_df = select_school_df.tail(10)
                        # function to get the graph
                        graph = get_plot(chart, z = select_school_df['capacity_of_school'],
                                         y=select_school_df['total_enrollment'],
                                         x=select_school_df['academic_year'],
                                         data=select_school_df,
                                         name_of_school=selected_school)
    else:
        error_message = "No records found"

    stu = {
        "graph": graph,
        "error_message": error_message,
        "name_of_school": data,
        "schools": schools,
        "schools_df": schools_df,

    }
    return render(request, 'district_2_trend.html', stu)



def district_3_trend(request):
    error_message = None
    graph = None
    df = None
    data = AggregateEnrollment.objects.all().filter(district_of_school=3). \
        values('name_of_school', 'category_of_school').distinct().annotate(total=Count('name_of_school')) \
        .order_by('category_of_school')
    schools_df = pd.DataFrame(AggregateEnrollment.objects.all().filter(district_of_school=3).values())
    schools = schools_df['name_of_school'].unique()

    if schools_df.shape[0] > 0:
        if request.method == 'POST':
            chart = request.POST.get('chart', False)
            selected_school = request.POST.get('school_name', None)
            if not chart:
                if not selected_school:
                    error_message = "Please select a chart type and school"

            else:
                if chart is not False:
                    if selected_school is not None:
                        select_school_df = pd.DataFrame(AggregateEnrollment.objects.all().\
                                                        filter(name_of_school=selected_school).values())
                        select_school_df.sort_values(by=['academic_year'], inplace=True)
                        select_school_df = select_school_df.tail(10)
                        # function to get the graph
                        graph = get_plot(chart, z = select_school_df['capacity_of_school'],
                                         y=select_school_df['total_enrollment'],
                                         x=select_school_df['academic_year'],
                                         data=select_school_df,
                                         name_of_school=selected_school)
    else:
        error_message = "No records found"

    stu = {
        "graph": graph,
        "error_message": error_message,
        "name_of_school": data,
        "schools": schools,
        "schools_df": schools_df,

    }
    return render(request, 'district_3_trend.html', stu)
