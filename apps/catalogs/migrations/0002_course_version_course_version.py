# Generated by Django 5.0.1 on 2024-01-10 09:02

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalogs", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("level", models.CharField(max_length=100)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="courses", to="catalogs.product"
                    ),
                ),
            ],
            options={
                "verbose_name": "3. Курс",
                "verbose_name_plural": "3. Курсы",
            },
        ),
        migrations.CreateModel(
            name="Version",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("length", models.CharField(max_length=100)),
                ("certificate", models.CharField(max_length=100)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="versions", to="catalogs.product"
                    ),
                ),
            ],
            options={
                "verbose_name": "Версия курса (стандарт / расширенная)",
                "verbose_name_plural": "Версии курса (стандарт / расширенная)",
            },
        ),
        migrations.CreateModel(
            name="Course_version",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("price", models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="course_versions",
                        to="catalogs.course",
                    ),
                ),
                (
                    "version",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="course_versions",
                        to="catalogs.version",
                    ),
                ),
            ],
            options={
                "verbose_name": "конкретный курс",
                "verbose_name_plural": "конкретные курсы",
            },
        ),
    ]