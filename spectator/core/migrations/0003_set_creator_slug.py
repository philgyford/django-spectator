# Generated by Django 1.11 on 2017-11-01 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("spectator_core", "0002_creator_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="creator",
            name="slug",
            field=models.SlugField(blank=True, max_length=10),
        ),
    ]
