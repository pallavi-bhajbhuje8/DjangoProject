# core/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class UserProfile(models.Model):
    """Extended user profile for patients and doctors"""

    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Administrator'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True)
    address = models.TextField(blank=True)
    avatar_url = models.URLField(
        max_length=500,
        default='https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150&h=150&fit=crop'
    )
    emergency_contact = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profiles'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.role})"

    @property
    def age(self):
        if self.date_of_birth:
            today = timezone.now().date()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None


class DoctorProfile(models.Model):
    """Additional information for doctors"""

    SPECIALTY_CHOICES = [
        ('general', 'General Practice'),
        ('cardiology', 'Cardiology'),
        ('dermatology', 'Dermatology'),
        ('endocrinology', 'Endocrinology'),
        ('gastroenterology', 'Gastroenterology'),
        ('neurology', 'Neurology'),
        ('oncology', 'Oncology'),
        ('orthopedics', 'Orthopedics'),
        ('pediatrics', 'Pediatrics'),
        ('psychiatry', 'Psychiatry'),
        ('pulmonology', 'Pulmonology'),
        ('urology', 'Urology'),
    ]

    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='doctor_info')
    specialty = models.CharField(max_length=50, choices=SPECIALTY_CHOICES, default='general')
    license_number = models.CharField(max_length=50, unique=True)
    years_experience = models.PositiveIntegerField(default=0)
    hospital_affiliation = models.CharField(max_length=200, blank=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bio = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    total_consultations = models.PositiveIntegerField(default=0)
    photo_url = models.URLField(
        max_length=500,
        default='https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=300&h=300&fit=crop'
    )

    class Meta:
        db_table = 'doctor_profiles'
        ordering = ['-rating']

    def __str__(self):
        return f"Dr. {self.user_profile.user.get_full_name()} - {self.get_specialty_display()}"


class MedicalHistory(models.Model):
    """Patient medical history records"""

    CONDITION_TYPES = [
        ('allergy', 'Allergy'),
        ('chronic', 'Chronic Condition'),
        ('surgery', 'Past Surgery'),
        ('medication', 'Current Medication'),
        ('family', 'Family History'),
        ('lifestyle', 'Lifestyle Factor'),
    ]

    patient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='medical_history')
    condition_type = models.CharField(max_length=20, choices=CONDITION_TYPES)
    condition_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    diagnosed_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    severity = models.CharField(
        max_length=20,
        choices=[('mild', 'Mild'), ('moderate', 'Moderate'), ('severe', 'Severe')],
        default='mild'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'medical_histories'
        ordering = ['-created_at']
        verbose_name_plural = 'Medical Histories'

    def __str__(self):
        return f"{self.patient} - {self.condition_name}"


class SymptomCheck(models.Model):
    """AI symptom check sessions"""

    URGENCY_CHOICES = [
        ('low', 'Low - Self Care'),
        ('medium', 'Medium - Consult Doctor'),
        ('high', 'High - Urgent Medical Attention'),
        ('critical', 'Critical - Emergency'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending Analysis'),
        ('analyzed', 'Analyzed'),
        ('reviewed', 'Doctor Reviewed'),
        ('closed', 'Closed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='symptom_checks')
    symptoms = models.TextField(help_text="Patient-reported symptoms")
    medical_history_summary = models.TextField(blank=True)
    current_concern = models.TextField(help_text="Primary health concern")
    urgency_level = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='low')
    ai_analysis = models.JSONField(null=True, blank=True)
    ai_summary = models.TextField(blank=True)
    ai_follow_up_questions = models.JSONField(null=True, blank=True)
    ai_guidance = models.TextField(blank=True)
    ai_risk_flags = models.JSONField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='reviewed_checks'
    )
    doctor_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'symptom_checks'
        ordering = ['-created_at']

    def __str__(self):
        return f"Check {self.id} - {self.patient} ({self.urgency_level})"


class Appointment(models.Model):
    """Appointment scheduling"""

    TYPE_CHOICES = [
        ('video', 'Video Consultation'),
        ('phone', 'Phone Consultation'),
        ('in_person', 'In-Person Visit'),
        ('chat', 'Chat Consultation'),
    ]

    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='doctor_appointments')
    symptom_check = models.ForeignKey(
        SymptomCheck, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='appointments'
    )
    appointment_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='video')
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    duration_minutes = models.PositiveIntegerField(default=30)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='scheduled')
    reason = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'appointments'
        ordering = ['scheduled_date', 'scheduled_time']

    def __str__(self):
        return f"{self.patient} → {self.doctor} on {self.scheduled_date}"


class ClinicalNote(models.Model):
    """Doctor's clinical notes for a patient"""

    appointment = models.OneToOneField(
        Appointment, on_delete=models.CASCADE,
        related_name='clinical_note',
        null=True, blank=True
    )
    doctor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='clinical_notes')
    patient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='patient_notes')
    chief_complaint = models.TextField()
    observations = models.TextField(blank=True)
    assessment = models.TextField(blank=True)
    considerations = models.TextField(blank=True)
    suggested_next_steps = models.TextField(blank=True)
    follow_up_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'clinical_notes'
        ordering = ['-created_at']

    def __str__(self):
        return f"Note by {self.doctor} for {self.patient} - {self.created_at.date()}"


class HealthMetric(models.Model):
    """Patient health metrics tracking"""

    METRIC_TYPES = [
        ('blood_pressure', 'Blood Pressure'),
        ('heart_rate', 'Heart Rate'),
        ('temperature', 'Temperature'),
        ('weight', 'Weight'),
        ('blood_sugar', 'Blood Sugar'),
        ('oxygen_level', 'Oxygen Level'),
        ('bmi', 'BMI'),
    ]

    patient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='health_metrics')
    metric_type = models.CharField(max_length=20, choices=METRIC_TYPES)
    value = models.CharField(max_length=50)
    unit = models.CharField(max_length=20)
    notes = models.TextField(blank=True)
    recorded_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'health_metrics'
        ordering = ['-recorded_at']

    def __str__(self):
        return f"{self.patient} - {self.get_metric_type_display()}: {self.value} {self.unit}"


class Notification(models.Model):
    """System notifications"""

    TYPE_CHOICES = [
        ('appointment', 'Appointment'),
        ('result', 'Test Result'),
        ('reminder', 'Reminder'),
        ('alert', 'Health Alert'),
        ('system', 'System'),
    ]

    recipient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=15, choices=TYPE_CHOICES, default='system')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    action_url = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} → {self.recipient}"