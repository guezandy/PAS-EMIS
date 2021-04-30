# Generated by Django 3.1.7 on 2021-04-30 17:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField()),
                ('created_by', models.CharField(blank=True, max_length=255)),
                ('district_code', models.CharField(blank=True, max_length=50, unique=True)),
                ('district_name', models.CharField(max_length=50)),
                ('updated_at', models.DateField()),
                ('updated_by', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='NationalEducationCensus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=255)),
                ('academic_year', models.CharField(max_length=30)),
                ('age_3_to_4_years', models.IntegerField()),
                ('age_5_to_11_years', models.IntegerField()),
                ('age_12_to_16_years', models.IntegerField()),
                ('updated_at', models.DateField(auto_now_add=True)),
                ('updated_by', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='NationalExpenditure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=255)),
                ('academic_year', models.CharField(max_length=30)),
                ('educational_expenditure', models.CharField(max_length=50)),
                ('gdp_millions', models.CharField(max_length=50)),
                ('government_expenditure', models.CharField(max_length=50)),
                ('primary_school_expenditure', models.CharField(max_length=50)),
                ('secondary_school_expenditure', models.CharField(max_length=50)),
                ('updated_at', models.DateField(auto_now_add=True)),
                ('updated_by', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='NationalGenderEnrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=255)),
                ('academic_year', models.CharField(max_length=30)),
                ('sex', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=20)),
                ('enrollment', models.IntegerField()),
                ('category_of_school', models.CharField(choices=[('public primary', 'Public Primary'), ('public secondary', 'Public Secondary'), ('private primary', 'Private Primary'), ('private secondary', 'Private Secondary'), ('special education', 'Special Education'), ('primary', 'Primary'), ('secondary', 'Secondary')], max_length=100)),
                ('updated_at', models.DateField(auto_now_add=True)),
                ('updated_by', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='NationalStudentTeacherRatio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=255)),
                ('category_of_school', models.CharField(choices=[('public primary', 'Public Primary'), ('public secondary', 'Public Secondary'), ('private primary', 'Private Primary'), ('private secondary', 'Private Secondary'), ('special education', 'Special Education'), ('primary', 'Primary'), ('secondary', 'Secondary')], max_length=20)),
                ('academic_year', models.CharField(max_length=20)),
                ('total_enrollment', models.CharField(max_length=20)),
                ('number_of_trained_male_teachers', models.CharField(max_length=20)),
                ('number_of_trained_female_teachers', models.CharField(max_length=20)),
                ('number_of_untrained_male_teachers', models.CharField(max_length=20)),
                ('number_of_untrained_female_teachers', models.CharField(max_length=20)),
                ('total_number_of_teachers', models.CharField(max_length=20)),
                ('updated_at', models.DateField(auto_now_add=True)),
                ('updated_by', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('created_by', models.CharField(blank=True, max_length=255)),
                ('school_code', models.CharField(blank=True, max_length=50, unique=True)),
                ('school_name', models.CharField(max_length=100)),
                ('category_of_school', models.CharField(choices=[('public primary', 'Public Primary'), ('public secondary', 'Public Secondary'), ('private primary', 'Private Primary'), ('private secondary', 'Private Secondary'), ('special education', 'Special Education'), ('primary', 'Primary'), ('secondary', 'Secondary')], max_length=50)),
                ('updated_at', models.DateField(auto_now_add=True)),
                ('updated_by', models.CharField(blank=True, max_length=255)),
                ('district_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='historical_surveillance.district')),
            ],
            options={
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='SpecialEdQuest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('created_by', models.CharField(blank=True, max_length=255)),
                ('name_of_principal', models.CharField(blank=True, max_length=255)),
                ('management', models.CharField(choices=[('ministry of education', 'Ministry of Education'), ('board/council', 'Board / Council'), ('others', 'Others')], max_length=100)),
                ('ownership', models.CharField(choices=[('government', 'Government'), ('private', 'Private'), ('denominational', 'Denominational')], max_length=100)),
                ('male_enrollment', models.IntegerField(blank=True)),
                ('female_enrollment', models.IntegerField(blank=True)),
                ('total_enrollment', models.IntegerField()),
                ('number_of_non_teaching_staff', models.IntegerField(blank=True)),
                ('number_of_teaching_staff', models.IntegerField(blank=True)),
                ('type_of_school', models.CharField(choices=[('hearing impaired', 'Hearing Impaired'), ('visually Impaired', 'Visually Impaired'), ('blind', 'Blind'), ('autistic', 'Autistic'), ('physically impaired', 'Physically Impaired'), ('multiple handicaps', 'Multiple Handicaps'), ('mentally challenged', 'Mentally Challenged')], max_length=100)),
                ('playing_field', models.CharField(choices=[('community owned', 'Community Owned'), ('school owned', 'School Owned'), ('other', 'Other')], max_length=100)),
                ('academic_year', models.CharField(blank=True, max_length=50)),
                ('number_of_classes', models.IntegerField(blank=True)),
                ('number_of_classrooms', models.IntegerField(blank=True)),
                ('number_of_halls', models.IntegerField(blank=True)),
                ('number_of_single_classes_in_single_classrooms', models.IntegerField(blank=True)),
                ('number_of_classes_sharing_classrooms', models.IntegerField(blank=True)),
                ('number_of_classes_in_hall_type_space', models.IntegerField(blank=True)),
                ('maximum_enrollment_capacity_of_school', models.IntegerField(blank=True)),
                ('itinerant_enrollment', models.IntegerField(blank=True)),
                ('resource_room_enrollment', models.IntegerField(blank=True)),
                ('home_based_enrollment', models.IntegerField(blank=True)),
                ('number_of_male_students_using_glasses', models.IntegerField(blank=True)),
                ('number_of_female_students_using_glasses', models.IntegerField(blank=True)),
                ('number_of_male_students_using_hearing_aids', models.IntegerField(blank=True)),
                ('number_of_female_students_using_hearing_aids', models.IntegerField(blank=True)),
                ('number_of_male_students_using_wheel_chair', models.IntegerField(blank=True)),
                ('number_of_female_students_using_wheel_chair', models.IntegerField(blank=True)),
                ('number_of_male_students_using_crutches', models.IntegerField(blank=True)),
                ('number_of_female_students_using_crutches', models.IntegerField(blank=True)),
                ('number_of_male_students_using_walkers', models.IntegerField(blank=True)),
                ('number_of_female_students_using_walkers', models.IntegerField(blank=True)),
                ('number_of_male_students_using_prosthesis', models.IntegerField(blank=True)),
                ('number_of_female_students_using_prosthesis', models.IntegerField(blank=True)),
                ('number_of_male_students_using_arm_leg_braces', models.IntegerField(blank=True)),
                ('number_of_female_students_using_arm_leg_braces', models.IntegerField(blank=True)),
                ('specify_other_disability_name', models.CharField(blank=True, max_length=255)),
                ('specify_other_disability_male', models.IntegerField(blank=True)),
                ('specify_other_disability_female', models.IntegerField(blank=True)),
                ('updated_at', models.DateField(auto_now_add=True)),
                ('updated_by', models.CharField(max_length=255)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='historical_surveillance.school')),
            ],
            options={
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=255)),
                ('year', models.CharField(max_length=20)),
                ('category_of_school', models.CharField(choices=[('public primary', 'Public Primary'), ('public secondary', 'Public Secondary'), ('private primary', 'Private Primary'), ('private secondary', 'Private Secondary'), ('special education', 'Special Education'), ('primary', 'Primary'), ('secondary', 'Secondary')], default=None, max_length=50)),
                ('grade', models.CharField(choices=[('grade k', 'Grade k'), ('grade 1', 'Grade 1'), ('grade 2', 'Grade 2'), ('grade 3', 'Grade 3'), ('grade 4', 'Grade 4'), ('grade 5', 'Grade 5'), ('grade 6', 'Grade 6'), ('form 1', 'Form 1'), ('form 2', 'Form 2'), ('form 3', 'Form 3'), ('form 4', 'Form 4'), ('form 5', 'Form 5'), ('form 6 L1', 'Form 6 L1'), ('form 6 L2', 'Form 6 L2')], default=None, max_length=20)),
                ('enrollment', models.IntegerField(blank=True, null=True)),
                ('minimum_age', models.IntegerField(blank=True)),
                ('maximum_age', models.IntegerField(blank=True)),
                ('sex', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=20, null=True)),
                ('updated_at', models.DateField(auto_now_add=True)),
                ('updated_by', models.CharField(blank=True, max_length=255)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='historical_surveillance.district')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='historical_surveillance.school')),
            ],
            options={
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='AggregateEnrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=255)),
                ('academic_year', models.CharField(max_length=20)),
                ('category_of_school', models.CharField(choices=[('public primary', 'Public Primary'), ('public secondary', 'Public Secondary'), ('private primary', 'Private Primary'), ('private secondary', 'Private Secondary'), ('special education', 'Special Education'), ('primary', 'Primary'), ('secondary', 'Secondary')], max_length=50)),
                ('capacity_of_school', models.IntegerField()),
                ('total_enrollment', models.IntegerField()),
                ('minimum_age', models.IntegerField(blank=True)),
                ('maximum_age', models.IntegerField(blank=True)),
                ('updated_at', models.DateField(auto_now_add=True)),
                ('updated_by', models.CharField(blank=True, max_length=255)),
                ('district_of_school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='historical_surveillance.district')),
                ('name_of_school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='historical_surveillance.school')),
            ],
            options={
                'abstract': False,
                'default_permissions': (),
            },
        ),
    ]
