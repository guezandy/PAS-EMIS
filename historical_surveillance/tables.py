# tables.py
from historical_surveillance.models import AggregateEnrollment
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