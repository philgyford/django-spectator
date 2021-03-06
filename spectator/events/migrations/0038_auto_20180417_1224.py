# Generated by Django 2.0 on 2018-04-17 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("spectator_events", "0037_exhibition_to_museum"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="kind",
            field=models.CharField(
                choices=[
                    ("cinema", "Cinema"),
                    ("concert", "Concert"),
                    ("comedy", "Comedy"),
                    ("dance", "Dance"),
                    ("museum", "Gallery/Museum"),
                    ("gig", "Gig"),
                    ("theatre", "Theatre"),
                    ("misc", "Other"),
                ],
                help_text="Used to categorise event. But any kind of Work can be added to any kind of Event.",  # noqa: E501
                max_length=20,
            ),
        ),
    ]
