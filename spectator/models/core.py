from django.db import models


class TimeStampedModelMixin(models.Model):
    "Should be mixed in to all models."
    time_created = models.DateTimeField(auto_now_add=True,
                help_text="The time this item was created in the database.")
    time_modified = models.DateTimeField(auto_now=True,
                help_text="The time this item was last saved to the database.")

    class Meta:
        abstract = True


class Creator(TimeStampedModelMixin, models.Model):
    """
    A person or a group/company/organisation that is responsible for making all
    or part of a book, play, movie, gig, etc.
    """

    KIND_CHOICES = (
        ('individual', 'Individual'),
        ('group', 'Group'),
    )

    name = models.CharField(max_length=255,
            help_text="e.g. 'Douglas Adams' or 'The Long Blondes'.")

    sort_name = models.CharField(blank=True, max_length=255,
            help_text="e.g. 'Adams, Douglas' or 'Long Blondes, The'. If left blank, will be created automatically on save.")

    kind = models.CharField(max_length=20, choices=KIND_CHOICES,
                                                        default='individual')

    def save(self, *args, **kwargs):
        if self.sort_name == '':
            self.sort_name = self._make_sort_name(self.name, self.kind)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('sort_name',)

    def _make_sort_name(self, name, kind):
        """
        Using name, returns a version for sorting.
        e.g. 'David Foster Wallace' returns 'Wallace, David Foster'.
        and 'The Long Blondes' returns 'Long Blondes, The'.
        but 'LCD Soundsystem' returns 'LCD Soundsystem'.
        name is 'individual' or 'group'.
        """
        sort_name = name
        parts = name.split(' ')

        if kind == 'group':
            articles = [
                            'a', 'an', 'the',
                            'un', 'une', 'le', 'la', 'les',
                            'ein', 'eine', 'der', 'die', 'das',
                            'una', 'el', 'los', 'las',
                        ]
            if len(parts) > 1 and parts[0].lower() in articles:
                # 'Long Blondes, The':
                sort_name = '{}, {}'.format(' '.join(parts[1:]), parts[0])

        else:
            # Individuals.
            suffixes = [
                        'Jr', 'Jr.', 'Sr', 'Sr.',
                        'I', 'II', 'III', 'IV', 'V',
                        ]
            # If a name has a capitalised particle in we use that to sort.
            # So 'Le Carre, John'
            # but 'Carre, John le'
            particles = [
                        'Le', 'La',
                        'Von', 'Van',
                        'Du', 'De',
                        ]
            surname = '' # Smith
            names = ''   # Fred Q
            suffix = ''  # Jr

            if parts[-1] in suffixes:
                # Remove suffixes entirely, as we'll add them back on the end.
                suffix = parts[-1]
                parts = parts[0:-1] # Remove suffix from parts
                sort_name = ' '.join(parts)

            if len(parts) > 1:

                if parts[-2] in particles:
                    # Turns ['Aaaa', 'Bbbb', 'Le', 'Cccc']
                    # into  ['Aaaa', 'Bbbb', 'Le Cccc']
                    parts = parts[0:-2] + [ ' '.join(parts[-2:]) ]

                # 'Faye, Alice':
                # 'Wallace, David Foster':
                sort_name = '{}, {}'.format(parts[-1], ' '.join(parts[:-1]))

            if suffix:
                # Add it back on.
                sort_name = '{} {}'.format(sort_name, suffix)

        return sort_name
