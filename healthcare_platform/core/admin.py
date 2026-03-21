# core/admin.py

from django.contrib import admin
from .models import (
    UserProfile, DoctorProfile, MedicalHistory,
    SymptomCheck, Appointment, ClinicalNote,
    HealthMetric, Notification
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone', 'gender', 'blood_group', 'created_at']
    list_filter = ['role', 'gender', 'blood_group']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ['user_profile', 'specialty', 'license_number',
                    'years_experience', 'is_available', 'rating']
    list_filter = ['specialty', 'is_available']
    search_fields = ['user_profile__user__first_name', 'license_number']


@admin.register(SymptomCheck)
class SymptomCheckAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'urgency_level', 'status', 'created_at']
    list_filter = ['urgency_level', 'status']
    search_fields = ['symptoms', 'current_concern']
    readonly_fields = ['ai_analysis', 'ai_summary', 'ai_follow_up_questions',
                       'ai_guidance', 'ai_risk_flags']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'appointment_type',
                    'scheduled_date', 'scheduled_time', 'status']
    list_filter = ['status', 'appointment_type', 'scheduled_date']


@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ['patient', 'condition_type', 'condition_name', 'severity', 'is_active']
    list_filter = ['condition_type', 'severity', 'is_active']


@admin.register(ClinicalNote)
class ClinicalNoteAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'patient', 'created_at']
    search_fields = ['chief_complaint', 'observations']


@admin.register(HealthMetric)
class HealthMetricAdmin(admin.ModelAdmin):
    list_display = ['patient', 'metric_type', 'value', 'unit', 'recorded_at']
    list_filter = ['metric_type']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'notification_type', 'title', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read']