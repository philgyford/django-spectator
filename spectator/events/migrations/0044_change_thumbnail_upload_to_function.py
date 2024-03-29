# Generated by Django 3.0.5 on 2020-04-07 10:51

from django.db import migrations, models

import spectator.core.models


class Migration(migrations.Migration):

    dependencies = [
        ("spectator_events", "0043_rename_ticket_to_thumbnail"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="thumbnail",
            field=models.ImageField(
                blank=True,
                default="",
                upload_to=spectator.core.models.thumbnail_upload_path,
            ),
        ),
    ]
