from django.contrib import admin
from .models import TypeService

@admin.register(TypeService)
class TypeServiceAdmin(admin.ModelAdmin):
    list_display = ('typeService',)