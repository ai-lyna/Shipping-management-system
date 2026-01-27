from django.urls import path
from . import Tour_views as views

urlpatterns = [
    path('', views.tournee_data, name="Tournees"),
    path('<int:tournee_id>/', views.tournee_id_view, name="Tournees/id"),
    path('<int:tournee_id>/edit/', views.update_tournee, name='Tournees/edit'),
    path("create/", views.create_tournee, name="Tournees/create"),
    path("delete/", views.delete_tournees, name="Tournees/delete"),
    path("info/", views.tournee_info, name="Tournees/info"),
]