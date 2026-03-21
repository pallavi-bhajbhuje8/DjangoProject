from django import forms
from .models import HealthMetric


class HealthMetricForm(forms.ModelForm):
    class Meta:
        model = HealthMetric
        fields = ['date', 'weight', 'heart_rate', 'blood_pressure_systolic',
                  'blood_pressure_diastolic', 'sleep_hours', 'water_intake',
                  'body_fat', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01',
                                               'placeholder': 'kg'}),
            'heart_rate': forms.NumberInput(attrs={'class': 'form-control',
                                                    'placeholder': 'bpm'}),
            'blood_pressure_systolic': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Systolic'}),
            'blood_pressure_diastolic': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Diastolic'}),
            'sleep_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5',
                                                     'placeholder': 'Hours'}),
            'water_intake': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1',
                                                      'placeholder': 'Liters'}),
            'body_fat': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1',
                                                  'placeholder': '%'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }