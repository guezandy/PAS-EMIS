# Generated by Django 3.1.7 on 2021-05-10 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('historical_surveillance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cee',
            name='test_yr',
            field=models.IntegerField(null=True),
        ),
    ]
