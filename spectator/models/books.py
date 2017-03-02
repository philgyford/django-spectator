from django.db import models

from . import BaseRole, Creator, TimeStampedModelMixin


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
        verbose_name_plural = 'Book series'

    def __str__(self):
        return self.title


class BookRole(BaseRole):
    """
    Linking a creator to a book, optionally via their role (e.g. 'Author',
    'Editor', etc.)
    """
    creator = models.ForeignKey('Creator', blank=False,
                            on_delete=models.CASCADE, related_name='book_roles')

    book = models.ForeignKey('Book', on_delete=models.CASCADE,
                                                    related_name='book_roles')


class Book(TimeStampedModelMixin, models.Model):
    """
    Not just books, but magazines etc too.

    Get a Book's creators:

        book = Book.objects.get(pk=1)

        # Just the creators:
        for creator in book.creators.all():
            print(creator.name)

        # Include their roles:
        for role in book.book_roles.all():
            print(role.book, role.creator, role.role_name)
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

    creators = models.ManyToManyField(Creator, through='BookRole',
                                                        related_name='books')

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class Reading(TimeStampedModelMixin, models.Model):
    """
    A period when a Book was read.
    """
    # Via https://www.flickr.com/services/api/misc.dates.html
    DATE_GRANULARITIES = (
        # (0, 'Y-m-d H:i:s'),
        (3, 'Y-m-d'),
        (4, 'Y-m'),
        (6, 'Y'),
        # (8, 'Circa...'),
    )

    book = models.ForeignKey('Book', null=False, blank=False)

    start_date = models.DateField(null=True, blank=True)
    start_granularity = models.PositiveSmallIntegerField(null=False,
            blank=False, default=3, choices=DATE_GRANULARITIES)
    end_date = models.DateField(null=True, blank=True)
    end_granularity = models.PositiveSmallIntegerField(null=False,
            blank=False, default=3, choices=DATE_GRANULARITIES)
    is_finished = models.BooleanField(default=False,
            help_text="Did you finish the book?")

    class Meta:
        ordering = ('end_date',)

    def __str__(self):
        return '{} ({} to {})'.format(self.book, self.start_date, self.end_date)

