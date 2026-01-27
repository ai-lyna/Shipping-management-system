from django.urls import path
from . import views

urlpatterns = [
    path('', views.reclamation_data, name="Reclamations"),
    path('<int:reclamation_id>/', views.reclamation_id_view, name="Reclamations/id"),
    path('<int:reclamation_id>/edit/', views.update_reclamation, name='Reclamations/edit'),
    path("create/", views.create_reclamation, name="Reclamations/create"),
    path("delete/", views.delete_reclamations, name="Reclamations/delete"),
    path("info/", views.reclamation_info, name="Reclamations/info"),
]