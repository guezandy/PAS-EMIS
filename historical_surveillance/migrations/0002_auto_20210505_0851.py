# Generated by Django 3.1.7 on 2021-05-05 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('historical_surveillance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nationalstudentteacherratio',
            name='number_of_trained_female_teachers',
            field=models.IntegerField(max_length=20),
        ),
        migrations.AlterField(
            model_name='nationalstudentteacherratio',
            name='number_of_trained_male_teachers',
            field=models.IntegerField(max_length=50),
        ),
        migrations.AlterField(
            model_name='nationalstudentteacherratio',
            name='number_of_untrained_female_teachers',
            field=models.IntegerField(max_length=20),
        ),
        migrations.AlterField(
            model_name='nationalstudentteacherratio',
            name='number_of_untrained_male_teachers',
            field=models.IntegerField(max_length=20),
        ),
        migrations.AlterField(
            model_name='nationalstudentteacherratio',
            name='total_enrollment',
            field=models.IntegerField(max_length=50),
        ),
        migrations.AlterField(
            model_name='nationalstudentteacherratio',
            name='total_number_of_teachers',
            field=models.IntegerField(max_length=20),
        ),
        migrations.CreateModel(
            name='CSEC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=255)),
                ('year', models.CharField(blank=True, max_length=255)),
                ('candidate_number', models.CharField(blank=True, max_length=255)),
                ('sex', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=255)),
                ('subject', models.CharField(blank=True, max_length=255)),
                ('proficiency', models.CharField(blank=True, max_length=255)),
                ('profile1', models.CharField(blank=True, max_length=255)),
                ('profile2', models.CharField(blank=True, max_length=255)),
                ('profile3', models.CharField(blank=True, max_length=255)),
                ('profile4', models.CharField(blank=True, max_length=255)),
                ('overall_grade', models.CharField(blank=True, max_length=255)),
                ('updated_at', models.DateField(auto_now_add=True, null=True)),
                ('updated_by', models.CharField(max_length=255, null=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='historical_surveillance.school')),
            ],
            options={
                'abstract': False,
                'default_permissions': (),
            },
        ),
    ]