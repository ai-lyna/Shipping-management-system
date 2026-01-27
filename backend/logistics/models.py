from django.db import models

class Chauffeur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    numPermis = models.CharField(max_length=50, unique=True)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    disponibilite = models.BooleanField(default=True)
    # FIXED: Changed from 'Adress' to 'Adresse'
    adresse = models.TextField()

    def __str__(self):
        return self.nom + '-'+ self.prenom

class Vehicule(models.Model):
    ETAT = [
            ('Dispo', 'Disponible'),
            ('maint', 'Maintenance'),
            ('onRoute', 'On Route'),
        ]
    numImmat = models.CharField(max_length=20, unique=True)
    type_vehicule = models.CharField(max_length=50)
    capacitePoids = models.FloatField()
    capaciteVolume = models.FloatField()
    consommationCarburant = models.FloatField()
    disponibilite = models.CharField(max_length=50, choices = ETAT, default='Dispo')

    def __str__(self):
        return self.numImmat