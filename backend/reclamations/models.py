from django.db import models
from backend.clients.models import Client
from backend.incidents.models import Incident
from backend.manageExpedition.models import Expedition

class Reclamation(models.Model):
    STATUT = [
        ('en_cours', 'En cours'),
        ('resolue', 'Résolue'),
        ('annulee', 'Annulée'),
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='reclamations')
    incident = models.ForeignKey(Incident, on_delete=models.SET_NULL, related_name='reclamations', null=True)
    expedition = models.ForeignKey(Expedition, on_delete=models.SET_NULL, related_name='reclamations', null=True)
    facture = models.ForeignKey('manageExpedition.Facture', on_delete=models.SET_NULL, related_name='reclamations', null=True)
    objet = models.CharField(max_length=200)
    description = models.TextField()
    date_reclamation = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT, default='en_cours')
    
    def __str__(self):
        return f"#{self.id} - {self.client.nom}"