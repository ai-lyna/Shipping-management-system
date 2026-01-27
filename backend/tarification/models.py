from django.db import models
from backend.manageDestination.models import Destination
from backend.typeservice.models import TypeService

class Tarification(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='tarifications')
    service = models.ForeignKey(TypeService, on_delete=models.CASCADE, related_name='tarifications')
    tarifPoids = models.DecimalField(max_digits=10, decimal_places=2)
    tarifVolume = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        unique_together = ['destination', 'service']
    
    def __str__(self):
        return f"Tarif {self.service.typeService} -> {self.destination.ville}"