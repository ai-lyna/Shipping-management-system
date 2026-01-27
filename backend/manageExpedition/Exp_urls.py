from django.urls import path
from . import Exp_views as views

urlpatterns = [
    path('', views.expedition_data, name="Expeditions"),
    path('<int:expedition_id>/', views.expedition_id_view, name="Expeditions/id"),
    path('<int:expedition_id>/edit/', views.update_expedition, name='Expeditions/edit'),
    path("create/", views.create_expedition, name="Expeditions/create"),
    path("delete/", views.delete_expeditions, name="Expeditions/delete"),
    path("info/", views.expedition_info, name="Expeditions/info"),
]