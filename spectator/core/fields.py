import re
import six

from django.conf import settings
from django.db import models
from django.db.models.constants import LOOKUP_SEP
from django.template.defaultfilters import slugify
from django.utils.encoding import force_text


MAX_UNIQUE_QUERY_ATTEMPTS = getattr(settings, 'EXTENSIONS_MAX_UNIQUE_QUERY_ATTEMPTS', 100)


class UniqueFieldMixin(object):
    """
    Taken from https://github.com/django-extensions/django-extensions/blob/b5404a4a5ed3a5893727b3be3d6a50bc21c534e3/django_extensions/db/fields/__init__.py
    """

    def check_is_bool(self, attrname):
        if not isinstance(getattr(self, attrname), bool):
            raise ValueError("'{}' argument must be True or False".format(attrname))

    @staticmethod
    def _get_fields(model_cls):
        return [
            (f, f.model if f.model != model_cls else None) for f in model_cls._meta.get_fields()
            if not f.is_relation or f.one_to_one or (f.many_to_one and f.related_model)
        ]

    def get_queryset(self, model_cls, slug_field):
        for field, model in self._get_fields(model_cls):
            if model and field == slug_field:
                return model._default_manager.all()
        return model_cls._default_manager.all()

    def find_unique(self, model_instance, field, iterator, *args):
        # exclude the current model instance from the queryset used in finding
        # next valid hash
        queryset = self.get_queryset(model_instance.__class__, field)
        if model_instance.pk:
            queryset = queryset.exclude(pk=model_instance.pk)

        # form a kwarg dict used to impliment any unique_together contraints
        kwargs = {}
        for params in model_instance._meta.unique_together:
            if self.attname in params:
                for param in params:
                    kwargs[param] = getattr(model_instance, param, None)

        new = six.next(iterator)
        kwargs[self.attname] = new
        while not new or queryset.filter(**kwargs):
            new = six.next(iterator)
            kwargs[self.attname] = new
        setattr(model_instance, self.attname, new)
        return new


class AutoSlugField(UniqueFieldMixin, models.SlugField):
    """ AutoSlugField

    Taken from https://github.com/django-extensions/django-extensions/blob/b5404a4a5ed3a5893727b3be3d6a50bc21c534e3/django_extensions/db/fields/__init__.py

    By default, sets editable=False, blank=True.
    Required arguments:
    populate_from
        Specifies which field, list of fields, or model method
        the slug will be populated from.
        populate_from can traverse a ForeignKey relationship
        by using Django ORM syntax:
            populate_from = 'related_model__field'
    Optional arguments:
    separator
        Defines the used separator (default: '-')
    overwrite
        If set to True, overwrites the slug on every save (default: False)
    Inspired by SmileyChris' Unique Slugify snippet:
    http://www.djangosnippets.org/snippets/690/
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('blank', True)
        kwargs.setdefault('editable', False)

        populate_from = kwargs.pop('populate_from', None)
        if populate_from is None:
            raise ValueError("missing 'populate_from' argument")
        else:
            self._populate_from = populate_from

        self.slugify_function = kwargs.pop('slugify_function', slugify)
        self.separator = kwargs.pop('separator', six.u('-'))
        self.overwrite = kwargs.pop('overwrite', False)
        self.check_is_bool('overwrite')
        self.allow_duplicates = kwargs.pop('allow_duplicates', False)
        self.check_is_bool('allow_duplicates')
        self.max_unique_query_attempts = kwargs.pop('max_unique_query_attempts', MAX_UNIQUE_QUERY_ATTEMPTS)
        super(AutoSlugField, self).__init__(*args, **kwargs)

    def _slug_strip(self, value):
        """
        Cleans up a slug by removing slug separator characters that occur at
        the beginning or end of a slug.
        If an alternate separator is used, it will also replace any instances
        of the default '-' separator with the new separator.
        """
        re_sep = '(?:-|%s)' % re.escape(self.separator)
        value = re.sub('%s+' % re_sep, self.separator, value)
        return re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)

    def slugify_func(self, content):
        if content:
            return self.slugify_function(content)
        return ''

    def slug_generator(self, original_slug, start):
        yield original_slug
        for i in range(start, self.max_unique_query_attempts):
            slug = original_slug
            end = '%s%s' % (self.separator, i)
            end_len = len(end)
            if self.slug_len and len(slug) + end_len > self.slug_len:
                slug = slug[:self.slug_len - end_len]
                slug = self._slug_strip(slug)
            slug = '%s%s' % (slug, end)
            yield slug
        raise RuntimeError('max slug attempts for %s exceeded (%s)' % (original_slug, self.max_unique_query_attempts))

    def create_slug(self, model_instance, add):
        # get fields to populate from and slug field to set
        if not isinstance(self._populate_from, (list, tuple)):
            self._populate_from = (self._populate_from, )
        slug_field = model_instance._meta.get_field(self.attname)

        if add or self.overwrite:
            # slugify the original field content and set next step to 2
            slug_for_field = lambda lookup_value: self.slugify_func(self.get_slug_fields(model_instance, lookup_value))
            slug = self.separator.join(map(slug_for_field, self._populate_from))
            start = 2
        else:
            # get slug from the current model instance
            slug = getattr(model_instance, self.attname)
            # model_instance is being modified, and overwrite is False,
            # so instead of doing anything, just return the current slug
            return slug

        # strip slug depending on max_length attribute of the slug field
        # and clean-up
        self.slug_len = slug_field.max_length
        if self.slug_len:
            slug = slug[:self.slug_len]
        slug = self._slug_strip(slug)
        original_slug = slug

        if self.allow_duplicates:
            setattr(model_instance, self.attname, slug)
            return slug

        return super(AutoSlugField, self).find_unique(
            model_instance, slug_field, self.slug_generator(original_slug, start))

    def get_slug_fields(self, model_instance, lookup_value):
        lookup_value_path = lookup_value.split(LOOKUP_SEP)
        attr = model_instance
        for elem in lookup_value_path:
            try:
                attr = getattr(attr, elem)
            except AttributeError:
                raise AttributeError(
                    "value {} in AutoSlugField's 'populate_from' argument {} returned an error - {} has no attribute {}".format(
                        elem, lookup_value, attr, elem))

        if callable(attr):
            return "%s" % attr()

        return attr

    def pre_save(self, model_instance, add):
        value = force_text(self.create_slug(model_instance, add))
        return value

    def get_internal_type(self):
        return "SlugField"

    def deconstruct(self):
        name, path, args, kwargs = super(AutoSlugField, self).deconstruct()
        kwargs['populate_from'] = self._populate_from
        if not self.separator == six.u('-'):
            kwargs['separator'] = self.separator
        if self.overwrite is not False:
            kwargs['overwrite'] = True
        if self.allow_duplicates is not False:
            kwargs['allow_duplicates'] = True
        return name, path, args, kwargs


class NaturalSortField(models.CharField):
    """
    Using the value of another field on the model, make a version that is
    more suitable for sorting.

    If the object has a `sort_as` property and that is set to `person` then
    the string will be treated as if it's a name, i.e. surname put first.

    Either way, this will be done:

    * Stripped of leading/trailing spaces.
    * All lowercase.
    * Integers heavily padded with zeros.

    And, if it's a person:

    * Surnames moved to the start.
        e.g. "David Foster Wallace" becomes "wallace, david foster".
             "John Le Carre" becomes "le carre, john".
             "Daphne du Maurier" becomes "maurier, daphne du".
             "Sir Fred Bloggs Jr" becomes "bloggs, sir fred jr".
             "Prince" is "prince".

    Or, if it's not a person:

    * Articles ("the", "a", etc) moved to the end of the string.
        e.g. "The Long Blondes" becomes "long blondes, the".
             "An Actor Prepares" becomes "actor prepares, an".
             "Le Tigre" becomes "tigre, le".
             "Vol. 2 No. 11, November 2004" becomes
                 "vol. 00000002 no. 00000011, november 00002004".

    So, use like:

        class Author(models.Model):
            name = models.CharField(max_length=255)
            name_sort = NaturalSortField('name',  max_length=255)
            sort_as = 'person'

            class Meta:
                ordering = ('name_sort',)
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
        string = getattr(model_instance, self.for_field)

        string = string.strip()

        if hasattr(model_instance, 'sort_as') and model_instance.sort_as == 'person':
            string = self.naturalize_person(string)
            # The case of the name is important, so we lowercase afterwards:
            string = string.lower()
        else:
            string = string.lower()
            string = self.naturalize_thing(string)

        return string

    def naturalize_thing(self, string):
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
            if parts[0] != parts[1]:
                # Don't do this if the name is 'The The' or 'La La Land'.
                # Makes 'long blondes, the':
                sort_string = '{}, {}'.format(' '.join(parts[1:]), parts[0])

        sort_string = self._naturalize_numbers(sort_string)

        return sort_string

    def naturalize_person(self, string):
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
    pass

class PersonDisplayNaturalSortField(NaturalSortField):
    pass
