from urllib.parse import urlparse

from django import template
from django.http import QueryDict
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


@register.simple_tag(takes_context=True)
def current_url_name(context):
    """
    Returns the name of the current URL, namespaced, or False.

    Example usage:

        {% current_url_name as url_name %}

        <a href="#"{% if url_name == 'myapp:home' %} class="active"{% endif %}">Home</a>

    """
    url_name = False
    if context.request.resolver_match:
        url_name = "{}:{}".format(
                                context.request.resolver_match.namespace,
                                context.request.resolver_match.url_name
                            )
    return url_name


@register.simple_tag(takes_context=True)
def query_string(context, key, value):
    """
    For adding/replacing a key=value pair to the GET string for a URL.

    eg, if we're viewing ?p=3 and we do {% url_replace order 'taken' %}
    then this returns "p=3&order=taken"

    And, if we're viewing ?p=3&order=uploaded and we do the same thing, we get
    the same result (ie, the existing "order=uploaded" is replaced).

    Expects the request object in context to do the above; otherwise it will
    just return a query string with the supplied key=value pair.
    """
    try:
        request = context['request']
        args = request.GET.copy()
    except KeyError:
        args = QueryDict('').copy()
    args[key] = value
    return args.urlencode()


