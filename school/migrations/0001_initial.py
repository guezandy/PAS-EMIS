# Generated by Django 3.1.7 on 2021-04-30 17:05

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
        ('historical_surveillance', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubjectGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('subject_group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='school.subjectgroup')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_key', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('middle_initial', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('sex', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], max_length=20, null=True)),
                ('date_of_birth', models.DateField(max_length=8)),
                ('religion', models.CharField(blank=True, max_length=100, null=True)),
                ('home_address', models.CharField(blank=True, max_length=100, null=True)),
                ('graduation_year', models.PositiveIntegerField(default=2021)),
                ('father_name', models.CharField(blank=True, max_length=100, null=True)),
                ('father_work_telephone', models.CharField(blank=True, max_length=100, null=True)),
                ('father_home_telephone', models.CharField(blank=True, max_length=100, null=True)),
                ('father_email', models.CharField(blank=True, max_length=100, null=True)),
                ('father_occupation', models.CharField(blank=True, max_length=100, null=True)),
                ('father_home_address', models.CharField(blank=True, max_length=100, null=True)),
                ('mother_name', models.CharField(blank=True, max_length=100, null=True)),
                ('mother_work_telephone', models.CharField(blank=True, max_length=100, null=True)),
                ('mother_home_telephone', models.CharField(blank=True, max_length=100, null=True)),
                ('mother_email', models.CharField(blank=True, max_length=100, null=True)),
                ('mother_occupation', models.CharField(blank=True, max_length=100, null=True)),
                ('mother_home_address', models.CharField(blank=True, max_length=100, null=True)),
                ('guardian_name', models.CharField(blank=True, max_length=100, null=True)),
                ('guardian_work_telephone', models.CharField(blank=True, max_length=100, null=True)),
                ('guardian_home_telephone', models.CharField(blank=True, max_length=100, null=True)),
                ('guardian_email', models.CharField(blank=True, max_length=100, null=True)),
                ('guardian_occupation', models.CharField(blank=True, max_length=100, null=True)),
                ('guardian_home_address', models.CharField(blank=True, max_length=100, null=True)),
                ('doctor_name', models.CharField(blank=True, max_length=100, null=True)),
                ('doctor_contact', models.CharField(blank=True, max_length=100, null=True)),
                ('existing_medication', models.CharField(blank=True, max_length=255, null=True)),
                ('existing_allergies', models.CharField(blank=True, max_length=255, null=True)),
                ('dietary_requirements', models.CharField(blank=True, max_length=255, null=True)),
                ('home_supervision', models.CharField(blank=True, max_length=255, null=True)),
                ('parent_help', models.CharField(blank=True, max_length=255, null=True)),
                ('discipline_history', models.CharField(blank=True, max_length=255, null=True)),
                ('special_needs', models.CharField(blank=True, max_length=255, null=True)),
                ('interests_talents', models.CharField(blank=True, max_length=255, null=True)),
                ('clubs_or_sports', models.CharField(blank=True, max_length=255, null=True)),
                ('improvements_requested', models.CharField(blank=True, max_length=255, null=True)),
                ('school_expectations', models.CharField(blank=True, max_length=255, null=True)),
                ('last_school_attended', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='last_school', to='historical_surveillance.school')),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='historical_surveillance.school')),
            ],
        ),
        migrations.CreateModel(
            name='PrincipalAppraisal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teaching_experience_years', models.IntegerField()),
                ('teaching_staff', models.IntegerField()),
                ('ancillary_staff', models.IntegerField()),
                ('administrative_staff', models.IntegerField()),
                ('evaluation_period_start', models.DateField(max_length=8)),
                ('evaluation_period_end', models.DateField(max_length=8)),
                ('last_appraisal', models.DateField(max_length=8)),
                ('pre_conference', models.BooleanField(default=False)),
                ('class_visits', models.IntegerField(choices=[(5, '(A)'), (4, '(VO)'), (3, '(O)'), (2, '(SO)'), (1, '(SE)'), (0, '(N)')])),
                ('class_observation', models.IntegerField(choices=[(5, '(A)'), (4, '(VO)'), (3, '(O)'), (2, '(SO)'), (1, '(SE)'), (0, '(N)')])),
                ('teacher_reviews', models.IntegerField(choices=[(5, '(A)'), (4, '(VO)'), (3, '(O)'), (2, '(SO)'), (1, '(SE)'), (0, '(N)')])),
                ('conducts_lessons', models.IntegerField(choices=[(5, '(A)'), (4, '(VO)'), (3, '(O)'), (2, '(SO)'), (1, '(SE)'), (0, '(N)')])),
                ('ensures_literacy_improvement', models.IntegerField(choices=[(5, '(A)'), (4, '(VO)'), (3, '(O)'), (2, '(SO)'), (1, '(SE)'), (0, '(N)')])),
                ('student_achivevemnet', models.IntegerField(choices=[(5, '(A)'), (4, '(VO)'), (3, '(O)'), (2, '(SO)'), (1, '(SE)'), (0, '(N)')])),
                ('class_supervision', models.IntegerField(choices=[(5, '(A)'), (4, '(VO)'), (3, '(O)'), (2, '(SO)'), (1, '(SE)'), (0, '(N)')])),
                ('school_development_plan', models.IntegerField(choices=[(5, '(A)'), (4, '(VO)'), (3, '(O)'), (2, '(SO)'), (1, '(SE)'), (0, '(N)')])),
                ('smart_objectives', models.IntegerField(choices=[(5, '(A)'), (4, '(VO)'), (3, '(O)'), (2, '(SO)'), (1, '(SE)'), (0, '(N)')])),
                ('annual_work_plan', models.IntegerField(choices=[(5, '(A)'), (4, '(VO)'), (3, '(O)'), (2, '(SO)'), (1, '(SE)'), (0, '(N)')])),
                ('submits_to_ministry', models.IntegerField(choices=[(5, '(A)'), (4, '(VO)'), (3, '(O)'), (2, '(SO)'), (1, '(SE)'), (0, '(N)')])),
                ('plan_implementation', models.IntegerField(choices=[(5, '(A)'), (4, '(VO)'), (3, '(O)'), (2, '(SO)'), (1, '(SE)'), (0, '(N)')])),
                ('master_time_table', models.IntegerField(choices=[(5, '(A)'), (4, '(VO)'), (3, '(O)'), (2, '(SO)'), (1, '(SE)'), (0, '(N)')])),
                ('time_table_available', models.IntegerField(choices=[(5, '(A)'), (4, '(VO)'), (3, '(O)'), (2, '(SO)'), (1, '(SE)'), (0, '(N)')])),
                ('ensure_teacher_comply_time_table', models.IntegerField(choices=[(5, '(A)'), (4, '(VO)'), (3, '(O)'), (2, '(SO)'), (1, '(SE)'), (0, '(N)')])),
                ('prepare_annual_report', models.IntegerField(choices=[(5, '(A)'), (4, '(VO)'), (3, '(O)'), (2, '(SO)'), (1, '(SE)'), (0, '(N)')])),
                ('principals_comments', models.CharField(max_length=1024)),
                ('district_education_officer_comments', models.CharField(max_length=1024)),
                ('chief_education_officer_comments', models.CharField(max_length=1024)),
                ('principal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.schoolprincipal')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='historical_surveillance.school')),
                ('students', models.ManyToManyField(to='school.Student')),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='school.subject')),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='school.course')),
            ],
        ),
        migrations.CreateModel(
            name='TeacherAppraisal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.teacher')),
            ],
            options={
                'unique_together': {('teacher', 'year')},
            },
        ),
        migrations.CreateModel(
            name='CourseGrade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.DecimalField(decimal_places=2, max_digits=4)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='school.course')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='school.student')),
            ],
            options={
                'unique_together': {('course', 'student')},
            },
        ),
        migrations.CreateModel(
            name='AssignmentGrade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.DecimalField(decimal_places=2, max_digits=4)),
                ('assignment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='school.assignment')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='school.student')),
            ],
            options={
                'unique_together': {('assignment', 'student')},
            },
        ),
    ]
