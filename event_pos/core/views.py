from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg, Count
from django.utils import timezone
from .models import (
    Category, Product, Review, Wishlist, Coupon,
    Cart, CartItem, Order, OrderItem, UserProfile
)
import json


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart
    else:
        if not request.session.session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
        return cart


def home(request):
    categories = Category.objects.filter(is_active=True, parent__isnull=True)[:8]
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    new_products = Product.objects.filter(is_active=True, is_new=True)[:6]
    all_products = Product.objects.filter(is_active=True)[:12]

    context = {
        'categories': categories,
        'featured_products': featured_products,
        'new_products': new_products,
        'all_products': all_products,
    }
    return render(request, 'core/home.html', context)


def shop(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True, parent__isnull=True)

    # Search
    query = request.GET.get('q', '')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__icontains=query)
        )

    # Category filter
    category_slug = request.GET.get('category', '')
    if category_slug:
        products = products.filter(
            Q(category__slug=category_slug) |
            Q(category__parent__slug=category_slug)
        )

    # Price filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Sort
    sort = request.GET.get('sort', 'newest')
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('name')
    elif sort == 'popular':
        products = products.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
    else:
        products = products.order_by('-created_at')

    active_category = None
    if category_slug:
        active_category = Category.objects.filter(slug=category_slug).first()

    context = {
        'products': products,
        'categories': categories,
        'query': query,
        'active_category': active_category,
        'current_sort': sort,
        'min_price': min_price or '',
        'max_price': max_price or '',
    }
    return render(request, 'core/shop.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(id=product.id)[:4]
    reviews = product.reviews.all()[:10]
    user_review = None
    in_wishlist = False

    if request.user.is_authenticated:
        user_review = Review.objects.filter(product=product, user=request.user).first()
        in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()

    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')
        title = request.POST.get('title', '')
        if rating:
            Review.objects.update_or_create(
                product=product,
                user=request.user,
                defaults={
                    'rating': int(rating),
                    'comment': comment,
                    'title': title,
                }
            )
            messages.success(request, 'Review submitted successfully!')
            return redirect('product_detail', slug=slug)

    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'user_review': user_review,
        'in_wishlist': in_wishlist,
    }
    return render(request, 'core/product_detail.html', context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = get_or_create_cart(request)
    quantity = int(request.POST.get('quantity', 1))

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.item_count,
            'message': f'{product.name} added to cart!'
        })

    messages.success(request, f'{product.name} added to cart!')
    return redirect(request.META.get('HTTP_REFERER', 'shop'))


def cart_view(request):
    cart = get_or_create_cart(request)
    context = {'cart': cart}
    return render(request, 'core/cart.html', context)


def update_cart(request, item_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)

    action = request.POST.get('action', '')
    if action == 'increase':
        item.quantity += 1
        item.save()
    elif action == 'decrease':
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
    elif action == 'remove':
        item.delete()

    quantity_val = request.POST.get('quantity')
    if quantity_val:
        try:
            qty = int(quantity_val)
            if qty > 0:
                item.quantity = qty
                item.save()
            else:
                item.delete()
        except ValueError:
            pass

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.item_count,
            'subtotal': float(cart.subtotal),
            'total': float(cart.total),
        })

    return redirect('cart')


def apply_coupon(request):
    if request.method == 'POST':
        code = request.POST.get('coupon_code', '').strip().upper()
        cart = get_or_create_cart(request)

        try:
            coupon = Coupon.objects.get(code=code)
            if coupon.is_valid:
                if cart.subtotal >= coupon.min_order_amount:
                    cart.coupon = coupon
                    cart.save()
                    messages.success(request, f'Coupon "{code}" applied successfully!')
                else:
                    messages.error(request, f'Minimum order amount is ₹{coupon.min_order_amount}')
            else:
                messages.error(request, 'This coupon has expired or is no longer valid.')
        except Coupon.DoesNotExist:
            messages.error(request, 'Invalid coupon code.')

    return redirect('cart')


def remove_coupon(request):
    cart = get_or_create_cart(request)
    cart.coupon = None
    cart.save()
    messages.info(request, 'Coupon removed.')
    return redirect('cart')


@login_required
def checkout(request):
    cart = get_or_create_cart(request)
    if cart.item_count == 0:
        messages.warning(request, 'Your cart is empty!')
        return redirect('shop')

    profile = UserProfile.objects.filter(user=request.user).first()

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            subtotal=cart.subtotal,
            discount=cart.discount_amount,
            shipping_cost=0 if cart.subtotal >= 500 else 50,
            total=cart.total + (0 if cart.subtotal >= 500 else 50),
            coupon_code=cart.coupon.code if cart.coupon else '',
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            zipcode=request.POST.get('zipcode'),
            payment_method=request.POST.get('payment_method', 'cod'),
            notes=request.POST.get('notes', ''),
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                product_image=item.product.image,
                price=item.product.price,
                quantity=item.quantity,
            )

        # Update coupon usage
        if cart.coupon:
            cart.coupon.used_count += 1
            cart.coupon.save()

        # Clear cart
        cart.items.all().delete()
        cart.coupon = None
        cart.save()

        # Update profile
        UserProfile.objects.update_or_create(
            user=request.user,
            defaults={
                'phone': request.POST.get('phone', ''),
                'address': request.POST.get('address', ''),
                'city': request.POST.get('city', ''),
                'state': request.POST.get('state', ''),
                'zipcode': request.POST.get('zipcode', ''),
            }
        )

        messages.success(request, f'Order {order.order_id} placed successfully!')
        return redirect('order_history')

    shipping_cost = 0 if cart.subtotal >= 500 else 50

    context = {
        'cart': cart,
        'profile': profile,
        'shipping_cost': shipping_cost,
        'order_total': cart.total + shipping_cost,
    }
    return render(request, 'core/checkout.html', context)


@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, product=product)

    if wishlist_item.exists():
        wishlist_item.delete()
        added = False
    else:
        Wishlist.objects.create(user=request.user, product=product)
        added = True

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'added': added})

    return redirect(request.META.get('HTTP_REFERER', 'shop'))


@login_required
def dashboard(request):
    recent_orders = Order.objects.filter(user=request.user)[:5]
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')[:8]
    total_orders = Order.objects.filter(user=request.user).count()
    total_spent = sum(o.total for o in Order.objects.filter(user=request.user))

    context = {
        'recent_orders': recent_orders,
        'wishlist_items': wishlist_items,
        'total_orders': total_orders,
        'total_spent': total_spent,
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    context = {'orders': orders}
    return render(request, 'core/order_history.html', context)


@login_required
def profile(request):
    profile_obj, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()

        profile_obj.phone = request.POST.get('phone', '')
        profile_obj.address = request.POST.get('address', '')
        profile_obj.city = request.POST.get('city', '')
        profile_obj.state = request.POST.get('state', '')
        profile_obj.zipcode = request.POST.get('zipcode', '')
        profile_obj.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')

    context = {'profile': profile_obj}
    return render(request, 'core/profile.html', context)


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # Merge session cart with user cart
            session_key = request.session.session_key
            if session_key:
                session_cart = Cart.objects.filter(session_key=session_key).first()
                if session_cart:
                    user_cart, _ = Cart.objects.get_or_create(user=user)
                    for item in session_cart.items.all():
                        cart_item, created = CartItem.objects.get_or_create(
                            cart=user_cart,
                            product=item.product,
                            defaults={'quantity': item.quantity}
                        )
                        if not created:
                            cart_item.quantity += item.quantity
                            cart_item.save()
                    session_cart.delete()

            next_url = request.GET.get('next', 'home')
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'core/login.html')


def user_register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')

        if password != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')

    return render(request, 'core/register.html')


def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')