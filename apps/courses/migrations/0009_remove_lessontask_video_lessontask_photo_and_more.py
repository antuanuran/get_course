# Generated by Django 4.1.13 on 2024-02-21 08:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("holder", "0004_rename_video_videoholder"),
        ("courses", "0008_alter_category_options_alter_course_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="lessontask",
            name="video",
        ),
        migrations.AddField(
            model_name="lessontask",
            name="photo",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="holder.imageholder",
            ),
        ),
        migrations.AddField(
            model_name="lessontaskanswer",
            name="video",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="holder.videoholder",
            ),
        ),
        migrations.AddField(
            model_name="useranswer",
            name="photo",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="holder.imageholder",
            ),
        ),
    ]
