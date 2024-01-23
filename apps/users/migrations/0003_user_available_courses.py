# Generated by Django 5.0.1 on 2024-01-18 07:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0002_course_favourites_course_is_sellable"),
        ("purchases", "0001_initial"),
        ("users", "0002_alter_user_managers"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="available_courses",
            field=models.ManyToManyField(
                blank=True, related_name="users", through="purchases.Purchase", to="courses.course"
            ),
        ),
    ]
