from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import AggregateEnrollmentForms, DistrictForms, SchoolForms, EnrollmentForms
from .models import AggregateEnrollment, School, District, Enrollment
import pandas as pd
from .utils import get_plot, get_pairs

# This is the view for the home page of this app
def index(request):
    return render(request, "base.html", {})


# This function controls the district creation form view and process form data for save into the database
def district(request):
    error_message = None
    form = DistrictForms()
    data = District.objects.values("district_code", "district_name")
    if request.method == "POST":
        form = DistrictForms(request.POST)
        if form.is_valid():
            # change the created by column to automatically insert the logged in user
            district_created_by = form.cleaned_data["created_by"]
            district_code = form.cleaned_data["district_code"]
            district_name = form.cleaned_data["district_name"]
            # change the updated by column to automatically insert the name of the logged in user updating the column
            district_updated = form.cleaned_data["updated_by"]
            if not District.objects.filter(
                district_code=district_code, district_name=district_name
            ).exists():
                form.save()
                return redirect("/historical/")

            else:
                error_message = "The record you are trying to create already exists."

        stu = {
            "error_message": error_message,
        }
        return render(request, "district.html", stu)
    return render(request, "district.html", {"form": form, "district_created": data})


# This function controls the schools creation form view and process form data for save into the database
def create_school(request):
    error_message = None
    form = SchoolForms()
    data = School.objects.values("school_name", "category_of_school", "district_name")
    if request.method == "POST":
        form = SchoolForms(request.POST)
        if form.is_valid():
            # change the created by column to automatically insert the logged in user
            school_created_by = form.cleaned_data["created_by"]
            school_code = form.cleaned_data["school_code"]
            school_name = form.cleaned_data["school_name"]
            district_name = form.cleaned_data["district_name"]
            school_category = form.cleaned_data["category_of_school"]
            # change the updated by column to automatically insert the name of the logged in user updating the column
            school_updated = form.cleaned_data["updated_by"]
            if not School.objects.filter(
                school_code=school_code,
                school_name=school_name,
                district_name=district_name,
                category_of_school=school_category,
            ).exists():
                form.save()
                return redirect("/historical/")

            else:
                error_message = "The record you are trying to create already exists."

        stu = {
            "name_of_school": data,
            "error_message": error_message,
            "form": form,
        }
        return render(request, "school.html", stu)
    return render(request, "school.html", {"form": form, "name_of_school": data})


# This function controls the enrollment by school,
# grade and gender form view, processes the and submits form data to the database
# This view is a place holder and still under construction
def enrollment(request):
    form = EnrollmentForms()
    districts_names = District.objects.values("district_code", "district_name")
    return render(
        request, "enrollment.html", {"form": form, "district_names": districts_names}
    )


# This function controls the total enrollment and school capacity form, processes the form data and submits
# it to the database
# This view is still underconstruction
def enroll_class(request):
    form = AggregateEnrollmentForms()
    if request.method == "POST":
        form = AggregateEnrollmentForms(request.POST)
        if form.is_valid():
            school_form = form.cleaned_data["name_of_school"]
            academic_year_form = form.cleaned_data["academic_year"]
            district_form = form.cleaned_data["district_of_school"]
            if not AggregateEnrollment.objects.filter(
                name_of_school=school_form,
                academic_year=academic_year_form,
                district_of_school=district_form,
            ).exists():
                form.save()
                return redirect("/")
        else:
            messages.add_message(
                request, messages.INFO, "Data has been entered previously"
            )

    return render(request, "enroll_class.html", {"form": form})


# This view controls the enrollment / Capacity views table
def enrolled(request):
    data = AggregateEnrollment.objects.all()

    stu = {"name_of_school": data}
    return render(request, "enrolled.html", stu)


# change this to get a form to select the district and pass it as a parameter to present filter the table and present
# the data for each district
def enrolled_district(request):
    error_message = None

    districts_names = District.objects.values("id", "district_name")

    if len(districts_names) > 0:
        if request.method == "POST":
            district_selected = request.POST.get("district_name", False)
            if not district_selected:
                error_message = "Please select a chart type and school"
            else:
                if district_selected is not False:
                    data = AggregateEnrollment.objects.all().filter(
                        district_of_school_id=district_selected
                    )
                stu = {
                    "error_message": error_message,
                    "districts_names": districts_names,
                    "district_selected": district_selected,
                    "data": data,
                }
                return render(request, "enrolled_district.html", stu)
        else:
            return render(
                request, "enrolled_district.html", {"districts_names": districts_names}
            )


def district_trend(request):
    error_message = None
    graph = None
    districts_lists = District.objects.values("district_code", "district_name")
    schools = School.objects.values("id", "school_name")

    if len(schools) > 0:
        if request.method == "POST":
            chart = request.POST.get("chart", False)
            selected_school = request.POST.get("school_name", None)
            if not chart:
                if not selected_school:
                    error_message = "Please select a chart type and school"
            else:
                if chart is not False:
                    if selected_school is not None:
                        select_school_df = pd.DataFrame(
                            AggregateEnrollment.objects.all()
                            .filter(name_of_school=selected_school)
                            .values()
                        )
                        select_school_df.sort_values(by=["academic_year"], inplace=True)
                        select_school_df = select_school_df.tail(10)
                        # function to get the graph
                        graph = get_plot(
                            chart,
                            z=select_school_df["capacity_of_school"],
                            y=select_school_df["total_enrollment"],
                            x=select_school_df["academic_year"],
                            data=select_school_df,
                            # change this to reflect the name of the school
                            name_of_school=selected_school,
                        )
    else:
        error_message = "No records found"

    stu = {
        "graph": graph,
        "error_message": error_message,
        "schools": schools,
        "districts_lists": districts_lists,
    }
    return render(request, "district_trend.html", stu)


def compare_trends(request):
    error_message = None
    graph = None
    district_df = District.objects.values("id", "district_name")
    year_df = pd.DataFrame(AggregateEnrollment.objects.values("academic_year"))
    year_list = year_df["academic_year"].unique()
    if len(district_df) > 0:
        if request.method == "POST":
            selected_district = request.POST.get("district_name", False)
            year = request.POST.get("year", False)
            if not selected_district:
                if not year:
                    error_message = "Please select a chart type and school"
            else:
                if selected_district is not False:
                    if year is not False:
                        aggregate_df = pd.DataFrame(
                            AggregateEnrollment.objects.all()
                            .filter(
                                district_of_school=selected_district, academic_year=year
                            )
                            .values()
                        )
                        schools_df = pd.DataFrame(School.objects.all().values())
                        df = pd.merge(
                            left=aggregate_df,
                            right=schools_df,
                            left_on="name_of_school_id",
                            right_on="id",
                        )
                        # function to get the graph
                        graph = get_pairs(
                            x=df["total_enrollment"],
                            y=df["capacity_of_school"],
                            data=df,
                            academic_year=year,
                            district_name=selected_district,
                            name_of_school=df["school_name"],
                        )
    else:
        error_message = "No records found"

    stu = {
        "graph": graph,
        "error_message": error_message,
        "districts_lists": district_df,
        "year_list": year_list,
    }
    return render(request, "compare_trends.html", stu)


# This view controls the enrollment / Capacity views table
def enrolled_grade(request):
    data = Enrollment.objects.all()

    stu = {"name_of_school": data}
    return render(request, "enrolled_grade.html", stu)


def district_grade(request):
    error_message = None

    districts_names = District.objects.values("id", "district_name")

    if len(districts_names) > 0:
        if request.method == "POST":
            district_selected = request.POST.get("district_name", False)
            if not district_selected:
                error_message = "Please select a chart type and school"
            else:
                if district_selected is not False:
                    data = Enrollment.objects.all().filter(
                        district_id=district_selected
                    )
                stu = {
                    "error_message": error_message,
                    "districts_names": districts_names,
                    "district_selected": district_selected,
                    "data": data,
                }
                return render(request, "district_grade.html", stu)
        else:
            return render(
                request, "district_grade.html", {"districts_names": districts_names}
            )


"""
def district_grade_school(request):
    error_message = None
    graph = None

    district_df = pd.DataFrame(District.objects.all().values())
    districts_lists = district_df['district_name']

    schools_df = pd.DataFrame(Enrollment.objects.all().values())
    schools = schools_df['school'].unique()

    data = Enrollment.objects.all(). \
        values('school', 'year', 'category_of_school', 'district', 'grade', 'sex', 'enrollment').distinct(). \
        annotate(total=Count('school')).order_by('category_of_school')

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
                        select_school_df = pd.DataFrame(Enrollment.objects.all().
                                                        filter(school=selected_school).values())
                        select_school_df.sort_values(by=['year'], inplace=True)
                        select_school_df = select_school_df.tail(10)
                        # function to get the graph
                        # graph = get_school_plot(chart, z=select_school_df['sex'],
                        # y=select_school_df['enrollment'],
                        # x=select_school_df['year'],
                        # a=select_school_df['grade'],
                        # data=select_school_df,
                        # name_of_school=selected_school)
    else:
        error_message = "No records found"

    stu = {
        "graph": graph,
        "error_message": error_message,
        "name_of_school": data,
        "schools": schools,
        "schools_df": schools_df,
        "districts_lists": districts_lists,

    }
    return render(request, 'district_grade_school.html', stu)
"""
