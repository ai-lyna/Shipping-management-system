from django.db import models
#from backend.clients.models import Client
from backend.manageExpedition.models import Facture 

class Payment (models.Model):
     TYPE = [
        ('total', 'Total'),
        ('partiel', 'Partiel'),
        ]
     #client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="payments")
     facture= models.ForeignKey(Facture, on_delete=models.CASCADE, related_name="payments")
     typePaiement = models.CharField(max_length=10,choices=TYPE)
     datePaiement = models.DateTimeField(auto_now=True)
     soldePaye= models.DecimalField(max_digits=7, decimal_places=2)

     
     def save(self, *args, **kwargs) :
          restant = self.facture.montant_TTC - self.soldePaye

          if self.client:
               self.client.solde = restant 
               self.client.save(update_fileds=['solde'])
        
          if self.client.solde in (None,0):
            self.typePaiement = 'Total'
          else : 
              self.typePaiement = 'Partiel'

          super().save(*args, **kwargs)

          

          