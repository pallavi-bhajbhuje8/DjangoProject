# core/management/commands/seed_data.py

import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import UserProfile, DoctorProfile, MedicalHistory

# Create the management/commands directories
# mkdir -p core/management/commands
# touch core/management/__init__.py
# touch core/management/commands/__init__.py


class Command(BaseCommand):
    help = 'Seeds the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # Create demo doctors
        doctors_data = [
            {
                'username': 'dr_mitchell',
                'first_name': 'Sarah',
                'last_name': 'Mitchell',
                'email': 'sarah.mitchell@medicare.ai',
                'specialty': 'cardiology',
                'years_experience': 15,
                'license_number': 'MD-CARD-001',
                'bio': 'Board-certified cardiologist with expertise in preventive cardiology.',
                'consultation_fee': 150.00,
                'rating': 4.9,
                'photo_url': 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=300&h=300&fit=crop',
            },
            {
                'username': 'dr_chen',
                'first_name': 'Emily',
                'last_name': 'Chen',
                'email': 'emily.chen@medicare.ai',
                'specialty': 'neurology',
                'years_experience': 12,
                'license_number': 'MD-NEUR-002',
                'bio': 'Neurologist specializing in headache disorders and neuromuscular conditions.',
                'consultation_fee': 175.00,
                'rating': 4.8,
                'photo_url': 'https://images.unsplash.com/photo-1594824476967-48c8b964273f?w=300&h=300&fit=crop',
            },
            {
                'username': 'dr_wilson',
                'first_name': 'James',
                'last_name': 'Wilson',
                'email': 'james.wilson@medicare.ai',
                'specialty': 'general',
                'years_experience': 20,
                'license_number': 'MD-GEN-003',
                'bio': 'Experienced general practitioner focused on holistic patient care.',
                'consultation_fee': 100.00,
                'rating': 4.9,
                'photo_url': 'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=300&h=300&fit=crop',
            },
            {
                'username': 'dr_patel',
                'first_name': 'Priya',
                'last_name': 'Patel',
                'email': 'priya.patel@medicare.ai',
                'specialty': 'dermatology',
                'years_experience': 8,
                'license_number': 'MD-DERM-004',
                'bio': 'Dermatologist with special interest in inflammatory skin conditions.',
                'consultation_fee': 125.00,
                'rating': 4.7,
                'photo_url': 'https://images.unsplash.com/photo-1651008376811-b90baee60c1f?w=300&h=300&fit=crop',
            },
            {
                'username': 'dr_garcia',
                'first_name': 'Maria',
                'last_name': 'Garcia',
                'email': 'maria.garcia@medicare.ai',
                'specialty': 'psychiatry',
                'years_experience': 10,
                'license_number': 'MD-PSYCH-005',
                'bio': 'Psychiatrist specializing in anxiety, depression, and stress management.',
                'consultation_fee': 200.00,
                'rating': 4.9,
                'photo_url': 'https://images.unsplash.com/photo-1614608682850-e0d6ed316d47?w=300&h=300&fit=crop',
            },
            {
                'username': 'dr_johnson',
                'first_name': 'Robert',
                'last_name': 'Johnson',
                'email': 'robert.johnson@medicare.ai',
                'specialty': 'orthopedics',
                'years_experience': 18,
                'license_number': 'MD-ORTH-006',
                'bio': 'Orthopedic specialist focused on sports injuries and joint health.',
                'consultation_fee': 160.00,
                'rating': 4.8,
                'photo_url': 'https://images.unsplash.com/photo-1622253694242-abeb37a33e97?w=300&h=300&fit=crop',
            },
        ]

        for doc_data in doctors_data:
            user, created = User.objects.get_or_create(
                username=doc_data['username'],
                defaults={
                    'first_name': doc_data['first_name'],
                    'last_name': doc_data['last_name'],
                    'email': doc_data['email'],
                }
            )
            if created:
                user.set_password('doctor123')
                user.save()

            profile, _ = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'role': 'doctor',
                    'phone': '+1-555-000-0000',
                    'gender': 'female' if doc_data['first_name'] in ['Sarah', 'Emily', 'Priya', 'Maria'] else 'male',
                }
            )

            DoctorProfile.objects.get_or_create(
                user_profile=profile,
                defaults={
                    'specialty': doc_data['specialty'],
                    'license_number': doc_data['license_number'],
                    'years_experience': doc_data['years_experience'],
                    'bio': doc_data['bio'],
                    'consultation_fee': doc_data['consultation_fee'],
                    'rating': doc_data['rating'],
                    'photo_url': doc_data['photo_url'],
                    'hospital_affiliation': 'MediCare AI Medical Center',
                    'is_available': True,
                }
            )

            self.stdout.write(f'  ✅ Created Dr. {doc_data["first_name"]} {doc_data["last_name"]}')

        # Create demo patient
        patient_user, created = User.objects.get_or_create(
            username='demo_patient',
            defaults={
                'first_name': 'Alex',
                'last_name': 'Thompson',
                'email': 'alex@example.com',
            }
        )
        if created:
            patient_user.set_password('patient123')
            patient_user.save()

        patient_profile, _ = UserProfile.objects.get_or_create(
            user=patient_user,
            defaults={
                'role': 'patient',
                'phone': '+1-555-123-4567',
                'gender': 'male',
                'blood_group': 'O+',
            }
        )

        # Add medical history for demo patient
        history_items = [
            {'condition_type': 'allergy', 'condition_name': 'Penicillin', 'severity': 'moderate'},
            {'condition_type': 'chronic', 'condition_name': 'Mild Hypertension', 'severity': 'mild'},
            {'condition_type': 'medication', 'condition_name': 'Lisinopril 10mg daily', 'severity': 'mild'},
        ]

        for item in history_items:
            MedicalHistory.objects.get_or_create(
                patient=patient_profile,
                condition_name=item['condition_name'],
                defaults=item,
            )

        self.stdout.write(self.style.SUCCESS('\n✅ Database seeded successfully!'))
        self.stdout.write(self.style.SUCCESS('  Demo Patient: demo_patient / patient123'))
        self.stdout.write(self.style.SUCCESS('  Demo Doctor:  dr_mitchell / doctor123'))