from django.urls import path
from . import views

urlpatterns = [
    path('', views.colis_data, name="Colis"),
    path('<int:colis_id>/', views.colis_id_view, name="Colis/id"),
    path('<int:colis_id>/edit/', views.update_colis, name='Colis/edit'),
    path("create/", views.create_colis, name="Colis/create"),
    path("delete/", views.delete_colis, name="Colis/delete"),
    path("info/", views.colis_info, name="Colis/info"),
]