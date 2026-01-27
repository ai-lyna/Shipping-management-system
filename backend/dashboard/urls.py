from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/commercial/', views.dashboard, {'tab': 'commercial'}, name="dashboard_commercial"),
    path('dashboard/operational/', views.dashboard, {'tab': 'operational'}, name="dashboard_operational"),
]
