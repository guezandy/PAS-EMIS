# Generated by Django 3.1.7 on 2021-04-21 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('historical_surveillance', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='enrollment',
            options={'default_permissions': ()},
        ),
        migrations.AlterModelOptions(
            name='nationaleducationcensus',
            options={'default_permissions': ()},
        ),
        migrations.AlterModelOptions(
            name='nationalexpenditure',
            options={'default_permissions': ()},
        ),
        migrations.AlterModelOptions(
            name='nationalgenderenrollment',
            options={'default_permissions': ()},
        ),
        migrations.AlterModelOptions(
            name='nationalstudentteacherratio',
            options={'default_permissions': ()},
        ),
        migrations.RenameField(
            model_name='nationaleducationcensus',
            old_name='age_5_to_7_years',
            new_name='age_5_to_11_years',
        ),
        migrations.AlterField(
            model_name='district',
            name='created_at',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='district',
            name='created_by',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='nationalgenderenrollment',
            name='category_of_school',
            field=models.CharField(choices=[('public primary', 'Public Primary'), ('public secondary', 'Public Secondary'), ('private primary', 'Private Primary'), ('private secondary', 'Private Secondary'), ('special education', 'Special Education'), ('primary', 'Primary'), ('secondary', 'Secondary')], max_length=100),
        ),
        migrations.AlterField(
            model_name='nationalstudentteacherratio',
            name='category_of_school',
            field=models.CharField(choices=[('public primary', 'Public Primary'), ('public secondary', 'Public Secondary'), ('private primary', 'Private Primary'), ('private secondary', 'Private Secondary'), ('special education', 'Special Education'), ('primary', 'Primary'), ('secondary', 'Secondary')], max_length=20),
        ),
        migrations.AlterField(
            model_name='school',
            name='created_by',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='school',
            name='school_name',
            field=models.CharField(max_length=100),
        ),
    ]
