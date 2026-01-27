from django.urls import path
from . import views

urlpatterns = [
    path('', views.typeservice_data, name="Typeservice"),
    path('<int:service_id>/', views.typeservice_id_view, name="Typeservice/id"),
    path('<int:service_id>/edit/', views.update_typeservice, name='Typeservice/edit'),
    path("create/", views.create_typeservice, name="Typeservice/create"),
    path("delete/", views.delete_typeservices, name="Typeservice/delete"),
    path("info/", views.typeservice_info, name="Typeservice/info"),
]