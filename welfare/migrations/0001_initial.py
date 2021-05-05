# Generated by Django 3.1.7 on 2021-05-05 08:11

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupportService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('created_by', models.CharField(blank=True, max_length=255)),
                ('updated_at', models.DateField(auto_now_add=True)),
                ('updated_by', models.CharField(blank=True, max_length=255)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(blank=True, max_length=250)),
            ],
            options={
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='StudentSupportAssoc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('created_by', models.CharField(blank=True, max_length=255)),
                ('updated_at', models.DateField(auto_now_add=True)),
                ('updated_by', models.CharField(blank=True, max_length=255)),
                ('comment', models.CharField(blank=True, max_length=500)),
                ('start_date', models.DateField(default=datetime.date.today, max_length=8)),
                ('end_date', models.DateField(blank=True, default=None, max_length=8, null=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='welfare.supportservice')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.student')),
            ],
            options={
                'abstract': False,
                'default_permissions': (),
            },
        ),
    ]
