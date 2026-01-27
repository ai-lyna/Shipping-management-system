from django.contrib import admin
from .models import Tarification

@admin.register(Tarification)
class TarificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'destination', 'service', 'tarifPoids', 'tarifVolume')
    list_filter = ('service',)