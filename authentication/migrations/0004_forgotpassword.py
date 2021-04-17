# Generated by Django 3.1.7 on 2021-04-13 03:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        (
            "authentication",
            "0003_districteducationofficer_earlychildhoodeducator_evaluationadmin_externalaccessor_schooladministrator",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="ForgotPassword",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="auth.user",
                    ),
                ),
                ("code", models.CharField(max_length=50)),
            ],
        ),
    ]
