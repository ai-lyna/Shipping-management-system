from django.contrib import admin
from .models import Incident

@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('id', 'incident_type', 'tour', 'date_reported', 'resolu')
    list_filter = ('incident_type', 'resolu')