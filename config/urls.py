from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Clients/', include('backend.clients.urls')),
    path('Colis/', include('backend.manageColis.urls')),
    path('Chauffeurs/', include('backend.logistics.chauf_urls')),
    path('Vehicules/', include('backend.logistics.veh_urls')),
    path('Destinations/', include('backend.manageDestination.urls')),
    path('Typeservice/', include('backend.typeservice.urls')),
    path('Tarification/', include('backend.tarification.urls')),
    path('Expeditions/', include('backend.manageExpedition.Exp_urls')),
    path('Tournees/', include('backend.manageExpedition.Tour_urls')),
    path('Factures/', include('backend.manageExpedition.Fac_urls')),
    path('Incidents/', include('backend.incidents.urls')),
    path('Reclamations/', include('backend.reclamations.urls')),
    path('dashboard/', include('backend.dashboard.urls')),
]
