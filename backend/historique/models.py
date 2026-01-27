from django.db import models
from backend.clients.models import Client
from backend.manageExpedition.models import Expedition

class Historique(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="historiques",
        null=True,
        blank=True
    )
    expedition = models.ForeignKey(
        Expedition,
        on_delete=models.CASCADE,
        related_name="historiques",
        null=True,
        blank=True
    )
    date_deposition = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Historique #{self.id}"