import re

from django.db import models


class NaturalSortField(models.CharField):
    """
    Using the value of another field on the model, make a version that is
    more suitable for sorting.

    * Stripped of leading/trailing spaces.
    * All lowercase.
    * Articles ("the", "a", etc) moved to the end of the string.
    * Integers heavily padded with zeros.

    e.g. "The Long Blondes" becomes "long blondes, the".
         "An Actor Prepares" becomes "actor prepares, an".
         "Le Tigre" becomes "tigre, le".
         "Vol. 2 No. 11, November 2004" becomes
             "vol. 00000002 no. 00000011, november 00002004".
    """

    description = "A string to allow more human-friendly sorting"

    def __init__(self, for_field, *args, **kwargs):
        """
        for_field - The name of the field to base this field's string on.
                    e.g. 'title' or 'name'.
        """
        self.for_field = for_field
        kwargs.setdefault('db_index', True)
        kwargs.setdefault('editable', False)
        kwargs.setdefault('max_length', 255)
        super(NaturalSortField, self).__init__(**kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        args.append(self.for_field)
        return name, path, args, kwargs

    def pre_save(self, model_instance, add):
        return self._naturalize(getattr(model_instance, self.for_field))

    def _naturalize(self, string):
        string = self._pre_naturalization(string)
        string = self._do_naturalization(string)
        string = self._post_naturalization(string)
        return string

    def _pre_naturalization(self, string):
        string = string.lower()
        string = string.strip()
        return string

    def _post_naturalization(self, string):
        return string

    def _do_naturalization(self, string):
        """
        Make a naturalized version of a general string, not a person's name.
        e.g., title of a book, a band's name, etc.

        string -- a lowercase string.
        """

        # Things we want to move to the back of the string:
        articles = [
                        'a', 'an', 'the',
                        'un', 'une', 'le', 'la', 'les', "l'", "l’",
                        'ein', 'eine', 'der', 'die', 'das',
                        'una', 'el', 'los', 'las',
                    ]

        sort_string = string
        parts = string.split(' ')

        if len(parts) > 1 and parts[0] in articles:
            # 'long blondes, the':
            sort_string = '{}, {}'.format(' '.join(parts[1:]), parts[0])

        sort_string = self._naturalize_numbers(sort_string)

        return sort_string

    def _naturalize_numbers(self, string):
        """
        Makes any integers into very zero-padded numbers.
        e.g. '1' becomes '00000001'.
        """

        def naturalize_int_match(match):
            return '%08d' % (int(match.group(0)),)

        string = re.sub(r'\d+', naturalize_int_match, string)

        return string


class PersonNaturalSortField(NaturalSortField):
    """
    Using the value of another field on the model, which should represent a
    person's name, make a version that is more suitable for sorting.

    * Stripped of leading/trailing spaces.
    * All lowercase.
    * Surnames moved to the start.
    * Integers heavily padded with zeros.

    e.g. "David Foster Wallace" becomes "wallace, david foster".
         "John Le Carre" becomes "le carre, john".
         "Daphne du Maurier" becomes "maurier, daphne du".
         "Sir Fred Bloggs Jr" becomes "bloggs, sir fred jr".
         "Prince" is "prince".
    """

    description = "A string to allow more human-friendly sorting of people's names"

    def _pre_naturalization(self, string):
        string = string.strip()
        return string

    def _post_naturalization(self, string):
        string = string.lower()
        return string

    def _do_naturalization(self, string):
        """
        Attempt to make a version of the string that has the surname, if any,
        at the start.

        'John, Brown' to 'Brown, John'
        'Sir John Brown Jr' to 'Brown, Sir John Jr'
        'Prince' to 'Prince'

        string -- The string to change.
        """
        suffixes = [
                    'Jr', 'Jr.', 'Sr', 'Sr.',
                    'I', 'II', 'III', 'IV', 'V',
                    ]
        # Add lowercase versions:
        suffixes = suffixes + [s.lower() for s in suffixes]

        # If a name has a capitalised particle in we use that to sort.
        # So 'Le Carre, John' but 'Carre, John le'.
        particles = [
                    'Le', 'La',
                    'Von', 'Van',
                    'Du', 'De',
                    ]

        surname = '' # Smith
        names = ''   # Fred James
        suffix = ''  # Jr

        sort_string = string
        parts = string.split(' ')

        if parts[-1] in suffixes:
            # Remove suffixes entirely, as we'll add them back on the end.
            suffix = parts[-1]
            parts = parts[0:-1] # Remove suffix from parts
            sort_string = ' '.join(parts)

        if len(parts) > 1:

            if parts[-2] in particles:
                # From ['Alan', 'Barry', 'Le', 'Carré']
                # to   ['Alan', 'Barry', 'Le Carré']:
                parts = parts[0:-2] + [ ' '.join(parts[-2:]) ]

            # From 'David Foster Wallace' to 'Wallace, David Foster':
            sort_string = '{}, {}'.format(parts[-1], ' '.join(parts[:-1]))

        if suffix:
            # Add it back on.
            sort_string = '{} {}'.format(sort_string, suffix)

        # In case this name has any numbers in it.
        sort_string = self._naturalize_numbers(sort_string)

        return sort_string


class PersonDisplayNaturalSortField(PersonNaturalSortField):
    """
    Using the value of another field on the model, which should represent a
    person's name, make a version that would be more suitable for sorting
    except it keeps its original case.

    So, you shouldn't use it for sorting, but it makes for a good visual
    display of the underlying sorting.

    * Stripped of leading/trailing spaces.
    * Original case.
    * Surnames moved to the start.
    * Integers heavily padded with zeros.

    e.g. "David Foster Wallace" becomes "Wallace, David Foster".
         "John Le Carre" becomes "le Carre, John".
         "Daphne du Maurier" becomes "Maurier, Daphne du".
         "Sir Fred Bloggs Jr" becomes "Bloggs, Sir Fred Jr".
         "Prince" is "Prince".
    """

    description = "A string that looks like the human-friendly person's name sorting string, but is itself more human-friendly"

    def _pre_naturalization(self, string):
        string = string.strip()
        return string

    def _post_naturalization(self, string):
        return string

