from django.urls import path
from . import views

urlpatterns = [
    path('', views.tarification_data, name="Tarifications"),
    path('<int:tarification_id>/', views.tarification_id_view, name="Tarifications/id"),
    path('<int:tarification_id>/edit/', views.update_tarification, name="Tarifications/edit"),
    path('create/', views.create_tarification, name="Tarifications/create"),
    path('delete/', views.delete_tarifications, name="Tarifications/delete"),
    path('info/', views.tarification_info, name="Tarifications/info"),
]
