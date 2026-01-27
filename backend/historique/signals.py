from django.db.models.signals import post_save
from django.dispatch import receiver

from backend.manageExpedition.models import Expedition
from .models import Historique


@receiver(post_save, sender=Expedition)
def create_historique_on_expedition_create(sender, instance, created, **kwargs):
    if created:
        Historique.objects.create(
            client=instance.client,
            expedition=instance
        )
