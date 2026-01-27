from django.contrib import admin
from .models import Colis

@admin.register(Colis)
class ColisAdmin(admin.ModelAdmin):
    list_display = ('id', 'poids', 'volume', 'description', 'id_exp')