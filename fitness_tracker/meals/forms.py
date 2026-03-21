from django import forms
from .models import Meal


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['meal_name', 'calories', 'protein', 'carbs', 'fat', 'fiber',
                  'meal_time', 'date', 'notes']
        widgets = {
            'meal_name': forms.TextInput(attrs={'class': 'form-control',
                                                 'placeholder': 'e.g., Grilled Chicken Salad'}),
            'calories': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'protein': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1',
                                                'placeholder': 'grams'}),
            'carbs': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1',
                                              'placeholder': 'grams'}),
            'fat': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1',
                                            'placeholder': 'grams'}),
            'fiber': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1',
                                              'placeholder': 'grams'}),
            'meal_time': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }