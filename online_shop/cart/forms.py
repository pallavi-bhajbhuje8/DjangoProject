from django import forms


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1, max_value=99, initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 80px;'})
    )


class CouponForm(forms.Form):
    code = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter coupon code'
        })
    )