from django.urls import path
from . import views


urlpatterns = [
    path('', views.payment_data, name="Payment"),
    path('<int:payment_id>/', views.payment_id_view, name="Payment/id"),
    path('<int:payment_id>/edit/', views.update_payment, name='Payment/edit'),
    path("create/", views.create_payment, name="Payment/create"),
    path("delete/", views.delete_payment, name="Payment/delete"),
    path("info/", views.payment_info, name="Payment/info"),
]
