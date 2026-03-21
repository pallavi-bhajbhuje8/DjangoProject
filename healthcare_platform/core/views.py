# core/views.py

import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count, Q, Avg
from datetime import timedelta

from .models import (
    UserProfile, DoctorProfile, MedicalHistory,
    SymptomCheck, Appointment, ClinicalNote,
    HealthMetric, Notification
)
from .forms import (
    UserRegistrationForm, SymptomCheckForm,
    AppointmentForm, ClinicalNoteForm,
    HealthMetricForm, MedicalHistoryForm
)
from .ai_engine import HealthcareAIEngine


# ─────────────────────────────────────────────────────────────
# LANDING PAGE
# ─────────────────────────────────────────────────────────────

def landing_page(request):
    """Public landing page"""
    doctors = DoctorProfile.objects.filter(is_available=True).select_related(
        'user_profile__user'
    )[:6]

    stats = {
        'total_patients': UserProfile.objects.filter(role='patient').count(),
        'total_doctors': DoctorProfile.objects.count(),
        'total_consultations': Appointment.objects.filter(status='completed').count(),
        'ai_analyses': SymptomCheck.objects.count(),
    }

    features = [
        {
            'icon': '🤖',
            'title': 'AI Symptom Analysis',
            'description': 'Advanced AI engine analyzes your symptoms and provides structured health insights.',
            'image': 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1f?w=400&h=250&fit=crop',
        },
        {
            'icon': '👨‍⚕️',
            'title': 'Expert Doctors',
            'description': 'Connect with board-certified physicians across multiple specialties.',
            'image': 'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=400&h=250&fit=crop',
        },
        {
            'icon': '📋',
            'title': 'Smart Medical Records',
            'description': 'Structured clinical notes and health tracking for comprehensive care.',
            'image': 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=400&h=250&fit=crop',
        },
        {
            'icon': '📱',
            'title': 'Telemedicine',
            'description': 'Video, phone, and chat consultations from the comfort of your home.',
            'image': 'https://images.unsplash.com/photo-1587854692152-cbe660dbde88?w=400&h=250&fit=crop',
        },
        {
            'icon': '📊',
            'title': 'Health Metrics',
            'description': 'Track vital signs and health metrics over time with visual dashboards.',
            'image': 'https://images.unsplash.com/photo-1551076805-e1869033e561?w=400&h=250&fit=crop',
        },
        {
            'icon': '🔒',
            'title': 'Secure & Private',
            'description': 'Your health data is encrypted and protected with enterprise-grade security.',
            'image': 'https://images.unsplash.com/photo-1563986768494-4dee2763ff3f?w=400&h=250&fit=crop',
        },
    ]

    context = {
        'doctors': doctors,
        'stats': stats,
        'features': features,
    }
    return render(request,'core/landing.html', context)


# ─────────────────────────────────────────────────────────────
# AUTHENTICATION
# ─────────────────────────────────────────────────────────────

def register_view(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role', 'patient')
            phone = form.cleaned_data.get('phone', '')

            # Create profile
            profile = UserProfile.objects.create(
                user=user,
                role=role,
                phone=phone,
            )

            # Create doctor profile if applicable
            if role == 'doctor':
                DoctorProfile.objects.create(
                    user_profile=profile,
                    license_number=f"TEMP-{user.id}",
                )

            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Your account has been created.')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()

    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'core/login.html')


def logout_view(request):
    """User logout"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('landing')


# ─────────────────────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    """Role-based dashboard routing"""
    profile = get_or_create_profile(request.user)

    if profile.role == 'doctor':
        return doctor_dashboard(request, profile)
    else:
        return patient_dashboard(request, profile)


def patient_dashboard(request, profile):
    """Patient dashboard view"""
    today = timezone.now().date()

    # Get recent data
    recent_checks = SymptomCheck.objects.filter(patient=profile)[:5]
    upcoming_appointments = Appointment.objects.filter(
        patient=profile,
        scheduled_date__gte=today,
        status__in=['scheduled', 'confirmed']
    )[:5]
    recent_metrics = HealthMetric.objects.filter(patient=profile)[:10]
    notifications = Notification.objects.filter(recipient=profile, is_read=False)[:5]
    medical_history = MedicalHistory.objects.filter(patient=profile, is_active=True)

    # Stats
    stats = {
        'total_checks': SymptomCheck.objects.filter(patient=profile).count(),
        'upcoming_appointments': upcoming_appointments.count(),
        'active_conditions': medical_history.count(),
        'health_metrics': recent_metrics.count(),
    }

    # Quick health cards
    health_cards = [
        {
            'title': 'AI Health Check',
            'description': 'Analyze your symptoms with our AI assistant',
            'icon': '🤖',
            'url': '/symptom-checker/',
            'color': '#4F46E5',
            'image': 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1f?w=300&h=180&fit=crop',
        },
        {
            'title': 'Book Appointment',
            'description': 'Schedule a consultation with a doctor',
            'icon': '📅',
            'url': '/appointments/book/',
            'color': '#059669',
            'image': 'https://images.unsplash.com/photo-1666214280557-f1b5022eb634?w=300&h=180&fit=crop',
        },
        {
            'title': 'Health Metrics',
            'description': 'Record and track your vital signs',
            'icon': '📊',
            'url': '/health-metrics/',
            'color': '#D97706',
            'image': 'https://images.unsplash.com/photo-1551076805-e1869033e561?w=300&h=180&fit=crop',
        },
        {
            'title': 'Medical Records',
            'description': 'View your complete health history',
            'icon': '📋',
            'url': '/patient-records/',
            'color': '#DC2626',
            'image': 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=300&h=180&fit=crop',
        },
    ]

    context = {
        'profile': profile,
        'recent_checks': recent_checks,
        'upcoming_appointments': upcoming_appointments,
        'recent_metrics': recent_metrics,
        'notifications': notifications,
        'medical_history': medical_history,
        'stats': stats,
        'health_cards': health_cards,
    }
    return render(request, 'core/dashboard_patient.html', context)


def doctor_dashboard(request, profile):
    """Doctor dashboard view"""
    today = timezone.now().date()

    try:
        doctor_info = profile.doctor_info
    except DoctorProfile.DoesNotExist:
        doctor_info = DoctorProfile.objects.create(
            user_profile=profile,
            license_number=f"TEMP-{profile.user.id}"
        )

    # Today's appointments
    todays_appointments = Appointment.objects.filter(
        doctor=profile,
        scheduled_date=today
    ).select_related('patient__user')

    # Pending reviews
    pending_reviews = SymptomCheck.objects.filter(
        status='analyzed'
    ).select_related('patient__user')[:10]

    # Recent patients
    recent_patients = Appointment.objects.filter(
        doctor=profile
    ).values('patient').distinct()[:10]

    # Stats
    stats = {
        'todays_appointments': todays_appointments.count(),
        'pending_reviews': pending_reviews.count(),
        'total_patients': Appointment.objects.filter(doctor=profile).values('patient').distinct().count(),
        'total_consultations': doctor_info.total_consultations,
        'rating': doctor_info.rating,
    }

    context = {
        'profile': profile,
        'doctor_info': doctor_info,
        'todays_appointments': todays_appointments,
        'pending_reviews': pending_reviews,
        'stats': stats,
    }
    return render(request, 'core/dashboard_doctor.html', context)


# ─────────────────────────────────────────────────────────────
# AI SYMPTOM CHECKER
# ─────────────────────────────────────────────────────────────

@login_required
def symptom_checker(request):
    """AI Symptom Checker - Main Interface"""
    profile = get_or_create_profile(request.user)

    if request.method == 'POST':
        form = SymptomCheckForm(request.POST)
        if form.is_valid():
            symptoms = form.cleaned_data['symptoms']
            medical_history = form.cleaned_data['medical_history']
            current_concern = form.cleaned_data['current_concern']
            user_type = profile.role

            # Run AI Analysis
            engine = HealthcareAIEngine()
            analysis = engine.analyze_symptoms(
                symptoms=symptoms,
                medical_history=medical_history,
                concern=current_concern,
                user_type=user_type,
            )

            # Save to database
            symptom_check = SymptomCheck.objects.create(
                patient=profile,
                symptoms=symptoms,
                medical_history_summary=medical_history,
                current_concern=current_concern,
                urgency_level=analysis.get('urgency_level', 'low'),
                ai_analysis=analysis.get('symptom_analysis'),
                ai_summary=json.dumps(analysis.get('medical_summary', {})),
                ai_follow_up_questions=analysis.get('follow_up_questions'),
                ai_guidance=json.dumps(analysis.get('patient_guidance', {})),
                ai_risk_flags=analysis.get('risk_flags'),
                status='analyzed',
            )

            return redirect('ai_report', check_id=symptom_check.id)
    else:
        form = SymptomCheckForm(initial={'user_type': profile.role})

    # Past checks
    past_checks = SymptomCheck.objects.filter(patient=profile)[:5]

    context = {
        'form': form,
        'profile': profile,
        'past_checks': past_checks,
    }
    return render(request, 'core/symptom_checker.html', context)


@login_required
def ai_report(request, check_id):
    """Display AI Analysis Report"""
    profile = get_or_create_profile(request.user)
    symptom_check = get_object_or_404(SymptomCheck, id=check_id)

    # Security: only the patient or a doctor can view
    if profile.role == 'patient' and symptom_check.patient != profile:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    # Parse stored JSON data
    medical_summary = {}
    patient_guidance = {}

    try:
        if symptom_check.ai_summary:
            medical_summary = json.loads(symptom_check.ai_summary)
    except (json.JSONDecodeError, TypeError):
        medical_summary = {}

    try:
        if symptom_check.ai_guidance:
            patient_guidance = json.loads(symptom_check.ai_guidance)
    except (json.JSONDecodeError, TypeError):
        patient_guidance = {}

    # Regenerate full analysis for doctor notes
    doctor_notes = None
    if profile.role == 'doctor':
        engine = HealthcareAIEngine()
        full_analysis = engine.analyze_symptoms(
            symptoms=symptom_check.symptoms,
            medical_history=symptom_check.medical_history_summary,
            concern=symptom_check.current_concern,
            user_type='doctor',
        )
        doctor_notes = full_analysis.get('doctor_notes')

    urgency_colors = {
        'low': '#059669',
        'medium': '#D97706',
        'high': '#DC2626',
        'critical': '#7C2D12',
    }

    context = {
        'check': symptom_check,
        'profile': profile,
        'analysis': symptom_check.ai_analysis or {},
        'medical_summary': medical_summary,
        'follow_up_questions': symptom_check.ai_follow_up_questions or [],
        'patient_guidance': patient_guidance,
        'risk_flags': symptom_check.ai_risk_flags or [],
        'doctor_notes': doctor_notes,
        'urgency_color': urgency_colors.get(symptom_check.urgency_level, '#6B7280'),
        'disclaimer': HealthcareAIEngine.SAFETY_DISCLAIMER,
    }
    return render(request, 'core/ai_report.html', context)


# ─────────────────────────────────────────────────────────────
# APPOINTMENTS
# ─────────────────────────────────────────────────────────────

@login_required
def appointments_view(request):
    """View all appointments"""
    profile = get_or_create_profile(request.user)

    if profile.role == 'doctor':
        appointments = Appointment.objects.filter(doctor=profile).select_related('patient__user')
    else:
        appointments = Appointment.objects.filter(patient=profile).select_related('doctor__user')

    context = {
        'profile': profile,
        'appointments': appointments,
    }
    return render(request, 'core/appointments.html', context)


@login_required
def book_appointment(request):
    """Book new appointment"""
    profile = get_or_create_profile(request.user)

    doctors = UserProfile.objects.filter(
        role='doctor',
        doctor_info__is_available=True
    ).select_related('user', 'doctor_info')

    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        doctor_profile = get_object_or_404(UserProfile, id=doctor_id, role='doctor')

        appointment = Appointment.objects.create(
            patient=profile,
            doctor=doctor_profile,
            appointment_type=request.POST.get('appointment_type', 'video'),
            scheduled_date=request.POST.get('scheduled_date'),
            scheduled_time=request.POST.get('scheduled_time'),
            reason=request.POST.get('reason', ''),
            fee=doctor_profile.doctor_info.consultation_fee,
        )

        # Create notification for doctor
        Notification.objects.create(
            recipient=doctor_profile,
            notification_type='appointment',
            title='New Appointment Booked',
            message=f'{profile.user.get_full_name()} has booked a {appointment.get_appointment_type_display()} appointment.',
            action_url=f'/appointments/',
        )

        messages.success(request, 'Appointment booked successfully!')
        return redirect('appointments')

    context = {
        'profile': profile,
        'doctors': doctors,
    }
    return render(request, 'core/appointments.html', context)


# ─────────────────────────────────────────────────────────────
# PATIENT RECORDS
# ─────────────────────────────────────────────────────────────

@login_required
def patient_records(request):
    """Patient health records management"""
    profile = get_or_create_profile(request.user)

    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.patient = profile
            record.save()
            messages.success(request, 'Medical history record added.')
            return redirect('patient_records')
    else:
        form = MedicalHistoryForm()

    history = MedicalHistory.objects.filter(patient=profile)
    checks = SymptomCheck.objects.filter(patient=profile)[:10]
    notes = ClinicalNote.objects.filter(patient=profile)

    context = {
        'profile': profile,
        'form': form,
        'medical_history': history,
        'symptom_checks': checks,
        'clinical_notes': notes,
    }
    return render(request, 'core/patient_records.html', context)


# ─────────────────────────────────────────────────────────────
# HEALTH METRICS
# ─────────────────────────────────────────────────────────────

@login_required
def health_metrics(request):
    """Health metrics tracking"""
    profile = get_or_create_profile(request.user)

    if request.method == 'POST':
        form = HealthMetricForm(request.POST)
        if form.is_valid():
            metric = form.save(commit=False)
            metric.patient = profile
            metric.save()
            messages.success(request, 'Health metric recorded.')
            return redirect('health_metrics')
    else:
        form = HealthMetricForm()

    metrics = HealthMetric.objects.filter(patient=profile)[:20]

    context = {
        'profile': profile,
        'form': form,
        'metrics': metrics,
    }
    return render(request, 'core/patient_records.html', context)


# ─────────────────────────────────────────────────────────────
# API ENDPOINTS
# ─────────────────────────────────────────────────────────────

@login_required
def api_quick_analysis(request):
    """AJAX endpoint for quick symptom analysis"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            symptoms = data.get('symptoms', '')

            if not symptoms:
                return JsonResponse({'error': 'Symptoms are required'}, status=400)

            engine = HealthcareAIEngine()
            analysis = engine.analyze_symptoms(symptoms=symptoms)

            return JsonResponse({
                'success': True,
                'urgency': analysis['urgency_level'],
                'possible_conditions': analysis['symptom_analysis']['possible_general_conditions'][:3],
                'risk_flags': analysis['risk_flags'],
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'POST method required'}, status=405)


@login_required
def api_mark_notification_read(request, notification_id):
    """Mark notification as read"""
    profile = get_or_create_profile(request.user)
    notification = get_object_or_404(Notification, id=notification_id, recipient=profile)
    notification.is_read = True
    notification.save()
    return JsonResponse({'success': True})


# ─────────────────────────────────────────────────────────────
# UTILITY FUNCTIONS
# ─────────────────────────────────────────────────────────────

def get_or_create_profile(user):
    """Get or create a user profile"""
    profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={'role': 'patient'}
    )
    return profile