# tables.py
from historical_surveillance.models import AggregateEnrollment, CEE, CSEC, District, Enrollment, School
from django.utils.html import format_html
from django.urls import reverse
import django_tables2 as tables
import django_filters


class ActionsColumn(tables.Column):
    editViewName = ''
    def __init__(self, *args, **kwargs):
        super().__init__('Actions',exclude_from_export=True)
        self.editViewName = kwargs.get('editViewName')

    def render(self, value):
        return format_html('<a href="'+reverse(self.editViewName, args=(value,))+ '"><button type="button" class="btn btn-sm btn-primary"><i class="fas fa-pencil-alt"></i> Edit</button></a>', value)

class DistrictTable(tables.Table):
    id = ActionsColumn(editViewName ='surveillance:update-district')
    class Meta:
        model = District
        fields = ('district_code', 'district_name', 'id')
        attrs = {"class": "table table-striped table-bordered"}

class DistrictFilter(django_filters.FilterSet):
    class Meta:
        model = District
        fields = ['district_code', 'district_name']

class SchoolTable(tables.Table):
    id = ActionsColumn(editViewName ='surveillance:update-school')
    class Meta:
        model = School
        fields = ('school_code', 'district_name', 'school_name','category_of_school', 'id')
        attrs = {"class": "table table-striped table-bordered"}

class SchoolFilter(django_filters.FilterSet):
    class Meta:
        model = School
        fields = ['school_code','district_name', 'school_name','category_of_school']

class EnrollmentTable(tables.Table):
    id = ActionsColumn(editViewName ='surveillance:update-enrollment')
    class Meta:
        model = Enrollment
        fields = ('district','school','grade','enrollment','sex', 'minimum_age','maximum_age','id')
        attrs = {"class": "table table-striped table-bordered"}

class EnrollmentFilter(django_filters.FilterSet):
    enrollment= django_filters.RangeFilter()
    maximum_age= django_filters.RangeFilter()
    minimum_age= django_filters.RangeFilter()
    class Meta:
        model = Enrollment
        fields = {'district': ['exact'] ,'school': ['exact'], 'grade':['exact'],'sex':['exact']}


class AggregateEnrollmentTable(tables.Table):
    id = ActionsColumn(editViewName ='surveillance:update-aggregate-enrollment')
    class Meta:
        model = AggregateEnrollment
        fields = ('academic_year','district_of_school','name_of_school','category_of_school','capacity_of_school','total_enrollment','id')
        attrs = {"class": "table table-striped table-bordered"}

class AggregateEnrollmentFilter(django_filters.FilterSet):
    capacity_of_school= django_filters.RangeFilter()
    total_enrollment= django_filters.RangeFilter()
    class Meta:
        model = AggregateEnrollment
        fields = {'academic_year' : ['contains'], 'district_of_school': ['exact'] ,'name_of_school': ['exact'],'category_of_school': ['exact'] }

class CeeTable(tables.Table):
    id = ActionsColumn(editViewName ='surveillance:update-cee')
    class Meta:
        model = CEE
        fields = ('test_yr','primsch','secsch','age_at_test','sex','engcomp','mathcomp','gpcomp','totcomp')
        attrs = {"class": "table table-striped table-bordered"}

class CeeFilter(django_filters.FilterSet):
    test_yr = django_filters.RangeFilter()
    age_at_test = django_filters.RangeFilter()
    engcomp = django_filters.RangeFilter()
    mathcomp = django_filters.RangeFilter()
    gpcomp = django_filters.RangeFilter()
    totcomp = django_filters.RangeFilter()
    class Meta:
        model = CEE
        fields = {'primsch':['exact'],'secsch':['exact']}

class CsecTable(tables.Table):
    id = ActionsColumn(editViewName ='surveillance:update-csec')
    class Meta:
        model = CSEC
        fields = ('year','school','sex','subject','proficiency','profile1','profile2','profile3','profile4','overall_grade')
        attrs = {"class": "table table-striped table-bordered"}

class CsecFilter(django_filters.FilterSet):
    year = django_filters.RangeFilter()
    class Meta:
        model = CSEC
        fields = {'school':['exact'],'sex':['exact'],'subject':['exact'], 'profile1':['exact'],'profile2':['exact'],'profile3':['exact'],'profile4':['exact'], 'overall_grade':['exact']}
