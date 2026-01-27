from django.urls import path
from . import Chauffeur_views 

urlpatterns = [
    path('', Chauffeur_views.chauffeur_data, name="Chauffeurs"),
    path('<int:chauffeur_id>/', Chauffeur_views.chauffeur_id_view, name="Chauffeurs/id"),
    path('<int:chauffeur_id>/edit/', Chauffeur_views.update_chaffeur, name='Chauffeurs/edit'),
    path("create/", Chauffeur_views.create_chaffeur, name="Chauffeurs/create"),
    path("delete/", Chauffeur_views.delete_chauffeur, name="Chauffeurs/delete"),
    path("info/", Chauffeur_views.chauffeur_info, name="Chauffeurs/info"),
]
