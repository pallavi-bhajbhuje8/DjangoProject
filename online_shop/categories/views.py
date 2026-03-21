from django.shortcuts import render, get_object_or_404
from .models import Category
from products.models import Product


def category_list(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, 'categories/category_products.html', {
        'categories': categories,
        'products': None,
        'selected_category': None,
    })


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(category=category, is_active=True)

    sort_by = request.GET.get('sort', '')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_date')
    elif sort_by == 'rating':
        products = products.order_by('-rating')

    return render(request, 'categories/category_products.html', {
        'categories': categories,
        'products': products,
        'selected_category': category,
        'sort_by': sort_by,
    })