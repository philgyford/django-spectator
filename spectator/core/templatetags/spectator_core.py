from urllib.parse import urlparse

from django import template
from django.http import QueryDict
from django.urls import reverse
from django.utils.html import format_html

from ..apps import spectator_apps

register = template.Library()


@register.simple_tag
def get_enabled_apps():
    """
    Returns a list of the optional Spectator apps that are currently installed
    and enabled. e.g. `['events', 'reading',]`.
    """
    return spectator_apps.enabled()


@register.filter
def get_item(dictionary, key):
    """
    For getting an item from a dictionary in a template using a variable.
    Use like:
        {{ mydict|get_item:my_var }}
    """
    return dictionary.get(key)


@register.inclusion_tag('spectator_core/includes/card_change_object_link.html')
def change_object_link_card(obj, perms):
    """
    If the user has permission to change `obj`, show a link to its Admin page.
    obj -- An object like Movie, Play, ClassicalWork, Publication, etc.
    perms -- The `perms` object that it's the template.
    """
    # eg: 'movie' or 'classicalwork':
    name = obj.__class__.__name__.lower()
    permission = 'spectator.can_edit_{}'.format(name)
    # eg: 'admin:events_classicalwork_change':
    change_url_name = 'admin:{}_{}_change'.format(obj._meta.app_label, name)

    return {
        'display_link': (permission in perms),
        'change_url': reverse(change_url_name, args=[obj.id])
    }


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
