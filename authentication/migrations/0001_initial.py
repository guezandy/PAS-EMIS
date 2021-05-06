# Generated by Django 3.1.7 on 2021-05-05 08:11

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('historical_surveillance', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationAccess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': [('view_school_app', 'Can view school application'), ('view_welfare_app', 'Can view welfare and supervision application'), ('view_surveillance_app', 'Can view historical surveillance application')],
                'abstract': False,
                'managed': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='DistrictAdministration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': [('create_principal_appraisal', 'Can create principal appraisals'), ('update_principal_appraisal', 'Can update principal appraisals'), ('view_principal_appraisal', 'Can view principal appraisals')],
                'abstract': False,
                'managed': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='EarlyChildhood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': [],
                'abstract': False,
                'managed': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='EvaluationAndAssessment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': [('create_accommodation_enrollment', 'Can create accommodation enrollments'), ('update_accommodation_enrollment', 'Can update accommodation enrollments'), ('view_accommodation_enrollment', 'Can view accommodation enrollments')],
                'abstract': False,
                'managed': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='ExternalAssessment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': [('create_external_assessment', 'Can create external assessment report forms'), ('update_external_assessment', 'Can update external assessment report forms'), ('view_external_assessment', 'Can view external assessment report forms')],
                'abstract': False,
                'managed': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Principal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': [('create_teacher_appraisal', 'Can create teacher appraisals'), ('update_teacher_appraisal', 'Can update teacher appraisals'), ('view_teacher_appraisal', 'Can view teacher appraisals'), ('create_vice_principal_appraisal', 'Can create vice principal appraisals'), ('update_vice_principal_appraisal', 'Can update vice principal appraisals'), ('view_vice_principal_appraisal', 'Can view vice principal appraisals')],
                'abstract': False,
                'managed': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='RestrictedSchoolAdministration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': [('create_teacher_enrollment', 'Can create teacher enrollment'), ('update_teacher_enrollment', 'Can update teacher enrollment'), ('view_teacher_enrollment', 'Can view teacher enrollment')],
                'abstract': False,
                'managed': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='SchoolAdministration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': [('create_accounting', 'Can create accounting and budgeting information'), ('update_accounting', 'Can update accounting and budgeting information'), ('view_accounting', 'Can view accounting and budgeting information'), ('create_school_activity_config', 'Can create school subjects, cocurricular, and extra-curricular activities'), ('update_school_activity_config', 'Can update school subjects, cocurricular, and extra-curricular activities'), ('view_school_activity_config', 'Can view school subjects, cocurricular, and extra-curricular activities'), ('create_student_enrollment', 'Can create student enrollment'), ('update_student_enrollment', 'Can update student enrollment'), ('view_student_enrollment', 'Can view student enrollment'), ('create_student_transfer', 'Can create student transfers'), ('update_student_transfer', 'Can update student transfers'), ('view_student_transfer', 'Can view student transfers')],
                'abstract': False,
                'managed': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='SchoolSupervision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': [('create_supervision_report', 'Can create school supervision reports'), ('update_supervision_report', 'Can update school supervision reports'), ('view_supervision_report', 'Can view school supervision reports')],
                'abstract': False,
                'managed': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='StatisticsAndPlanning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': [('create_stats_report', 'Can create aggregated data / statistical planning reports'), ('update_stats_report', 'Can update aggregated data / statistical planning reports'), ('view_stats_report', 'Can view aggregated data / statistical planning reports'), ('create_stats_data_management', 'Can create statistical data'), ('update_stats_data_management', 'Can update statistical data'), ('view_stats_data_management', 'Can view statistical data')],
                'abstract': False,
                'managed': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='SupportServices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': [('create_student_support_definition', 'Can create student support/service definitions'), ('update_student_support_definition', 'Can update student support/service definitions'), ('view_student_support_definition', 'Can view student support/service definitions'), ('create_student_resource_alloc', 'Can create student support/service allocations'), ('update_student_resource_alloc', 'Can update student support/service allocations'), ('view_student_resource_alloc', 'Can view student support/service allocations'), ('create_student_counsel_forms', 'Can create student counseling forms'), ('update_student_counsel_forms', 'Can update student counseling forms'), ('view_student_counsel_forms', 'Can view student counseling forms')],
                'abstract': False,
                'managed': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Teaching',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': [('create_student_attendance', 'Can create student attendance'), ('update_student_attendance', 'Can update student attendance'), ('view_student_attendance', 'Can view student attendance'), ('create_student_grades', 'Can create student grades'), ('update_student_grades', 'Can update student grades'), ('view_student_grades', 'Can view student grades'), ('create_student_dev_behavioral', 'Can create student developmental and behavioral data'), ('update_student_dev_behavioral', 'Can update student developmental and behavioral data'), ('view_student_dev_behavioral', 'Can view student developmental and behavioral data')],
                'abstract': False,
                'managed': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Activation',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('code', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='EvaluationAdmin',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
            ],
            options={
                'verbose_name': 'Evaluation Admin',
                'abstract': False,
                'default_permissions': (),
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ExternalAccessor',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
            ],
            options={
                'verbose_name': 'External Accessor',
                'abstract': False,
                'default_permissions': (),
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ForgotPassword',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('code', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='StatisticianAdmin',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
            ],
            options={
                'verbose_name': 'Stastician Admin',
                'abstract': False,
                'default_permissions': (),
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='SupportServicesAdmin',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
            ],
            options={
                'verbose_name': 'Support Services Admin',
                'abstract': False,
                'default_permissions': (),
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('sex', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], max_length=20, null=True)),
                ('status', models.CharField(blank=True, choices=[('permanent', 'permanent'), ('probation', 'probation'), ('acting', 'acting')], max_length=20, null=True)),
                ('home_address', models.CharField(max_length=100)),
                ('contact_number', models.CharField(blank=True, max_length=100, null=True)),
                ('date_of_birth', models.DateField(blank=True, max_length=8, null=True)),
                ('trained', models.CharField(blank=True, choices=[('trained', 'Trained'), ('untrained', 'Untrained')], max_length=100, null=True)),
                ('grade', models.CharField(max_length=100)),
                ('qualifications', models.CharField(blank=True, choices=[('Ph.D', 'Ph.D'), ("Master's Degree", "Master's Degree"), ("Bachelor's Degree", "Bachelor's Degree"), ("Bachelor's Degree in Education", "Bachelor's Degree in Education"), ('Associate Degree in Education', 'Associate Degree in Education'), ('Diploma in Education', 'Diploma in Education'), ('Associate Degree in Teacher Education (Primary)', 'Associate Degree in Teacher Education (Primary)'), ('Certificate in Management', 'Certificate in Management'), ("2 or more 'A' Levels", "2 or more 'A' Levels"), ("1 'A' Level", "1 'A' Level"), ("5 or more 'O' Levels/CXC general", "5 or more 'O' Levels/CXC general")], max_length=50, null=True)),
                ('national_insurance_number', models.CharField(blank=True, max_length=100, null=True)),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='historical_surveillance.school')),
            ],
            options={
                'verbose_name': 'Teacher',
                'abstract': False,
                'default_permissions': (),
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='SchoolSuperviser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='historical_surveillance.school')),
            ],
            options={
                'verbose_name': 'School Superviser',
                'abstract': False,
                'default_permissions': (),
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='SchoolPrincipal',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('sex', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], max_length=20, null=True)),
                ('status', models.CharField(blank=True, choices=[('permanent', 'permanent'), ('probation', 'probation'), ('acting', 'acting')], max_length=20, null=True)),
                ('date_of_birth', models.DateField(blank=True, max_length=8, null=True)),
                ('qualifications', models.CharField(blank=True, choices=[('Ph.D', 'Ph.D'), ("Master's Degree", "Master's Degree"), ("Bachelor's Degree", "Bachelor's Degree"), ("Bachelor's Degree in Education", "Bachelor's Degree in Education"), ('Associate Degree in Education', 'Associate Degree in Education'), ('Diploma in Education', 'Diploma in Education'), ('Associate Degree in Teacher Education (Primary)', 'Associate Degree in Teacher Education (Primary)'), ('Certificate in Management', 'Certificate in Management'), ("2 or more 'A' Levels", "2 or more 'A' Levels"), ("1 'A' Level", "1 'A' Level"), ("5 or more 'O' Levels/CXC general", "5 or more 'O' Levels/CXC general")], max_length=50, null=True)),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='historical_surveillance.school')),
            ],
            options={
                'verbose_name': 'Principal',
                'abstract': False,
                'default_permissions': (),
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='SchoolAdministrator',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='historical_surveillance.school')),
            ],
            options={
                'verbose_name': 'School Administrator',
                'abstract': False,
                'default_permissions': (),
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='EarlyChildhoodEducator',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='historical_surveillance.school')),
            ],
            options={
                'verbose_name': 'Early Childhood',
                'abstract': False,
                'default_permissions': (),
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='DistrictEducationOfficer',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('district', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='historical_surveillance.district')),
            ],
            options={
                'verbose_name': 'District Education Officer',
                'abstract': False,
                'default_permissions': (),
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
