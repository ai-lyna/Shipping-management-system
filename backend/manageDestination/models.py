from django.db import models

class Destination(models.Model):
    numBureau = models.IntegerField(primary_key=True)
    ville = models.CharField(max_length=30)
    pays = models.CharField(max_length=20)
    zoneGeo = models.CharField(max_length=30)
    tarifBase = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.ville + " - " + self.pays