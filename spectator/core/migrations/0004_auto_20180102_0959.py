# Generated by Django 2.0 on 2018-01-02 09:59

from django.conf import settings
from django.db import migrations, models
from hashids import Hashids


def generate_slug(value):
    "A copy of spectator.core.models.SluggedModelMixin._generate_slug()"
    alphabet = "abcdefghijkmnopqrstuvwxyz23456789"
    salt = "Django Spectator"

    if hasattr(settings, "SPECTATOR_SLUG_ALPHABET"):
        alphabet = settings.SPECTATOR_SLUG_ALPHABET

    if hasattr(settings, "SPECTATOR_SLUG_SALT"):
        salt = settings.SPECTATOR_SLUG_SALT

    hashids = Hashids(alphabet=alphabet, salt=salt, min_length=5)

    return hashids.encode(value)


def set_slug(apps, schema_editor):
    """
    Create a slug for each Creator already in the DB.
    """
    Creator = apps.get_model("spectator_core", "Creator")

    for c in Creator.objects.all():
        c.slug = generate_slug(c.pk)
        c.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [
        ("spectator_core", "0003_set_creator_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="creator",
            name="slug",
            field=models.SlugField(blank=True, max_length=10),
        ),
        migrations.RunPython(set_slug),
    ]
