import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Order, OrderItem
from .forms import CheckoutForm
from cart.models import Cart
from payments.models import Payment


@login_required
def checkout_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product').all()

    if not items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart:cart_view')

    discount = request.session.get('discount', 0)
    coupon_code = request.session.get('coupon_code', '')
    subtotal = cart.get_total()
    discount_amount = (subtotal * discount) / 100 if discount else 0
    final_total = subtotal - discount_amount

    # Pre-fill from profile
    initial_data = {}
    if hasattr(request.user, 'profile'):
        profile = request.user.profile
        initial_data = {
            'shipping_address': profile.address,
            'shipping_city': profile.city,
            'shipping_state': profile.state,
            'shipping_country': profile.country or 'India',
            'shipping_zip': profile.zip_code,
            'phone': profile.phone,
        }

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create Order
            order = Order.objects.create(
                user=request.user,
                shipping_address=form.cleaned_data['shipping_address'],
                shipping_city=form.cleaned_data['shipping_city'],
                shipping_state=form.cleaned_data['shipping_state'],
                shipping_country=form.cleaned_data['shipping_country'],
                shipping_zip=form.cleaned_data['shipping_zip'],
                phone=form.cleaned_data['phone'],
                subtotal=subtotal,
                discount_amount=round(discount_amount, 2),
                total_price=round(final_total, 2),
                coupon_code=coupon_code,
                notes=form.cleaned_data.get('notes', ''),
            )

            # Create Order Items
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_name=item.product.product_name,
                    product_image=item.product.product_image,
                    price=item.get_price(),
                    quantity=item.quantity,
                )
                # Reduce stock
                item.product.stock_quantity -= item.quantity
                if item.product.stock_quantity < 0:
                    item.product.stock_quantity = 0
                item.product.save()

            # Create Payment
            payment_method = form.cleaned_data['payment_method']
            payment_status = 'completed' if payment_method != 'cod' else 'pending'
            Payment.objects.create(
                order=order,
                user=request.user,
                payment_method=payment_method,
                amount=round(final_total, 2),
                status=payment_status,
            )

            # Clear cart and coupon
            cart.items.all().delete()
            request.session.pop('discount', None)
            request.session.pop('coupon_code', None)

            messages.success(request, f'Order placed successfully! Order ID: {order.order_id}')
            return redirect('orders:order_detail', order_id=order.order_id)
    else:
        form = CheckoutForm(initial=initial_data)

    return render(request, 'orders/checkout.html', {
        'form': form,
        'items': items,
        'subtotal': subtotal,
        'discount': discount,
        'discount_amount': round(discount_amount, 2),
        'final_total': round(final_total, 2),
        'coupon_code': coupon_code,
    })


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    items = order.items.all()
    payment = Payment.objects.filter(order=order).first()
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'items': items,
        'payment': payment,
    })


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    if order.status in ['pending', 'processing']:
        order.status = 'cancelled'
        order.save()

        # Restore stock
        for item in order.items.all():
            if item.product:
                item.product.stock_quantity += item.quantity
                item.product.save()

        # Update payment
        payment = Payment.objects.filter(order=order).first()
        if payment:
            payment.status = 'refunded'
            payment.save()

        messages.success(request, f'Order #{order.order_id} has been cancelled.')
    else:
        messages.error(request, 'This order cannot be cancelled.')
    return redirect('orders:order_detail', order_id=order.order_id)


@login_required
def download_receipt(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    items = order.items.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="receipt_{order.order_id}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Order Receipt'])
    writer.writerow([])
    writer.writerow(['Order ID', order.order_id])
    writer.writerow(['Date', order.created_at.strftime('%Y-%m-%d %H:%M')])
    writer.writerow(['Status', order.get_status_display()])
    writer.writerow(['Customer', order.user.get_full_name() or order.user.username])
    writer.writerow(['Shipping Address', f'{order.shipping_address}, {order.shipping_city}, {order.shipping_state}, {order.shipping_country} - {order.shipping_zip}'])
    writer.writerow([])
    writer.writerow(['Product', 'Quantity', 'Price', 'Subtotal'])

    for item in items:
        writer.writerow([
            item.product_name,
            item.quantity,
            f'${item.price}',
            f'${item.get_subtotal()}'
        ])

    writer.writerow([])
    writer.writerow(['Subtotal', '', '', f'${order.subtotal}'])
    if order.discount_amount > 0:
        writer.writerow(['Discount', '', '', f'-${order.discount_amount}'])
    writer.writerow(['Total', '', '', f'${order.total_price}'])

    return response