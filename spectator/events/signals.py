from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import EventRole


@receiver(post_delete, sender=EventRole, dispatch_uid='spectator.delete.event_role')
@receiver(post_save, sender=EventRole, dispatch_uid='spectator.save.event_role')
def eventrole_changed(sender, **kwargs):
    """
    When an Event's creators are changed we want to re-save the Event
    itself so that its title_sort can be recreated if necessary
    """
    kwargs['instance'].event.save()

