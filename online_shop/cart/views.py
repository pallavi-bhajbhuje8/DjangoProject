from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Cart, CartItem, Coupon
from products.models import Product
from .forms import CouponForm


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product').all()
    coupon_form = CouponForm()

    discount = request.session.get('discount', 0)
    coupon_code = request.session.get('coupon_code', '')

    total = cart.get_total()
    discount_amount = (total * discount) / 100 if discount else 0
    final_total = total - discount_amount

    return render(request, 'cart/cart.html', {
        'cart': cart,
        'items': items,
        'coupon_form': coupon_form,
        'discount': discount,
        'coupon_code': coupon_code,
        'discount_amount': round(discount_amount, 2),
        'final_total': round(final_total, 2),
    })


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart, created = Cart.objects.get_or_create(user=request.user)

    quantity = int(request.POST.get('quantity', 1))
    if quantity < 1:
        quantity = 1

    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart, product=product,
        defaults={'quantity': quantity}
    )

    if not item_created:
        cart_item.quantity += quantity
        cart_item.save()

    if cart_item.quantity > product.stock_quantity:
        cart_item.quantity = product.stock_quantity
        cart_item.save()
        messages.warning(request, f'Only {product.stock_quantity} items available.')
    else:
        messages.success(request, f'"{product.product_name}" added to cart!')

    return redirect('cart:cart_view')


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.product_name
    cart_item.delete()
    messages.info(request, f'"{product_name}" removed from cart.')
    return redirect('cart:cart_view')


@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))

    if quantity < 1:
        cart_item.delete()
        messages.info(request, 'Item removed from cart.')
    elif quantity > cart_item.product.stock_quantity:
        cart_item.quantity = cart_item.product.stock_quantity
        cart_item.save()
        messages.warning(request, f'Only {cart_item.product.stock_quantity} items available.')
    else:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Cart updated.')

    return redirect('cart:cart_view')


@login_required
def apply_coupon(request):
    if request.method == 'POST':
        code = request.POST.get('code', '').strip().upper()
        try:
            coupon = Coupon.objects.get(
                code=code,
                is_active=True,
                valid_from__lte=timezone.now(),
                valid_until__gte=timezone.now()
            )
            cart = Cart.objects.get(user=request.user)
            total = cart.get_total()

            if total < coupon.min_order_amount:
                messages.error(request, f'Minimum order amount is ${coupon.min_order_amount}.')
            else:
                request.session['discount'] = float(coupon.discount_percent)
                request.session['coupon_code'] = coupon.code
                messages.success(request, f'Coupon applied! {coupon.discount_percent}% discount.')
        except Coupon.DoesNotExist:
            messages.error(request, 'Invalid or expired coupon code.')

    return redirect('cart:cart_view')


@login_required
def remove_coupon(request):
    request.session.pop('discount', None)
    request.session.pop('coupon_code', None)
    messages.info(request, 'Coupon removed.')
    return redirect('cart:cart_view')