from django.db import models
from backend.clients.models import Client 
from backend.manageDestination.models import Destination
from backend.logistics.models import Chauffeur, Vehicule
from backend.typeservice.models import TypeService

class Tournee(models.Model):
    date_tournee = models.DateField()
    chauffeur = models.ForeignKey(Chauffeur, on_delete=models.SET_NULL, null=True)
    vehicule = models.ForeignKey(Vehicule, on_delete=models.SET_NULL, null=True)
    destinations = models.ManyToManyField(Destination, related_name="tournees")
    
    def __str__(self):
        return f"Tournee #{self.id}"

class Facture(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="factures", null=True, blank=True)
    date_fact = models.DateField(auto_now=True)
    
    @property
    def montant_HT(self):
        exps = self.client.expeditions.all()
        montant_HT = 0 
        for e in exps:
            montant_exp = e.montant_total 
            montant_HT = montant_HT + montant_exp
        return montant_HT
    
    @property
    def montant_TTC(self):
        return (self.montant_HT * 0.19) + self.montant_HT
    
    def __str__(self):
        return f"Facture #{self.id}"

class Expedition(models.Model):
    STATUT = [
        ('trsit', 'en transit'),
        ('centri', 'en centre de tri'),
        ('encourslivr', 'en cours de livraison'),
        ('livr', 'livré'),
        ('echec', 'echec de livraison'),
    ]
    

    id_Exp = models.CharField(max_length=10, primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True, related_name="expeditions")
    type_service = models.ForeignKey(TypeService, on_delete=models.CASCADE, null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT)
    date_exped = models.DateTimeField(auto_now=True)
    numBureau = models.ForeignKey(Destination, on_delete=models.CASCADE)
    tournee = models.ForeignKey(Tournee, on_delete=models.SET_NULL, null=True, blank=True, related_name="expeditions")
    tarification = models.ForeignKey('tarification.Tarification', on_delete=models.CASCADE, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.id_Exp:
            import datetime
            last_id = Expedition.objects.count() + 1
            date_str = datetime.datetime.now().strftime('%Y%m%d')
            self.id_Exp = f"EXP-{date_str}-{last_id:04d}"
        super().save(*args, **kwargs)
    
    @property
    def montant_total(self):
        tarifBase = self.numBureau.tarifBase
        poidsTot = 0
        volumeTot = 0
        

        for colis in self.colis.all():
            poidsTot = poidsTot + colis.poids
            volumeTot = volumeTot + colis.volume
        

        if self.tarification:
            prixPoidsTot = poidsTot * self.tarification.tarifPoids
            prixVolTot = volumeTot * self.tarification.tarifVolume
            return tarifBase + prixPoidsTot + prixVolTot
        else:
   
            return tarifBase
    
    def __str__(self):
        return f"#{self.id_Exp}"