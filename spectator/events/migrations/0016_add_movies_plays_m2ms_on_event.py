# Generated by Django 2.0 on 2018-01-26 09:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("spectator_events", "0015_rename_classical_dance_on_event"),
    ]

    operations = [
        migrations.CreateModel(
            name="MovieSelection",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "order",
                    models.PositiveSmallIntegerField(
                        default=1, help_text="Position on the Event programme."
                    ),
                ),
            ],
            options={"verbose_name": "movie selection", "ordering": ("order",)},
        ),
        migrations.CreateModel(
            name="PlaySelection",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "order",
                    models.PositiveSmallIntegerField(
                        default=1, help_text="Position on the Event programme."
                    ),
                ),
            ],
            options={"verbose_name": "play selection", "ordering": ("order",)},
        ),
        migrations.AlterField(
            model_name="event",
            name="movie",
            field=models.ForeignKey(
                blank=True,
                help_text="Only used if event is of 'Movie' kind.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="old_movie",
                to="spectator_events.Movie",
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="play",
            field=models.ForeignKey(
                blank=True,
                help_text="Only used if event is of 'Play' kind.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="old_play",
                to="spectator_events.Play",
            ),
        ),
        migrations.AddField(
            model_name="playselection",
            name="event",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="play_selections",
                to="spectator_events.Event",
            ),
        ),
        migrations.AddField(
            model_name="playselection",
            name="play",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="events",
                to="spectator_events.Play",
            ),
        ),
        migrations.AddField(
            model_name="movieselection",
            name="event",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="movie_selections",
                to="spectator_events.Event",
            ),
        ),
        migrations.AddField(
            model_name="movieselection",
            name="movie",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="events",
                to="spectator_events.Movie",
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="movies",
            field=models.ManyToManyField(
                blank=True,
                help_text="Only used if event is of 'Movie' kind.",
                through="spectator_events.MovieSelection",
                to="spectator_events.Movie",
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="plays",
            field=models.ManyToManyField(
                blank=True,
                help_text="Only used if event is of 'Play' kind.",
                through="spectator_events.PlaySelection",
                to="spectator_events.Play",
            ),
        ),
    ]
