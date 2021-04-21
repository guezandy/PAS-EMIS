# Generated by Django 3.1.7 on 2021-04-21 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20210420_2335'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolprincipal',
            name='date_of_birth',
            field=models.DateField(blank=True, max_length=8, null=True),
        ),
        migrations.AddField(
            model_name='schoolprincipal',
            name='qualifications',
            field=models.CharField(blank=True, choices=[('Ph.D', 'Ph.D'), ("Master's Degree", "Master's Degree"), ("Bachelor's Degree", "Bachelor's Degree"), ("Bachelor's Degree in Education", "Bachelor's Degree in Education"), ('Associate Degree in Education', 'Associate Degree in Education'), ('Diploma in Education', 'Diploma in Education'), ('Associate Degree in Teacher Education (Primary)', 'Associate Degree in Teacher Education (Primary)'), ('Certificate in Management', 'Certificate in Management'), ("2 or more 'A' Levels", "2 or more 'A' Levels"), ("1 'A' Level", "1 'A' Level"), ("5 or more 'O' Levels/CXC general", "5 or more 'O' Levels/CXC general")], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='schoolprincipal',
            name='sex',
            field=models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='schoolprincipal',
            name='status',
            field=models.CharField(blank=True, choices=[('permanent', 'permanent'), ('probation', 'probation'), ('acting', 'acting')], max_length=20, null=True),
        ),
    ]
