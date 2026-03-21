from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product
from categories.models import Category
from reviews.models import Review
from reviews.forms import ReviewForm


def home_view(request):
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    latest_products = Product.objects.filter(is_active=True)[:8]
    categories = Category.objects.filter(is_active=True)
    return render(request, 'home.html', {
        'featured_products': featured_products,
        'latest_products': latest_products,
        'categories': categories,
    })


def product_list(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)

    # Search
    query = request.GET.get('q', '')
    if query:
        products = products.filter(
            Q(product_name__icontains=query) |
            Q(description__icontains=query)
        )

    # Category filter
    category_slug = request.GET.get('category', '')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # Sort
    sort_by = request.GET.get('sort', '')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_date')
    elif sort_by == 'rating':
        products = products.order_by('-rating')
    elif sort_by == 'name':
        products = products.order_by('product_name')

    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category_slug,
        'sort_by': sort_by,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    reviews = Review.objects.filter(product=product).order_by('-review_date')
    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(id=product.id)[:4]

    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(product=product, user=request.user).first()

    review_form = ReviewForm()

    return render(request, 'products/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'related_products': related_products,
        'user_review': user_review,
        'review_form': review_form,
    })