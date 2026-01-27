from django.db import models
from backend.manageExpedition.models import Tournee
from backend.Trajet.models import Trajet

class Incident(models.Model):
    TYPE_INCIDENTS = [
        ('retard', 'Retard'),
        ('retard', 'Retard'),
        ('perte', 'Perte'),
        ('dommage', 'Dommage'),
        ('technique', 'Problème technique'),
        ('autre', 'Autre'),
    ]
    incident_type = models.CharField(max_length=50, choices=TYPE_INCIDENTS)
    tour = models.ForeignKey(Tournee, on_delete=models.CASCADE, null=True, related_name='incidents')
    description = models.TextField()
    date_reported = models.DateTimeField(auto_now_add=True)
    resolu = models.BooleanField(default=False)
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE, null=True,blank=True,verbose_name="Trajet associé")

    def __str__(self):
        tour_id = self.tour.id if self.tour else "No Tour"
        return f"{self.incident_type} - Tour {tour_id}"