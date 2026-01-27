from django.urls import path
from . import views

urlpatterns = [
    path('', views.client_data, name="Clients"),
    path('<int:client_id>/', views.client_id_view, name="Clients/id"),
    path('<int:client_id>/edit/', views.update_client, name='Clients/edit'),
    path("create/", views.create_client, name="Clients/create"),
    path("delete/", views.delete_clients, name="Clients/delete"),
    path("info/", views.client_info, name="Clients/info"),
]
