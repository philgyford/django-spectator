from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from . import TimeStampedModelMixin, Role


class BookSeries(TimeStampedModelMixin, models.Model):
    """
    A way to group 'Books' into series.
    """
    title = models.CharField(null=False, blank=False, max_length=255,
            help_text="e.g. 'The London Review of Books'.")
    url = models.URLField(null=False, blank=True, max_length=255,
            verbose_name='URL', help_text="e.g. 'https://www.lrb.co.uk/'.")

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class Book(TimeStampedModelMixin, models.Model):
    """
    Not jut books, but magazines etc too.

    A Book's creators:
        book = Book.objects.get(pk=1)
        for r in book.roles.all():
            print(r.creator, r.role_name)
    """

    KIND_CHOICES = (
        ('book', 'Book'),
        ('periodical', 'Periodical'),
    )

    title = models.CharField(null=False, blank=False, max_length=255,
            help_text="e.g. 'Aurora' or 'Vol. 39 No. 4, 16 February 2017'.")
    series = models.ForeignKey('BookSeries', blank=True, null=True,
                                                    on_delete=models.SET_NULL)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES,
                                                        default='book')
    official_url = models.URLField(null=False, blank=True, max_length=255,
            verbose_name='Official URL',
            help_text="Official URL for this book/issue.")
    isbn_gb = models.CharField(null=False, blank=True, max_length=20,
            verbose_name='UK ISBN', help_text="e.g. '0356500489'.")
    isbn_us = models.CharField(null=False, blank=True, max_length=20,
            verbose_name='US ISBN', help_text="e.g. '0316098094'.")
    notes_url = models.URLField(null=False, blank=True, max_length=255,
            verbose_name='Notes URL', help_text="URL of your notes/review.")

    roles = GenericRelation('Role', related_query_name='books')

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

