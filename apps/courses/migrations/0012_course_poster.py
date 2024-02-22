# Generated by Django 4.1.13 on 2024-02-22 07:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("holder", "0006_linkholder"),
        ("courses", "0011_remove_course_poster"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="poster",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="holder.imageholder",
            ),
        ),
    ]
