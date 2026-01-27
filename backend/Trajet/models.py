from django.db import models
class Trajet(models.Model):
    kilometrage = models.FloatField(verbose_name="Kilométrage (km)")
    duree = models.DurationField(verbose_name="Durée")
    consommation_carb = models.FloatField(verbose_name="Consommation carburant (L)")
    
    class Meta:
        verbose_name = "Trajet"
        verbose_name_plural = "Trajets"
    
    def __str__(self):
        return f"Trajet {self.id} ({self.kilometrage} km)"