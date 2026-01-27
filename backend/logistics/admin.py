from django.contrib import admin
from .models import Chauffeur, Vehicule

@admin.register(Chauffeur)
class ChauffeurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom','telephone', 'email', 'numPermis', 'disponibilite')
    list_filter = ('disponibilite',)

@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('numImmat', 'type_vehicule', 'disponibilite', 'capacitePoids' ,'capaciteVolume', 'consommationCarburant')
    list_filter = ('disponibilite', 'type_vehicule')