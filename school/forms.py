from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML

from .models import (
    Course,
    CourseOutcome,
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
        fields = ["district_name", "district_code"]
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = "__all__"
        widgets = {
            "created_by": TextInput(attrs={"readonly": "readonly"}),
            "updated_by": TextInput(attrs={"readonly": "readonly"}),
        }
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'


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
            "school_expectations": "Expectations of school",
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("first_name", css_class="form-group col-md-4 mb-0"),
                Column("middle_initial", css_class="form-group col-md-4 mb-0"),
                Column("last_name", css_class="form-group col-md-4 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("sex", css_class="form-group col-md-4 mb-0"),
                Column("date_of_birth", css_class="form-group col-md-4 mb-0"),
                css_class="form-row",
            ),
            "home_address",
            "last_school_attended",
            "school",
            "graduation_year",
            "father_name",
            Row(
                Column("father_work_telephone", css_class="form-group col-md-4 mb-0"),
                Column("father_home_telephone", css_class="form-group col-md-4 mb-0"),
                css_class="form-row",
            ),
            "father_email",
            Row(
                Column("father_occupation", css_class="form-group col-md-4 mb-0"),
                Column("father_home_address", css_class="form-group col-md-4 mb-0"),
                css_class="form-row",
            ),
            "mother_name",
            Row(
                Column("mother_work_telephone", css_class="form-group col-md-4 mb-0"),
                Column("mother_home_telephone", css_class="form-group col-md-4 mb-0"),
                css_class="form-row",
            ),
            "mother_email",
            Row(
                Column("mother_occupation", css_class="form-group col-md-4 mb-0"),
                Column("mother_home_address", css_class="form-group col-md-4 mb-0"),
                css_class="form-row",
            ),
            "guardian_name",
            Row(
                Column("guardian_work_telephone", css_class="form-group col-md-4 mb-0"),
                Column("guardian_home_telephone", css_class="form-group col-md-4 mb-0"),
                css_class="form-row",
            ),
            "guardian_email",
            Row(
                Column("guardian_occupation", css_class="form-group col-md-4 mb-0"),
                Column("guardian_home_address", css_class="form-group col-md-4 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("doctor_name", css_class="form-group col-md-4 mb-0"),
                Column("doctor_contact", css_class="form-group col-md-4 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("existing_medication", css_class="form-group col-md-4 mb-0"),
                Column("existing_allergies", css_class="form-group col-md-4 mb-0"),
                Column("dietary_requirements", css_class="form-group col-md-4 mb-0"),
                css_class="form-row",
            ),
            "home_supervision",
            "parent_help",
            "discipline_history",
            "special_needs",
            "interests_talents",
            "clubs_or_sports",
            "improvements_requested",
            "school_expectations",
            Submit('submit', 'Submit')
        )


# TODO https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'


class CourseOutcomeForm(forms.ModelForm):
    class Meta:
        model = CourseOutcome
        fields = "__all__"
        widgets = {
            "notes": Textarea(attrs={"rows": 3, "cols": 20}),
        }
    helper = FormHelper()
    helper.add_input(Submit('submit', 'Submit', css_class='btn-primary'))
    helper.form_method = 'POST'


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "username",
            "school",
            Row(
                Column("first_name", css_class="form-group col-md-4 mb-0"),
                Column("last_name", css_class="form-group col-md-4 mb-0"),
                css_class="form-row",
            ),
            "sex",
            "date_of_birth",
            "qualifications",
            Submit('submit', 'Submit')
        )


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
            # Leadership
            "involves_staff": "involve staff in the decision making ",
            "facilitates_parental": "facilitates parental/stakeholder involvement in school life ",
            "inspires_and_motivates": "inspires and motivates staff and students to achieve their full potential ",
            "uses_variety_of_interpersonal": "uses a variety of interpersonal and group skills to achieve school goals ",
            "advises_staff": "advises staff, parents, and Ministry Officials on matters affecting the school",
            "provies_pastoral_care": "provides pastoral care to students and staff.",
            # Management
            "employs_suitable_procedures": "employs suitable procedures for recruiting and selecting staff",
            "solicits_staff_input": "solicit staff input in the deployment process",
            "deploys_teachers": "deploys teachers effectively according to their competences",
            "provides_a_working_atmosphere": "provides a working atmosphere that enables staff to perform well",
            "system_of_incentives": "establishes a system of incentives for recognizing and rewarding students, staff and other stakeholders",
            "regular_meetings_for_staff": "organizes regular meetings for staff and parents ",
            "regular_assembles": "organizes regular assembles",
            "timely_info": "ensures that information is disseminated in a timely manner.",
            # Curriculum
            "ensure_curriculum_guides": "ensures that curriculum guides and support materials are available and adequate",
            "ensures_consistent_instruction": "ensures that transition in instruction is consistent with the prescribed curriculum",
            "prescribed_subjects": "ensures that the prescribed subjects are adequately catered for in a master time-table",
            "ensure_all_aspects": "ensures that all aspects of the curriculum are taught/implemented.",
            "promotes_participation": "Promotes participation in co and extra curricular activities",
            "ensure_curriculum_modifications": "ensures that the curriculum is modified to cater for the varying needs, interests and abilities of students.",
            # Students
            "regular_student_assessment": "facilitate regular students’ assessment (school based, district, national/regional)",
            "analyses_students": "analyzes students’ performance",
            "institutes_practices": "Institutes appropriate practices for remediation",
            "ensures_teachers_eqipped": "ensures that teachers are equipped with relevant techniques for evaluating student performance.",
            # Teachers
            "conducts_periodic_appraisals": "conducts periodic appraisals of teachers",
            "provides_relevant_feedback": "provides relevant feedback for improvement",
            "provides_support_to_teachers": "provide support to individual teachers where necessary.",
            # Discipline
            "clear_guidelines_student_behaviour": "establishes clearly defined guidelines for student behavior in accordance with the Education Act.",
            "maintains_roster": "prepares and maintains roster for supervision of students",
            "order_and_discipline": "maintains order and discipline in the school",
            "uses_appropriate_sanctions": "uses appropriate sanctions for violation of school rules and regulations",
            "ensures_staff_observes_standards": "ensures that staff observes the established standards.",
            "reports_all_incidents": "Reports promptly all incidents of violence, slashed abuse and other criminal acts to the relevant authorities.",
            "maintains_accurate_documentation": "maintains accurate and up to date documentation of offenses / sanctions.",
            # Staff development
            "conducts_needs_assessment": "conducts needs assessment among staff",
            "organizes_staff_training": "organizes and facilitates staff training workshops.",
            "facilitate_staff_attendance": "facilitates staff attendance at workshops/seminars/conferences",
            "staff_training": "provides opportunities for staff members to use competences acquired at training sessions.",
            # Physical plant
            "maintenance": "ensures the proper maintenance of school property",
            "resources_on_time": "requests necessary resources on time.",
            "distributes_resources": "distributes available resources to staff as needed.",
            "safe_environment": "ensures that the school's environment is safe and secure.",
            "emergency_plan": "maintains an emergency plan",
            "inventory_of_supplies": "maintains an inventory of school supplies, equipment and furniture.",
            # Financial
            "annual_budget": "prepares and submits an annual budget",
            "school_revenue": "keeps accurate records of revenue and expenditure",
            "annual_financial_report": "prepares and submits an annual financial report",
            "report_on_time": "submits prescribed data to the Ministry of Education on time.",
            # Interpersonal relations
            "healthy_workplace": "builds and maintains a healthy working relationship with all stakeholders.",
            "respect_ideas": "Respects the ideas and opinions of staff members.",
            "cares_for_staff": "cares for staff and students",
            "manages_conflict": "manages conflicts effectively ",
            "resolves_conflict": "resolves conflicts effectively.",
            "work_and_dignity": "values the work and dignity of others.",
            "demonstrates_sensitivity": "Demonstrate sensitivity to the needs and feelings of others ",
            "maintains_confidentiality": "maintains confidentiality.",
            # Personal growth
            "education_and_research": "keeps abreast of educational development and research.",
            "supervisory_suggestions": "Accept supervisory suggestions/directives",
            "professional_training": "pursues appropriate professional training and development.",
            "ministry_standards": "Observes the standards as established by the Ministry of Education",
            "school_related_activities": "attend school and school related activities regularly.",
            "school_activities_puncutality": "Reports for school and school related activities punctually",
            "participates_organized_development": "participates in organized professional development activities",
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "principal",
            "teaching_experience_years",
            Row(
                Column("teaching_staff", css_class="form-group col-md-4 mb-0"),
                Column("ancillary_staff", css_class="form-group col-md-4 mb-0"),
                Column("administrative_staff", css_class="form-group col-md-4 mb-0"),
                css_class="form-row",
            ),
            Row(
                Column("evaluation_period_start", css_class="form-group col-md-4 mb-0"),
                Column("evaluation_period_end", css_class="form-group col-md-4 mb-0"),
                css_class="form-row",
            ),
            "last_appraisal",
            "pre_conference",
            HTML("<h5>Teaching and Learning</h5>"),
            Row(
                Column("class_visits", css_class="form-group col-md-6 mb-0"),
                Column("class_observation", css_class="form-group col-md-6 mb-0"),
                Column("teacher_reviews", css_class="form-group col-md-6 mb-0"),
                Column("conducts_lessons", css_class="form-group col-md-6 mb-0"),
                Column(
                    "ensures_literacy_improvement", css_class="form-group col-md-6 mb-0"
                ),
                Column("student_achivevement", css_class="form-group col-md-6 mb-0"),
                Column("class_supervision", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
            HTML("<h5>Planning and organization</h5>"),
            Row(
                Column("school_development_plan", css_class="form-group col-md-6 mb-0"),
                Column("smart_objectives", css_class="form-group col-md-6 mb-0"),
                Column("annual_work_plan", css_class="form-group col-md-6 mb-0"),
                Column("submits_to_ministry", css_class="form-group col-md-6 mb-0"),
                Column("plan_implementation", css_class="form-group col-md-6 mb-0"),
                Column("master_time_table", css_class="form-group col-md-6 mb-0"),
                Column("time_table_available", css_class="form-group col-md-6 mb-0"),
                Column(
                    "ensure_teacher_comply_time_table",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column("prepare_annual_report", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
            HTML("<h5>Leadership</h5>"),
            Row(
                Column("involves_staff", css_class="form-group col-md-6 mb-0"),
                Column("facilitates_parental", css_class="form-group col-md-6 mb-0"),
                Column("inspires_and_motivates", css_class="form-group col-md-6 mb-0"),
                Column(
                    "uses_variety_of_interpersonal",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column("advises_staff", css_class="form-group col-md-6 mb-0"),
                Column("provies_pastoral_care", css_class="form-group col-md-6 mb-0"),
            ),
            HTML("<h5>Management</h5>"),
            Row(
                Column(
                    "employs_suitable_procedures", css_class="form-group col-md-6 mb-0"
                ),
                Column("solicits_staff_input", css_class="form-group col-md-6 mb-0"),
                Column("deploys_teachers", css_class="form-group col-md-6 mb-0"),
                Column(
                    "provides_a_working_atmosphere",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column("system_of_incentives", css_class="form-group col-md-6 mb-0"),
                Column(
                    "regular_meetings_for_staff", css_class="form-group col-md-6 mb-0"
                ),
                Column("regular_assembles", css_class="form-group col-md-6 mb-0"),
                Column("timely_info", css_class="form-group col-md-6 mb-0"),
            ),
            HTML("<h5>Curriculum</h5>"),
            Row(
                Column(
                    "ensure_curriculum_guides", css_class="form-group col-md-6 mb-0"
                ),
                Column(
                    "ensures_consistent_instruction",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column("prescribed_subjects", css_class="form-group col-md-6 mb-0"),
                Column("ensure_all_aspects", css_class="form-group col-md-6 mb-0"),
                Column("promotes_participation", css_class="form-group col-md-6 mb-0"),
                Column(
                    "ensure_curriculum_modifications",
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            HTML("<h5>Student Assessment</h5>"),
            Row(
                Column(
                    "regular_student_assessment", css_class="form-group col-md-6 mb-0"
                ),
                Column("analyses_students", css_class="form-group col-md-6 mb-0"),
                Column("institutes_practices", css_class="form-group col-md-6 mb-0"),
                Column(
                    "ensures_teachers_eqipped", css_class="form-group col-md-6 mb-0"
                ),
            ),
            HTML("<h5>Teacher Assessment</h5>"),
            Row(
                Column(
                    "conducts_periodic_appraisals", css_class="form-group col-md-6 mb-0"
                ),
                Column(
                    "provides_relevant_feedback", css_class="form-group col-md-6 mb-0"
                ),
                Column(
                    "provides_support_to_teachers", css_class="form-group col-md-6 mb-0"
                ),
            ),
            HTML("<h5>Discipline</h5>"),
            Row(
                Column(
                    "clear_guidelines_student_behaviour",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column("maintains_roster", css_class="form-group col-md-6 mb-0"),
                Column("order_and_discipline", css_class="form-group col-md-6 mb-0"),
                Column(
                    "uses_appropriate_sanctions", css_class="form-group col-md-6 mb-0"
                ),
                Column(
                    "ensures_staff_observes_standards",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column("reports_all_incidents", css_class="form-group col-md-6 mb-0"),
                Column(
                    "maintains_accurate_documentation",
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            HTML("<h5>Staff Development</h5>"),
            Row(
                Column(
                    "conducts_needs_assessment", css_class="form-group col-md-6 mb-0"
                ),
                Column(
                    "organizes_staff_training", css_class="form-group col-md-6 mb-0"
                ),
                Column(
                    "facilitate_staff_attendance", css_class="form-group col-md-6 mb-0"
                ),
                Column("staff_training", css_class="form-group col-md-6 mb-0"),
            ),
            HTML("<h5>Physical Plant</h5>"),
            Row(
                Column("maintenance", css_class="form-group col-md-6 mb-0"),
                Column("resources_on_time", css_class="form-group col-md-6 mb-0"),
                Column("distributes_resources", css_class="form-group col-md-6 mb-0"),
                Column("safe_environment", css_class="form-group col-md-6 mb-0"),
                Column("emergency_plan", css_class="form-group col-md-6 mb-0"),
                Column("inventory_of_supplies", css_class="form-group col-md-6 mb-0"),
            ),
            HTML("<h5>Financial Management</h5>"),
            Row(
                Column("annual_budget", css_class="form-group col-md-6 mb-0"),
                Column("school_revenue", css_class="form-group col-md-6 mb-0"),
                Column("annual_financial_report", css_class="form-group col-md-6 mb-0"),
                Column("report_on_time", css_class="form-group col-md-6 mb-0"),
            ),
            HTML("<h5>Interpersonal relations</h5>"),
            Row(
                Column("healthy_workplace", css_class="form-group col-md-6 mb-0"),
                Column("respect_ideas", css_class="form-group col-md-6 mb-0"),
                Column("cares_for_staff", css_class="form-group col-md-6 mb-0"),
                Column("manages_conflict", css_class="form-group col-md-6 mb-0"),
                Column("resolves_conflict", css_class="form-group col-md-6 mb-0"),
                Column("work_and_dignity", css_class="form-group col-md-6 mb-0"),
                Column(
                    "demonstrates_sensitivity", css_class="form-group col-md-6 mb-0"
                ),
                Column(
                    "maintains_confidentiality", css_class="form-group col-md-6 mb-0"
                ),
            ),
            HTML("<h5>Personal Growth</h5>"),
            Row(
                Column("education_and_research", css_class="form-group col-md-6 mb-0"),
                Column("supervisory_suggestions", css_class="form-group col-md-6 mb-0"),
                Column("professional_training", css_class="form-group col-md-6 mb-0"),
                Column("ministry_standards", css_class="form-group col-md-6 mb-0"),
                Column(
                    "school_related_activities", css_class="form-group col-md-6 mb-0"
                ),
                Column(
                    "school_activities_puncutality",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "participates_organized_development",
                    css_class="form-group col-md-6 mb-0",
                ),
            ),
            HTML("<h5>Comments</h5>"),
            "principals_comments",
            "district_education_officer_comments",
            "chief_education_officer_comments",
            Submit('submit', 'Submit')
        )


class TeacherAppraisalForm(forms.ModelForm):
    class Meta:
        model = TeacherAppraisal
        fields = "__all__"

        widgets = {
            "evaluation_period_start": TextInput(attrs={"type": "date"}),
            "evaluation_period_end": TextInput(attrs={"type": "date"}),
            "last_appraisal": TextInput(attrs={"type": "date"}),
            # Comments
            "strengths": Textarea(attrs={"rows": 3, "cols": 20}),
            "area_of_development": Textarea(attrs={"rows": 3, "cols": 20}),
            "appraiser_comments": Textarea(attrs={"rows": 3, "cols": 20}),
            "teacher_comments": Textarea(attrs={"rows": 3, "cols": 20}),
            "district_officer_comments": Textarea(attrs={"rows": 3, "cols": 20}),
            "district_officer_recommendations": Textarea(attrs={"rows": 3, "cols": 20}),
        }
        labels = {
            # Planning and organization
            "prepares_work": "Prepares and submits schemes of work related to the scope and sequence of the curriculum",
            "prepares_lesson_plans": "Prepares lesson plans",
            "lesson_plan_order": "Prepares lesson plans that are well laid out and sequenced",
            "objectives_clear": "Writes objectives that are clear",
            "objectives_appropriate": "Writes objectives that are level appropriate",
            "objectives_achievable": "Selects objectives that are achievable",
            "content": "Prepares content that is a good match for the objectives",
            "good_judgement": "Demonstrates sound judgment in decision-making.",
            "plans_activities": "Plans activities that are well differentiated",
            "prepares_individual_instruction": "Prepares instruction with opportunities for individual work.",
            "prepares_group_instruction": "Prepares instruction with opportunities for group work.",
            "subtible_material": "Prepares materials that are usable in the setting.",
            "adequate_material": "Prepares instructional materials that are adequate",
            "includes_timing": "Includes timing as an integral part of the planning",
            "well_organized": "Is well organized for lesson presentation.",
            "prepares_exercises": "Prepares assessment exercises to monitor students’ learning",
            # Instructional
            "welcomes_class": "Welcomes/ settles the class appropriately.",
            "objectives_explicit": "Makes objectives explicit to students at the start of the lesson.",
            "engages_student": "Engages students in activities that are appropriate. ",
            "engages_students_meaningfully": "Engages students in activities that are meaningful.",
            "encourages_student": "Engages students in activities that encourage them to think",
            "awareness_of_student": "Demonstrates an awareness of students’ levels of performance.",
            "teachers_in_harmony": "Teaches in harmony with objectives",
            "teaching_strategies": "Uses a variety of teaching strategies to enhance learning",
            "grasp_of_subject": "Demonstrates a good grasp of the subject matter",
            "presents_correct_information": "Presents correct information",
            "arouses_students_interest": "Arouses and maintains students’ interest",
            "appropriate_instructional_material": "Uses appropriate instructional material in the teaching/learning environment.",
            "appropriate_questionting": "Uses appropriate questioning techniques",
            "student_opportunities": "Gives students opportunities to respond to questions",
            "student_participation": "Ensures that all students participate in instructional activities",
            "effective_use_of_structures": "Makes effective use of a variety of organizational structures (whole class, small groups, pairs, one-on-one).",
            "guides_stduent_to_develop": "Guides students to develop concepts/ master skills.",
            "presents_instruction_logically": "Presents instruction in a logical and coherent manner",
            "ends_lessons": "Ends lessons appropriately",
            "achieves_objectives": "Achieves instructional objectives.",
            # Assessment
            "clear_comms": "Communicates clear criteria/standards for assessment to students.",
            "assess_activities": "Uses appropriate assessment activities to monitor students performance ",
            "designs_assessmnet": "Designs assessment exercises at the appropriate level(s) of difficulty",
            "regular_assessment": "Regularly assesses during lesson to ascertain students’ understanding",
            "corrective_feedback": "Provides corrective feedback during the course of the lesson",
            "accurate_records": "Maintains accurate records of students’ performance",
            "monitors_student_progress": "Frequently monitors each students’ progress",
            "timely_feedback_to_students": "Provides timely feedback to students on their performance",
            "timely_feedback_to_parents": "Provides timely feedback to parents on students’ performance.",
            "results_of_assessment": "Takes appropriate action based on results of assessments.",
            # Professionalism
            "express_themselves": "Expresses himself / herself clearly and is easily understood. ",
            "arrives_work_on_time": "arrives for lessons on time ",
            "arrives_lesson_on_time": "arrives for work on time",
            "reports_regularly": "reports for work regularly ",
            "ensures_safety": "ensures the safety of all students",
            "trustworthy": "is trustworthy",
            "demonstrates_maturity": "demonstrates maturity in dealing with students ",
            "sound_judgement": "Demonstrates sound judgment in decision-making",
            "seeks_opportunitiy": "Seeks opportunities for his/her Professional Development",
            "participates_development": "Participates in professional Development",
            "demonstrates_leadership": "demonstrates leadership skills in the performance of duties",
            "contribute_to_activities": "Contribute To the life of the school including co-curricular activities.",
            "submits_required_info": "Submits required information (reports, data, etc) on time",
            "adhere_code_of_ethics": "adheres to the code of ethics",
            # Interpersonal
            "enourages_students": "Encourages students to respect the worth and dignity of others.",
            "offers_advise": "offers advice to others (principal, colleagues, students, parents)",
            "accepts_advice": "accepts advice from others (principal, colleagues, students, parents)",
            "is_cooperative": "Is co-operative and works well with staff members",
            "demonstrates_sensitvity": "demonstrates sensitivity To opinions, attitudes, and feelings of others",
            "comms_students": "Communicates effectively with students.",
            "comms_colleagues": "Communicates effectively with colleagues",
            "comms_principal": "Communicates effectively with Principal",
            "comms_support_staff": "Communicates effectively with support / ancillary staff ",
            "comms_parents": "Communicates effectively with parents ",
            "good_rapport_students": "Maintains a good rapport with Students",
            "good_rapport_principal": "Maintains a good rapport with Principal ",
            "good_rapport_colleagues": "Maintains a good rapport with colleagues",
            "good_rapport_support_staff": "Maintains a good rapport with support / ancillary staff ",
            "good_rapport_parents": "Maintains a good rapport with parents ",
            # Class management
            "demonstrates_awareness": "demonstrates an awareness  of what is happening in the classroom.",
            "creates_atmosphere": "creates an atmosphere conducive to learning ",
            "student_behaviour": "deals effectively with students’ behavior. ",
            "fair_with_students": "Is Fair in dealing with students ",
            "manages_time": "manages time effectively ",
            "manages_learning_resources": "manages and utilizes learning resources effectively ",
            "manages_effectively": "manages effectively Classroom-Related activities, assignments, projects, field trips, etc. ",
            "ensures_students_rules": "ensures that students observe the rules for classroom activities and students’ behavior",
            "effective_transition": "demonstrates effective transition from one activity to another during instruction",
            "class_register": "takes a class register ",
            "accurate_records": "keeps accurate and relevant student records",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "teacher",
            Row(
                Column("year", css_class="form-group col-md-6 mb-0"),
                Column(
                    "teaching_experience_years", css_class="form-group col-md-6 mb-0"
                ),
            ),
            Row(
                Column("evaluation_period_start", css_class="form-group col-md-6 mb-0"),
                Column("evaluation_period_end", css_class="form-group col-md-6 mb-0"),
                Column("last_appraisal", css_class="form-group col-md-6 mb-0"),
            ),
            HTML("<h5>Planning and organization</h5>"),
            Row(
                Column("prepares_work", css_class="form-group col-md-6 mb-0"),
                Column("prepares_lesson_plans", css_class="form-group col-md-6 mb-0"),
                Column("lesson_plan_order", css_class="form-group col-md-6 mb-0"),
                Column("objectives_clear", css_class="form-group col-md-6 mb-0"),
                Column("objectives_appropriate", css_class="form-group col-md-6 mb-0"),
                Column("objectives_achievable", css_class="form-group col-md-6 mb-0"),
                Column("content", css_class="form-group col-md-6 mb-0"),
                Column("good_judgement", css_class="form-group col-md-6 mb-0"),
                Column("plans_activities", css_class="form-group col-md-6 mb-0"),
                Column(
                    "prepares_individual_instruction",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "prepares_group_instruction", css_class="form-group col-md-6 mb-0"
                ),
                Column("subtible_material", css_class="form-group col-md-6 mb-0"),
                Column("adequate_material", css_class="form-group col-md-6 mb-0"),
                Column("includes_timing", css_class="form-group col-md-6 mb-0"),
                Column("well_organized", css_class="form-group col-md-6 mb-0"),
                Column("prepares_exercises", css_class="form-group col-md-6 mb-0"),
            ),
            HTML("<h5>Instructional Process</h5>"),
            Row(
                Column("welcomes_class", css_class="form-group col-md-6 mb-0"),
                Column("objectives_explicit", css_class="form-group col-md-6 mb-0"),
                Column("engages_student", css_class="form-group col-md-6 mb-0"),
                Column(
                    "engages_students_meaningfully",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column("encourages_student", css_class="form-group col-md-6 mb-0"),
                Column("awareness_of_student", css_class="form-group col-md-6 mb-0"),
                Column("teachers_in_harmony", css_class="form-group col-md-6 mb-0"),
                Column("teaching_strategies", css_class="form-group col-md-6 mb-0"),
                Column("grasp_of_subject", css_class="form-group col-md-6 mb-0"),
                Column(
                    "presents_correct_information", css_class="form-group col-md-6 mb-0"
                ),
                Column(
                    "arouses_students_interest", css_class="form-group col-md-6 mb-0"
                ),
                Column(
                    "appropriate_instructional_material",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column(
                    "appropriate_questionting", css_class="form-group col-md-6 mb-0"
                ),
                Column("student_opportunities", css_class="form-group col-md-6 mb-0"),
                Column("student_participation", css_class="form-group col-md-6 mb-0"),
                Column(
                    "effective_use_of_structures", css_class="form-group col-md-6 mb-0"
                ),
                Column(
                    "guides_stduent_to_develop", css_class="form-group col-md-6 mb-0"
                ),
                Column(
                    "presents_instruction_logically",
                    css_class="form-group col-md-6 mb-0",
                ),
                Column("ends_lessons", css_class="form-group col-md-6 mb-0"),
                Column("achieves_objectives", css_class="form-group col-md-6 mb-0"),
            ),
            HTML("<h5>Assessment</h5>"),
            Row(
                Column("clear_comms", css_class="form-group col-md-6 mb-0"),
                Column("assess_activities", css_class="form-group col-md-6 mb-0"),
                Column("designs_assessmnet", css_class="form-group col-md-6 mb-0"),
                Column("regular_assessment", css_class="form-group col-md-6 mb-0"),
                Column("corrective_feedback", css_class="form-group col-md-6 mb-0"),
                Column("accurate_records", css_class="form-group col-md-6 mb-0"),
                Column(
                    "monitors_student_progress", css_class="form-group col-md-6 mb-0"
                ),
                Column(
                    "timely_feedback_to_students", css_class="form-group col-md-6 mb-0"
                ),
                Column(
                    "timely_feedback_to_parents", css_class="form-group col-md-6 mb-0"
                ),
                Column("results_of_assessment", css_class="form-group col-md-6 mb-0"),
            ),
            HTML("<h5>Professionalism</h5>"),
            Row(
                Column("express_themselves", css_class="form-group col-md-6 mb-0"),
                Column("arrives_work_on_time", css_class="form-group col-md-6 mb-0"),
                Column("arrives_lesson_on_time", css_class="form-group col-md-6 mb-0"),
                Column("reports_regularly", css_class="form-group col-md-6 mb-0"),
                Column("ensures_safety", css_class="form-group col-md-6 mb-0"),
                Column("trustworthy", css_class="form-group col-md-6 mb-0"),
                Column("demonstrates_maturity", css_class="form-group col-md-6 mb-0"),
                Column("sound_judgement", css_class="form-group col-md-6 mb-0"),
                Column("seeks_opportunitiy", css_class="form-group col-md-6 mb-0"),
                Column(
                    "participates_development", css_class="form-group col-md-6 mb-0"
                ),
                Column("demonstrates_leadership", css_class="form-group col-md-6 mb-0"),
                Column(
                    "contribute_to_activities", css_class="form-group col-md-6 mb-0"
                ),
                Column("submits_required_info", css_class="form-group col-md-6 mb-0"),
                Column("adhere_code_of_ethics", css_class="form-group col-md-6 mb-0"),
            ),
            HTML("<h5>Interpersonal Relationships</h5>"),
            Row(
                Column("enourages_students", css_class="form-group col-md-6 mb-0"),
                Column("offers_advise", css_class="form-group col-md-6 mb-0"),
                Column("accepts_advice", css_class="form-group col-md-6 mb-0"),
                Column("is_cooperative", css_class="form-group col-md-6 mb-0"),
                Column("demonstrates_sensitvity", css_class="form-group col-md-6 mb-0"),
                Column("comms_students", css_class="form-group col-md-6 mb-0"),
                Column("comms_colleagues", css_class="form-group col-md-6 mb-0"),
                Column("comms_principal", css_class="form-group col-md-6 mb-0"),
                Column("comms_parents", css_class="form-group col-md-6 mb-0"),
                Column("good_rapport_students", css_class="form-group col-md-6 mb-0"),
                Column("good_rapport_principal", css_class="form-group col-md-6 mb-0"),
                Column("good_rapport_colleagues", css_class="form-group col-md-6 mb-0"),
                Column(
                    "good_rapport_support_staff", css_class="form-group col-md-6 mb-0"
                ),
                Column("good_rapport_parents", css_class="form-group col-md-6 mb-0"),
            ),
            HTML("<h5>Class management</h5>"),
            Row(
                Column("demonstrates_awareness", css_class="form-group col-md-6 mb-0"),
                Column("creates_atmosphere", css_class="form-group col-md-6 mb-0"),
                Column("student_behaviour", css_class="form-group col-md-6 mb-0"),
                Column("fair_with_students", css_class="form-group col-md-6 mb-0"),
                Column("manages_time", css_class="form-group col-md-6 mb-0"),
                Column(
                    "manages_learning_resources", css_class="form-group col-md-6 mb-0"
                ),
                Column("manages_effectively", css_class="form-group col-md-6 mb-0"),
                Column("ensures_students_rules", css_class="form-group col-md-6 mb-0"),
                Column("effective_transition", css_class="form-group col-md-6 mb-0"),
                Column("class_register", css_class="form-group col-md-6 mb-0"),
                Column("accurate_records", css_class="form-group col-md-6 mb-0"),
            ),
            HTML("<h5>Comments</h5>"),
            "strengths",
            "area_of_development",
            "appraiser_comments",
            "teacher_comments",
            "district_officer_comments",
            "district_officer_recommendations",
            Submit('submit', 'Submit')
        )
