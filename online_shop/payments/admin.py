from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'order', 'user', 'payment_method', 'amount', 'status', 'created_at']
    list_filter = ['payment_method', 'status']
    search_fields = ['transaction_id', 'order__order_id']
    readonly_fields = ['transaction_id']