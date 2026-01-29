from django.urls import path
from . import views


urlpatterns = [
    path('', views.payment_data, name="Payments"),
    path('<int:payment_id>/', views.payment_id_view, name="Payment/id"),
    path('<int:payment_id>/edit/', views.update_payment, name='Payments/edit'),
    path("create/", views.create_payment, name="Payments/create"),
    path("delete/", views.delete_payment, name="Payments/delete"),
    path("info/", views.payment_info, name="Payments/info"),
]
