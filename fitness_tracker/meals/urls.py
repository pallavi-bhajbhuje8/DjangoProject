from django.urls import path
from . import views

app_name = 'meals'

urlpatterns = [
    path('', views.meal_list, name='list'),
    path('add/', views.meal_create, name='create'),
    path('<int:pk>/edit/', views.meal_edit, name='edit'),
    path('<int:pk>/delete/', views.meal_delete, name='delete'),
]