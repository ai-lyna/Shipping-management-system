from django.db import models

class Colis(models.Model):
    poids = models.FloatField()
    volume = models.FloatField()
    description = models.CharField(max_length=100)
    id_exp = models.ForeignKey('manageExpedition.Expedition', on_delete=models.CASCADE, related_name='colis')
    
    def __str__(self):
        return f"Colis #{self.id}"