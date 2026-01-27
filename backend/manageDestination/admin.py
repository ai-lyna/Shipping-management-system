from django.contrib import admin
from .models import Destination

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('numBureau', 'ville', 'pays', 'zoneGeo', 'tarifBase')
    search_fields = ('ville', 'pays')