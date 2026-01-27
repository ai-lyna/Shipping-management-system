from django.urls import path
from . import fac_views as views

urlpatterns = [
    path('', views.facture_data, name="Factures"),
    path('<int:facture_id>/', views.facture_id_view, name="Factures/id"),
    path('<int:facture_id>/edit/', views.update_facture, name='Factures/edit'),
    path("create/", views.create_facture, name="Factures/create"),
    path("delete/", views.delete_factures, name="Factures/delete"),
    path("info/", views.facture_info, name="Factures/info"),
]