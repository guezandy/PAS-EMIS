# Generated by Django 3.1.7 on 2021-04-19 15:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0003_auto_20210419_1458'),
        ('historical_surveillance', '0002_auto_20210419_1534'),
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
                ('first_name', models.CharField(max_length=100)),
                ('middle_initial', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField(max_length=8)),
                ('graduation_year', models.PositiveIntegerField(default=2021)),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='historical_surveillance.school')),
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
