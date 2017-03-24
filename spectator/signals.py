from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import ConcertRole, MiscEventRole


@receiver(post_delete, sender=ConcertRole, dispatch_uid='spectator.delete.concert_role')
@receiver(post_save, sender=ConcertRole, dispatch_uid='spectator.save.concert_role')
def concertrole_changed(sender, **kwargs):
    """
    When a Concert's creators are changed we want to re-svae the Concert
    itself so that its title_sort can be recreated if necessary
    """
    kwargs['instance'].concert.save()


@receiver(post_delete, sender=MiscEventRole, dispatch_uid='spectator.delete.misc_event_role')
@receiver(post_save, sender=MiscEventRole, dispatch_uid='spectator.save.misc_event_role')
def misceventrole_changed(sender, **kwargs):
    """
    When a MiscEvent's creators are changed we want to re-svae the MiscEvent
    itself so that its title_sort can be recreated if necessary
    """
    kwargs['instance'].miscevent.save()

