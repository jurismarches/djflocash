from django.db.models import signals
from django.dispatch import receiver

from . import models


@receiver(signals.pre_save, sender=models.Notification)
def link_payement(sender, **kwargs):
    """try to link notification to payement
    """
    obj = kwargs['instance']
    if obj.payement is None:
        obj.payement = obj.find_payement()
