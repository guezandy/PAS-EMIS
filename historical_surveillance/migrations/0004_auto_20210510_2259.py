# Generated by Django 3.1.7 on 2021-05-11 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('historical_surveillance', '0003_auto_20210506_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='primaryperformance',
            name='above_average_scores',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='primaryperformance',
            name='tests_sat',
            field=models.IntegerField(null=True),
        ),
    ]
