# Generated by Django 3.0.5 on 2020-04-07 10:52

from django.db import migrations, models

import spectator.core.models


class Migration(migrations.Migration):

    dependencies = [
        ("spectator_reading", "0007_rename_cover_to_thumbnail"),
    ]

    operations = [
        migrations.AlterField(
            model_name="publication",
            name="thumbnail",
            field=models.ImageField(
                blank=True,
                default="",
                upload_to=spectator.core.models.thumbnail_upload_path,
            ),
        ),
    ]
