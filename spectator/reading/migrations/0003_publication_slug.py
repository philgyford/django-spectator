# Generated by Django 1.11 on 2017-11-01 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("spectator_reading", "0002_publicationseries_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="publication",
            name="slug",
            field=models.SlugField(blank=True, default="a", max_length=10),
            preserve_default=False,
        ),
    ]
