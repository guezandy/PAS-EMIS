# Generated by Django 3.1.7 on 2021-05-03 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('historical_surveillance', '0003_merge_20210502_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='school_code',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
