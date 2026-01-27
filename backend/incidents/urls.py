from django.urls import path
from . import views

urlpatterns = [
    path('', views.incident_data, name="Incidents"),
    path('<int:incident_id>/', views.incident_id_view, name="Incidents/id"),
    path('<int:incident_id>/edit/', views.update_incident, name='Incidents/edit'),
    path("create/", views.create_incident, name="Incidents/create"),
    path("delete/", views.delete_incidents, name="Incidents/delete"),
    path("info/", views.incident_info, name="Incidents/info"),
]