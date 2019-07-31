from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFit

from spectator.core import app_settings


class Thumbnail(ImageSpec):
    "Base class"
    format = "JPEG"
    options = {"quality": 60}


class ListThumbnail(Thumbnail):
    "For displaying in lists of Publications, Events, etc."
    processors = [ResizeToFit(*app_settings.THUMBNAIL_LIST_SIZE)]


class ListThumbnail2x(ListThumbnail):
    """Retina version of ListThumbnail
    Generated twice the size of our set dimensions.
    """
    dimensions = [d * 2 for d in app_settings.THUMBNAIL_LIST_SIZE]
    processors = [ResizeToFit(*dimensions)]


class DetailThumbnail(Thumbnail):
    "For displaying on the detail pages of Publication, Event, etc"
    processors = [ResizeToFit(*app_settings.THUMBNAIL_DETAIL_SIZE)]


class DetailThumbnail2x(DetailThumbnail):
    """Retina version of DetailThumbnail
    Generated twice the size of our set dimensions.
    """
    dimensions = [d * 2 for d in app_settings.THUMBNAIL_DETAIL_SIZE]
    processors = [ResizeToFit(*dimensions)]


register.generator("spectator:list_thumbnail", ListThumbnail)
register.generator("spectator:list_thumbnail2x", ListThumbnail2x)
register.generator("spectator:detail_thumbnail", DetailThumbnail)
register.generator("spectator:detail_thumbnail2x", DetailThumbnail2x)
