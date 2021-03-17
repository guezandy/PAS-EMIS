# Generated by Django 3.1.7 on 2021-03-17 17:20

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensitive_data', django_cryptography.fields.encrypt(models.CharField(max_length=50))),
                ('non_sensitive_data', models.CharField(max_length=50)),
            ],
        ),
    ]
