from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Payment


@login_required
def payment_history(request):
    payments = Payment.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'payments/payment_history.html', {'payments': payments})