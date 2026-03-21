from django.urls import path
from . import views

app_name = 'workouts'

urlpatterns = [
    path('', views.workout_list, name='list'),
    path('add/', views.workout_create, name='create'),
    path('<int:pk>/', views.workout_detail, name='detail'),
    path('<int:pk>/edit/', views.workout_edit, name='edit'),
    path('<int:pk>/delete/', views.workout_delete, name='delete'),
]