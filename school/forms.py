from django import forms

from .models import (
    Course,
    Subject,
    SubjectGroup,
    Assignment,
    AssignmentGrade,
    CourseGrade,
    Student,
    TeacherAppraisal,
    PrincipalAppraisal,
)
from historical_surveillance.models import District, School
from authentication.models.users import Teacher, SchoolPrincipal
from django.forms import TextInput, Textarea


class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = "__all__"
        widgets = {
            "created_by": TextInput(attrs={"readonly": "readonly"}),
            "updated_by": TextInput(attrs={"readonly": "readonly"}),
        }


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = "__all__"
        widgets = {
            "created_by": TextInput(attrs={"readonly": "readonly"}),
            "updated_by": TextInput(attrs={"readonly": "readonly"}),
        }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"
        labels = {
            "existing_medication": "Please note here any medical problem(s) that you child may have and medication(s) being used.",
            "existing_allergies": "Please note here any allergies your child may have",
            "dietary_requirements": "Does your child have any dietary requirements",
            "special_needs": "Please note here any problems which may bar your child from participating in physical activities",
            "home_supervision": "Do you find that your child often needs home-work supervision or extra help? Explain.",
            "parent_help": "Are you able to supervise your child's school work and give help when needed?",
            "discipline_history": "Has your child ever been subject of a major disciplinary action? If so please explain",
            "interests_talents": "Describe your child's special interest or talents",
            "clubs_or_sports": "Please list any clubs or sports teams your child belongs to",
            "improvements_requested": "What academic improvements would you like to see in your child by the end of the first term",
            "school_expectations": "",
        }
        widgets = {
            "date_of_birth": TextInput(attrs={"type": "date"}),
            "existing_medication": Textarea(attrs={"rows": 3, "cols": 20}),
            "existing_allergies": Textarea(attrs={"rows": 3, "cols": 20}),
            "dietary_requirements": Textarea(attrs={"rows": 3, "cols": 20}),
            "home_supervision": Textarea(attrs={"rows": 3, "cols": 20}),
            "parent_help": Textarea(attrs={"rows": 3, "cols": 20}),
            "discipline_history": Textarea(attrs={"rows": 3, "cols": 20}),
            "special_needs": Textarea(attrs={"rows": 3, "cols": 20}),
            "interests_talents": Textarea(attrs={"rows": 3, "cols": 20}),
            "clubs_or_sports": Textarea(attrs={"rows": 3, "cols": 20}),
            "improvements_requested": Textarea(attrs={"rows": 3, "cols": 20}),
            "school_expectations": Textarea(attrs={"rows": 3, "cols": 20}),
        }


# TODO https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"
        # fields = ["school", "subject", "teachers"]


class CourseGradeForm(forms.ModelForm):
    class Meta:
        model = CourseGrade
        fields = "__all__"


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = "__all__"


class SubjectGroupForm(forms.ModelForm):
    class Meta:
        model = SubjectGroup
        fields = "__all__"


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = "__all__"


class AssignmentGradeForm(forms.ModelForm):
    class Meta:
        model = AssignmentGrade
        fields = "__all__"


class PrincipalForm(forms.ModelForm):
    class Meta:
        model = SchoolPrincipal
        fields = [
            "username",
            "school",
            "first_name",
            "last_name",
            "email",
            "sex",
            "date_of_birth",
            "qualifications",
        ]
        widgets = {
            "date_of_birth": TextInput(attrs={"type": "date"}),
        }


class PrincipalAppraisalForm(forms.ModelForm):
    class Meta:
        model = PrincipalAppraisal
        fields = "__all__"
        labels = {
            "teaching_experience_years": "Teaching experience: Year(s)",
            "teaching_staff": "Number of teaching Staff",
            "ancillary_staff": "Number of Ancillary Staff",
            "administrative_staff": "Number of Administrative Staff",
            "evaluation_period_start": "Evaluation Period Start",
            "evaluation_period_end": "Evaluation Period End",
            "last_appraisal": "Period of Last Appraisal",
            "pre_conference": "Pre-conference",
            # Teaching and learning
            "class_visits": "Maintains a schedule of class visits",
            "class_observation": "Provides feedback on classroom observations",
            "teacher_reviews": "Reviews teachers: (a) Scheme and record of work (b) written plans/lesson notes",
            "conducts_lessons": "Conducts demonstration lessons when necessary",
            "ensures_literacy_improvement": "Ensures that improvement in literacy and numeracy are priority targets for all students",
            "student_achivevemnet": "sets standards for students' achievement",
            "class_supervision": "ensures that classes are adequately supervised at all times",
            # Planning and organization
            "school_development_plan": "formulates the School Development Plan with assistance of staff and relevant stakeholders",
            "smart_objectives": "ensures that the objectives outlined in the plan are (SMART) specific, measureable, achievable, result oriented and timed",
            "annual_work_plan": "prepares an Annual Work Plan that includes a calendar of activities for the school",
            "submits_to_ministry": "submits copies of Plans to Ministry of Education by October of each year",
            "plan_implementation": "ensures that the plan is implemented, monitored and evaluated",
            "master_time_table": "prepares a master time-table for the school",
            "time_table_available": "makes the time-table available to teachers and Ministry officials",
            "ensure_teacher_comply_time_table": "ensures that teachers comply with the time-table",
            "prepare_annual_report": "prepares and submits an annual report to the Ministry",
            # Comments
            "principals_comments": "Principal's Comments",
            "district_education_officer_comments": "District Education Officer's Comments",
            "chief_education_officer_comments": "Cheif Education Officer's Comments",
        }
        widgets = {
            "evaluation_period_start": TextInput(attrs={"type": "date"}),
            "evaluation_period_end": TextInput(attrs={"type": "date"}),
            "last_appraisal": TextInput(attrs={"type": "date"}),
            # Comments
            "principals_comments": Textarea(attrs={"rows": 3, "cols": 20}),
            "district_education_officer_comments": Textarea(
                attrs={"rows": 3, "cols": 20}
            ),
            "chief_education_officer_comments": Textarea(attrs={"rows": 3, "cols": 20}),
        }


class TeacherAppraisalForm(forms.ModelForm):
    class Meta:
        model = TeacherAppraisal
        fields = "__all__"

