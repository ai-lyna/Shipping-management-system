from django.contrib import admin
from .models import Historique

@admin.register(Historique)
class HistoriqueAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'expedition', 'date_deposition')