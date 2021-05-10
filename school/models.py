import datetime
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from authentication.models.permissions import Teaching
from historical_surveillance.models import District, School
from authentication.models.users import Teacher, SchoolPrincipal
from emis.permissions import CustomPermissionModel
from historical_surveillance.models import SEX_CHOICES


class Student(models.Model):
    def current_year():
        return datetime.date.today().year

    external_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=100)
    middle_initial = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    sex = models.CharField(choices=SEX_CHOICES, max_length=20)

    date_of_birth = models.DateField(max_length=8)
    religion = models.CharField(max_length=100, blank=True, null=True)
    home_address = models.CharField(max_length=100)

    last_school_attended = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        null=True,
        related_name="last_school",
        blank=True,
    )
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)
    graduation_year = models.PositiveIntegerField(default=current_year())
    device_access = models.BooleanField(default=False)
    is_device_personal = models.BooleanField(default=False)
    steady_internet = models.BooleanField(default=False)
    type_of_device = models.CharField(
        max_length=30,
        choices=(
            ("phone", "Phone"),
            ("tablet", "Tablet"),
            ("laptop/computer", "Laptop / Computer"),
        ),
        null=True,
        blank=True,
    )

    father_name = models.CharField(max_length=100, blank=True, null=True)
    father_work_telephone = models.CharField(max_length=100, blank=True, null=True)
    father_home_telephone = models.CharField(max_length=100, blank=True, null=True)
    father_email = models.CharField(max_length=100, blank=True, null=True)
    father_occupation = models.CharField(max_length=100, blank=True, null=True)
    father_home_address = models.CharField(max_length=100, blank=True, null=True)

    mother_name = models.CharField(max_length=100, blank=True, null=True)
    mother_work_telephone = models.CharField(max_length=100, blank=True, null=True)
    mother_home_telephone = models.CharField(max_length=100, blank=True, null=True)
    mother_email = models.CharField(max_length=100, blank=True, null=True)
    mother_occupation = models.CharField(max_length=100, blank=True, null=True)
    mother_home_address = models.CharField(max_length=100, blank=True, null=True)

    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_work_telephone = models.CharField(max_length=100, blank=True, null=True)
    guardian_home_telephone = models.CharField(max_length=100, blank=True, null=True)
    guardian_email = models.CharField(max_length=100, blank=True, null=True)
    guardian_occupation = models.CharField(max_length=100, blank=True, null=True)
    guardian_home_address = models.CharField(max_length=100, blank=True, null=True)

    doctor_name = models.CharField(max_length=100, blank=True, null=True)
    doctor_contact = models.CharField(max_length=100, blank=True, null=True)

    existing_medication = models.CharField(max_length=255, blank=True, null=True)
    existing_allergies = models.CharField(max_length=255, blank=True, null=True)
    dietary_requirements = models.CharField(max_length=255, blank=True, null=True)

    # Additional freeform questions
    home_supervision = models.CharField(max_length=255, blank=True, null=True)
    parent_help = models.CharField(max_length=255, blank=True, null=True)
    discipline_history = models.CharField(max_length=255, blank=True, null=True)
    special_needs = models.CharField(max_length=255, blank=True, null=True)
    interests_talents = models.CharField(max_length=255, blank=True, null=True)
    clubs_or_sports = models.CharField(max_length=255, blank=True, null=True)
    improvements_requested = models.CharField(max_length=255, blank=True, null=True)
    school_expectations = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Ex: Capstone course - has 1 teacher 1 subject a schedule and many students
class Course(models.Model):
    subject_name = models.CharField(max_length=255, blank=True, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    students = models.ManyToManyField(Student)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.subject_name}"


class CourseOutcome(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    # Grade
    grade = models.DecimalField(max_digits=4, decimal_places=2)
    # Attendance
    days_absent = models.IntegerField(null=True, blank=True)
    # Notes
    notes = models.CharField(max_length=550, null=True, blank=True)

    class Meta(CustomPermissionModel.Meta):
        unique_together = ("course", "student")

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} |{self.course.subject_name} | Grade: {self.grade} Attendance: {self.days_absent}"


APPRAISAL_CHOICES = (
    (5, "(A)"),
    (4, "(VO)"),
    (3, "(O)"),
    (2, "(SO)"),
    (1, "(SE)"),
    (0, "(N)"),
)


class PrincipalAppraisal(models.Model):
    principal = models.ForeignKey(SchoolPrincipal, on_delete=models.CASCADE, null=True)

    teaching_experience_years = models.IntegerField()
    teaching_staff = models.IntegerField()
    ancillary_staff = models.IntegerField()
    administrative_staff = models.IntegerField()
    evaluation_period_start = models.DateField(max_length=8)
    evaluation_period_end = models.DateField(max_length=8)
    last_appraisal = models.DateField(max_length=8)

    pre_conference = models.BooleanField(default=False)

    # Teaching and learning
    class_visits = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    class_observation = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    teacher_reviews = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    conducts_lessons = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    ensures_literacy_improvement = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )
    student_achivevement = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    class_supervision = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)

    # Planning and organization
    school_development_plan = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    smart_objectives = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    annual_work_plan = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    submits_to_ministry = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    plan_implementation = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    master_time_table = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    time_table_available = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    ensure_teacher_comply_time_table = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )
    prepare_annual_report = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)

    # leadership
    involves_staff = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    facilitates_parental = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    inspires_and_motivates = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    uses_variety_of_interpersonal = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )
    advises_staff = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    provies_pastoral_care = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)

    # management
    employs_suitable_procedures = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )
    solicits_staff_input = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    deploys_teachers = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    provides_a_working_atmosphere = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )
    system_of_incentives = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    regular_meetings_for_staff = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )
    regular_assembles = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    timely_info = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)

    # Curriculum
    ensure_curriculum_guides = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    ensures_consistent_instruction = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )
    prescribed_subjects = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    ensure_all_aspects = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    promotes_participation = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    ensure_curriculum_modifications = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )

    # Student Assessment
    regular_student_assessment = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )
    analyses_students = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    institutes_practices = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    ensures_teachers_eqipped = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)

    # Teachers
    conducts_periodic_appraisals = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )
    provides_relevant_feedback = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )
    provides_support_to_teachers = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )

    # Discipline
    clear_guidelines_student_behaviour = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )
    maintains_roster = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    order_and_discipline = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    uses_appropriate_sanctions = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )
    ensures_staff_observes_standards = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )
    reports_all_incidents = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    maintains_accurate_documentation = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )

    # Staff devvelopment
    conducts_needs_assessment = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )
    organizes_staff_training = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    facilitate_staff_attendance = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )
    staff_training = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)

    # Physical plant
    maintenance = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    resources_on_time = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    distributes_resources = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    safe_environment = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    emergency_plan = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    inventory_of_supplies = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)

    # Financial management
    annual_budget = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    school_revenue = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    annual_financial_report = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    report_on_time = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)

    # Interpersonal relations
    healthy_workplace = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    respect_ideas = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    cares_for_staff = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    manages_conflict = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    resolves_conflict = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    work_and_dignity = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    demonstrates_sensitivity = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    maintains_confidentiality = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )

    # Personal growth
    education_and_research = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    supervisory_suggestions = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    professional_training = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    ministry_standards = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    school_related_activities = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )
    school_activities_puncutality = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )
    participates_organized_development = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )

    # Comments
    principals_comments = models.CharField(max_length=1024)
    district_education_officer_comments = models.CharField(max_length=1024)
    chief_education_officer_comments = models.CharField(max_length=1024)

    def __str__(self):
        return f"{self.principal.first_name} {self.principal.last_name} appraisal"


class TeacherAppraisal(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    year = models.IntegerField()

    teaching_experience_years = models.IntegerField()
    evaluation_period_start = models.DateField(max_length=8)
    evaluation_period_end = models.DateField(max_length=8)
    last_appraisal = models.DateField(max_length=8)

    # Planning and organization
    prepares_work = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    prepares_lesson_plans = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    lesson_plan_order = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    objectives_clear = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    objectives_appropriate = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    objectives_achievable = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    content = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    good_judgement = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    plans_activities = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    prepares_individual_instruction = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )
    prepares_group_instruction = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )
    subtible_material = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    adequate_material = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    includes_timing = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    well_organized = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    prepares_exercises = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)

    # Instructional Process
    welcomes_class = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    objectives_explicit = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    engages_student = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    engages_students_meaningfully = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )
    encourages_student = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    awareness_of_student = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    teachers_in_harmony = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    teaching_strategies = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    grasp_of_subject = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)

    presents_correct_information = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )
    arouses_students_interest = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )
    appropriate_instructional_material = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )
    appropriate_questionting = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    student_opportunities = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    student_participation = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    effective_use_of_structures = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )
    guides_stduent_to_develop = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )
    presents_instruction_logically = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )
    ends_lessons = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    achieves_objectives = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)

    # Assessment
    clear_comms = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    assess_activities = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    designs_assessmnet = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    regular_assessment = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    corrective_feedback = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    accurate_records = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    monitors_student_progress = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )
    timely_feedback_to_students = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )
    timely_feedback_to_parents = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )
    results_of_assessment = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)

    # Professionalism
    express_themselves = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    arrives_work_on_time = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    arrives_lesson_on_time = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    reports_regularly = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    ensures_safety = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    trustworthy = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    demonstrates_maturity = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    sound_judgement = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    seeks_opportunitiy = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    participates_development = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    demonstrates_leadership = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    contribute_to_activities = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    submits_required_info = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    adhere_code_of_ethics = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)

    # Interpersonal Relationships
    enourages_students = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    offers_advise = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    accepts_advice = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    is_cooperative = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    demonstrates_sensitvity = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    comms_students = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    comms_colleagues = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    comms_principal = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    comms_support_staff = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    comms_parents = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    good_rapport_students = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    good_rapport_principal = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    good_rapport_colleagues = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    good_rapport_support_staff = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )
    good_rapport_parents = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)

    # Class management
    demonstrates_awareness = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    creates_atmosphere = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    student_behaviour = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    fair_with_students = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    manages_time = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    manages_learning_resources = models.IntegerField(
        choices=APPRAISAL_CHOICES, default=3
    )
    manages_effectively = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    ensures_students_rules = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    effective_transition = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    class_register = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)
    accurate_records = models.IntegerField(choices=APPRAISAL_CHOICES, default=3)

    # Comments
    strengths = models.CharField(max_length=1024, default="")
    area_of_development = models.CharField(max_length=1024, default="")
    appraiser_comments = models.CharField(max_length=1024, default="")
    teacher_comments = models.CharField(max_length=1024, default="")
    district_officer_comments = models.CharField(max_length=1024, default="")
    district_officer_recommendations = models.CharField(max_length=1024, default="")

    class Meta(CustomPermissionModel.Meta):
        unique_together = ("teacher", "year")

    def __str__(self):
        return f"{self.teacher.first_name} {self.teacher.last_name} appraisal"
