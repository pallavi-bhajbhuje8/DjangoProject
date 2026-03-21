from django.urls import path
from . import views

app_name = 'goals'

urlpatterns = [
    path('', views.goal_list, name='list'),
    path('add/', views.goal_create, name='create'),
    path('<int:pk>/edit/', views.goal_edit, name='edit'),
    path('<int:pk>/delete/', views.goal_delete, name='delete'),
]