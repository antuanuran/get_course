# Generated by Django 5.0.1 on 2024-01-11 05:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("catalogs", "0002_course_version_course_version"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="teachers",
        ),
    ]
