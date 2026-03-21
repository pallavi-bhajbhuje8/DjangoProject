from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'category', 'price', 'discount_price',
                    'stock_quantity', 'rating', 'is_active', 'is_featured']
    list_filter = ['category', 'is_active', 'is_featured']
    search_fields = ['product_name', 'description']
    prepopulated_fields = {'slug': ('product_name',)}
    list_editable = ['price', 'stock_quantity', 'is_active', 'is_featured']