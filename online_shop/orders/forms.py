from django import forms
from .models import Order


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Street Address'})
    )
    shipping_city = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'})
    )
    shipping_state = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'})
    )
    shipping_country = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
        initial='India'
    )
    shipping_zip = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ZIP Code'})
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'})
    )
    payment_method = forms.ChoiceField(
        choices=[
            ('credit_card', 'Credit Card'),
            ('debit_card', 'Debit Card'),
            ('upi', 'UPI'),
            ('cod', 'Cash on Delivery'),
        ],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Order notes (optional)'})
    )


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }