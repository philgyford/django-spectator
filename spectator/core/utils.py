from django.utils.html import strip_tags
from django.utils.text import Truncator


def truncate_string(text, strip_html=True, chars=255, truncate='…', at_word_boundary=False):
    """Truncate a string to a certain length, removing line breaks and mutliple
    spaces, optionally removing HTML, and appending a 'truncate' string.

    Keyword arguments:
    strip_html -- boolean.
    chars -- Number of characters to return.
    at_word_boundary -- Only truncate at a word boundary, which will probably
        result in a string shorter than chars.
    truncate -- String to add to the end.
    """
    if strip_html:
        text = strip_tags(text)
    text = text.replace('\n', ' ').replace('\r', '')
    text = ' '.join(text.split())
    if at_word_boundary:
        if len(text) > chars:
            text = text[:chars].rsplit(' ', 1)[0] + truncate
    else:
        text = Truncator(text).chars(chars, html=False, truncate=truncate)
    return text


def chartify(qs, score_field, cutoff=0, ensure_chartiness=True):
    """
    Given a QuerySet it will go through and add a `chart_position` property to
    each object returning a list of the objects.

    If adjacent objects have the same 'score' (based on `score_field`) then
    they will have the same `chart_position`. This can then be used in
    templates for the `value` of <li> elements in an <ol>.

    By default any objects with a score of 0 or less will be removed.

    By default, if all the items in the chart have the same position, no items
    will be returned (it's not much of a chart).

    Keyword arguments:
    qs -- The QuerySet
    score_field -- The name of the numeric field that each object in the
                   QuerySet has, that will be used to compare their positions.
    cutoff -- Any objects with a score of this value or below will be removed
              from the list. Set to None to disable this.
    ensure_chartiness -- If True, then if all items in the list have the same
                         score, an empty list will be returned.
    """
    chart = []
    position = 0
    prev_obj = None

    for counter, obj in enumerate(qs):
        score = getattr(obj, score_field)

        if score != getattr(prev_obj, score_field, None):
            position = counter + 1

        if cutoff is None or score > cutoff:
            obj.chart_position = position
            chart.append(obj)

        prev_obj = obj

    if ensure_chartiness and len(chart) > 0:
        if getattr(chart[0], score_field) == getattr(chart[-1], score_field):
            chart = []

    return chart
