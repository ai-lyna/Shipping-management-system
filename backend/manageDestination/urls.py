from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.destination_data, name="Destinations"),
    path('<int:numBureau>/', views.destination_id_view, name="Destinations/id"),
    path('<int:numBureau>/edit/', views.update_destination, name='Destinations/edit'),
    path("create/", views.create_destination, name="Destinations/create"),
    path("delete/", views.delete_destinations, name="Destinations/delete"),
    path("info/", views.destination_info, name="Destinations/info"),
]