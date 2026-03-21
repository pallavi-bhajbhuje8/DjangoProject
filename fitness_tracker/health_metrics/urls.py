from django.urls import path
from . import views

app_name = 'health_metrics'

urlpatterns = [
    path('', views.metrics_list, name='list'),
    path('add/', views.metrics_create, name='create'),
    path('<int:pk>/edit/', views.metrics_edit, name='edit'),
    path('<int:pk>/delete/', views.metrics_delete, name='delete'),
]