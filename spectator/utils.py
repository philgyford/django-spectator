


def make_sort_name(name, kind):
    """
    Using name, returns a version for sorting.
    e.g. 'David Foster Wallace' returns 'Wallace, David Foster'.
    and 'The Long Blondes' returns 'Long Blondes, The'.
    but 'LCD Soundsystem' returns 'LCD Soundsystem'.
    name is 'person' or 'thing'.
    """
    sort_name = name
    parts = name.split(' ')

    if kind == 'thing':
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
        # Person
        suffixes = [
                    'Jr', 'Jr.', 'Sr', 'Sr.',
                    'I', 'II', 'III', 'IV', 'V',
                    ]
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

        if parts[-1] in suffixes:
            # Remove suffixes entirely, as we'll add them back on the end.
            suffix = parts[-1]
            parts = parts[0:-1] # Remove suffix from parts
            sort_name = ' '.join(parts)

        if len(parts) > 1:

            if parts[-2] in particles:
                # From ['Aa', 'Bb', 'Le', 'Cc'] to  ['Aa', 'Bb', 'Le Cc']:
                parts = parts[0:-2] + [ ' '.join(parts[-2:]) ]

            # From 'David Foster Wallace' to 'Wallace, David Foster':
            sort_name = '{}, {}'.format(parts[-1], ' '.join(parts[:-1]))

        if suffix:
            # Add it back on.
            sort_name = '{} {}'.format(sort_name, suffix)

    return sort_name

