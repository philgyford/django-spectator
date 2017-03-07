from urllib.parse import urlparse

from django import template
from django.utils.html import format_html

register = template.Library()


@register.filter
def domain_urlize(value):
    """
    Returns an HTML link to the supplied URL, but only using the domain as the
    text.

    e.g. if `my_url` is 'http://www.example.org/foo/' then:

        {{ my_url|domain_urlize }}

    returns:
        <a href="http://www.example.org/foo/" rel="nofollow">www.example.org</a>
    """
    parsed_uri = urlparse(value)
    domain = '{uri.netloc}'.format(uri=parsed_uri)
    return format_html('<a href="{}" rel="nofollow">{}</a>',
            value,
            domain
        )

