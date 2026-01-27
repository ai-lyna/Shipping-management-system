from django.contrib import admin
from .models import Expedition, Tournee, Facture

@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):
    list_display = ('id_Exp', 'client', 'statut', 'date_exped', 'montant_total')
    list_filter = ('statut',)
    search_fields = ('id_Exp', 'client__nom')

@admin.register(Tournee)
class TourneeAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_tournee', 'chauffeur', 'vehicule')
    filter_horizontal = ('destinations',)

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'date_fact', 'montant_HT', 'montant_TTC')