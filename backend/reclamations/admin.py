from django.contrib import admin
from .models import Reclamation

@admin.register(Reclamation)
class ReclamationAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'statut', 'date_reclamation')
    list_filter = ('statut',)
    search_fields = ('client__nom', 'objet')