# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-01 17:32
from __future__ import unicode_literals

from django.db import migrations
from spectator.core.fields import AutoSlugField


def set_slug(apps, schema_editor):
    """
    Create a slug for each Venue already in the DB.
    """
    Venue = apps.get_model('spectator_events', 'Venue')

    # We need to use AutoSlugField's methods to generate a slug for each
    # Venue.
    asfield = AutoSlugField(populate_from='name', separator='-')
    asfield.attname = 'slug'

    for v in Venue.objects.all():
        v.slug = asfield.pre_save(v, True)
        v.save()


class Migration(migrations.Migration):

    dependencies = [
        ('spectator_events', '0003_auto_20171101_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='slug',
            field=AutoSlugField(blank=True, editable=False, null=True, populate_from='name'),
        ),
        migrations.RunPython(set_slug),
    ]