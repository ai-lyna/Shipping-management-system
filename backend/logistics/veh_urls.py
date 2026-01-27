from django.urls import path
from . import Chauffeur_views , Vehicule_views

urlpatterns = [
    path('', Vehicule_views.vehicule_data, name="Vehicules"),
    path('<int:vehicule_id>/', Vehicule_views.vehicule_id_view, name="Vehicules/id"),
    path('<int:vehicule_id>/edit/', Vehicule_views.update_vehicule, name='Vehicules/edit'),
    path("create/", Vehicule_views.create_vehicule, name="Vehicules/create"),
    path("delete/", Vehicule_views.delete_vehicule, name="Vehicules/delete"),
    path("info/", Vehicule_views.vehicule_info, name="Vehicules/info"),
]