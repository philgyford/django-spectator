from django.db import models

from spectator.fields import NaturalSortField, PersonNaturalSortField,\
        PersonDisplayNaturalSortField


class TitleModel(models.Model):
    title = models.CharField(max_length=255)
    title_sort = NaturalSortField('title')


class PersonModel(models.Model):
    name = models.CharField(max_length=255)
    name_sort = PersonNaturalSortField('name')
    name_sort_display = PersonDisplayNaturalSortField('name')

