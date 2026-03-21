# core/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import (
    UserProfile, DoctorProfile, MedicalHistory,
    SymptomCheck, Appointment, ClinicalNote, HealthMetric
)


class UserRegistrationForm(UserCreationForm):
    """Registration form with role selection"""

    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    ]

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'your.email@example.com'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Last Name'
        })
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': '+1 (555) 000-0000'
        })
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Choose a username'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Create a password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Confirm your password'
        })


class SymptomCheckForm(forms.Form):
    """Form for patient symptom submission"""

    symptoms = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'placeholder': 'Describe your symptoms in detail...\n\nExample: I have had a persistent headache for 3 days, mostly on the left side. It gets worse when I look at screens.',
            'rows': 5,
        }),
        label='What symptoms are you experiencing?'
    )
    medical_history = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'placeholder': 'List any relevant medical history...\n\nExample: Type 2 diabetes (diagnosed 2019), high blood pressure, taking metformin',
            'rows': 3,
        }),
        label='Relevant Medical History'
    )
    current_concern = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'placeholder': 'What is your main concern right now?\n\nExample: I\'m worried this headache might be something serious because it won\'t go away.',
            'rows': 3,
        }),
        label='What is your primary concern?'
    )
    user_type = forms.ChoiceField(
        choices=[('patient', 'Patient'), ('doctor', 'Doctor')],
        widget=forms.HiddenInput(),
        initial='patient'
    )


class AppointmentForm(forms.ModelForm):
    """Form for booking appointments"""

    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_type', 'scheduled_date', 'scheduled_time', 'reason']
        widgets = {
            'doctor': forms.Select(attrs={'class': 'form-input'}),
            'appointment_type': forms.Select(attrs={'class': 'form-input'}),
            'scheduled_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'scheduled_time': forms.TimeInput(attrs={
                'class': 'form-input',
                'type': 'time'
            }),
            'reason': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
                'placeholder': 'Briefly describe the reason for your visit'
            }),
        }


class ClinicalNoteForm(forms.ModelForm):
    """Form for doctor clinical notes"""

    class Meta:
        model = ClinicalNote
        fields = ['chief_complaint', 'observations', 'assessment',
                  'considerations', 'suggested_next_steps', 'follow_up_date']
        widgets = {
            'chief_complaint': forms.Textarea(attrs={
                'class': 'form-textarea', 'rows': 2
            }),
            'observations': forms.Textarea(attrs={
                'class': 'form-textarea', 'rows': 3
            }),
            'assessment': forms.Textarea(attrs={
                'class': 'form-textarea', 'rows': 3
            }),
            'considerations': forms.Textarea(attrs={
                'class': 'form-textarea', 'rows': 3
            }),
            'suggested_next_steps': forms.Textarea(attrs={
                'class': 'form-textarea', 'rows': 3
            }),
            'follow_up_date': forms.DateInput(attrs={
                'class': 'form-input', 'type': 'date'
            }),
        }


class HealthMetricForm(forms.ModelForm):
    """Form for recording health metrics"""

    class Meta:
        model = HealthMetric
        fields = ['metric_type', 'value', 'unit', 'notes']
        widgets = {
            'metric_type': forms.Select(attrs={'class': 'form-input'}),
            'value': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., 120/80'
            }),
            'unit': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., mmHg, bpm, °F'
            }),
            'notes': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Optional notes'
            }),
        }


class MedicalHistoryForm(forms.ModelForm):
    """Form for adding medical history entries"""

    class Meta:
        model = MedicalHistory
        fields = ['condition_type', 'condition_name', 'description',
                  'diagnosed_date', 'severity', 'is_active']
        widgets = {
            'condition_type': forms.Select(attrs={'class': 'form-input'}),
            'condition_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Type 2 Diabetes'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 2,
                'placeholder': 'Additional details...'
            }),
            'diagnosed_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'severity': forms.Select(attrs={'class': 'form-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }