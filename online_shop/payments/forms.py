from django import forms


class PaymentForm(forms.Form):
    payment_method = forms.ChoiceField(
        choices=[
            ('credit_card', 'Credit Card'),
            ('debit_card', 'Debit Card'),
            ('upi', 'UPI'),
            ('cod', 'Cash on Delivery'),
        ],
        widget=forms.RadioSelect()
    )