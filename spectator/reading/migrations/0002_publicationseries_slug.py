# Generated by Django 1.11 on 2017-11-01 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("spectator_reading", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="publicationseries",
            name="slug",
            field=models.SlugField(blank=True, default="a", max_length=10),
            preserve_default=False,
        ),
    ]
