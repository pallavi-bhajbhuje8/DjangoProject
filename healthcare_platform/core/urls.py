# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Landing
    path('', views.landing_page, name='landing'),

    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # AI Symptom Checker
    path('symptom-checker/', views.symptom_checker, name='symptom_checker'),
    path('report/<uuid:check_id>/', views.ai_report, name='ai_report'),

    # Appointments
    path('appointments/', views.appointments_view, name='appointments'),
    path('appointments/book/', views.book_appointment, name='book_appointment'),

    # Patient Records
    path('patient-records/', views.patient_records, name='patient_records'),

    # Health Metrics
    path('health-metrics/', views.health_metrics, name='health_metrics'),

    # API
    path('api/quick-analysis/', views.api_quick_analysis, name='api_quick_analysis'),
    path('api/notification/<int:notification_id>/read/',
         views.api_mark_notification_read, name='api_notification_read'),
]