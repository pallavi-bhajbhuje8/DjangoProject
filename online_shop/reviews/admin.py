from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'review_date']
    list_filter = ['rating', 'review_date']
    search_fields = ['product__product_name', 'user__username', 'review_text']