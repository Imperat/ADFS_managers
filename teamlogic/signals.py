from django.db.models import signals
from django.dispatch import receiver

import models

@receiver(signals.pre_save, sender=models.Tournament)
def alert_kefal(sender, **kwargs):
    pass