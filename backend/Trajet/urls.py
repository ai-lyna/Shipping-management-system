from django.urls import path
from . import views

urlpatterns = [
    path('', views.trajet_data, name="Trajets"),
    path('<int:trajet_id>/', views.trajet_id_view, name="Trajets/id"),
    path('<int:trajet_id>/edit/', views.update_trajet, name="Trajets/edit"),
    path('create/', views.create_trajet, name="Trajets/create"),
    path('delete/', views.delete_trajets, name="Trajets/delete"),
    path('info/', views.trajet_info, name="Trajets/info"),
]
