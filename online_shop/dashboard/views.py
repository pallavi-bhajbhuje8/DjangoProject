from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from products.models import Product
from products.forms import ProductForm
from categories.models import Category
from categories.forms import CategoryForm
from orders.models import Order, OrderItem
from orders.forms import OrderStatusForm
from payments.models import Payment
import json


@staff_member_required
def dashboard_home(request):
    total_orders = Order.objects.count()
    total_users = User.objects.filter(is_staff=False).count()
    total_products = Product.objects.count()
    total_revenue = Payment.objects.filter(status='completed').aggregate(
        total=Sum('amount'))['total'] or 0

    recent_orders = Order.objects.all()[:10]

    # Monthly revenue for chart
    monthly_revenue = (
        Payment.objects.filter(status='completed')
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    months = [item['month'].strftime('%b %Y') for item in monthly_revenue] if monthly_revenue else []
    revenues = [float(item['total']) for item in monthly_revenue] if monthly_revenue else []

    # Order status counts
    status_counts = Order.objects.values('status').annotate(count=Count('id'))
    status_labels = [item['status'].capitalize() for item in status_counts]
    status_data = [item['count'] for item in status_counts]

    # Top products
    top_products = (
        OrderItem.objects.values('product_name')
        .annotate(total_sold=Sum('quantity'))
        .order_by('-total_sold')[:5]
    )

    context = {
        'total_orders': total_orders,
        'total_users': total_users,
        'total_products': total_products,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'months_json': json.dumps(months),
        'revenues_json': json.dumps(revenues),
        'status_labels_json': json.dumps(status_labels),
        'status_data_json': json.dumps(status_data),
        'top_products': top_products,
    }
    return render(request, 'dashboard/dashboard.html', context)


# --- Product Management ---
@staff_member_required
def dashboard_products(request):
    products = Product.objects.select_related('category').all()
    query = request.GET.get('q', '')
    if query:
        products = products.filter(product_name__icontains=query)
    return render(request, 'dashboard/products.html', {
        'products': products,
        'query': query,
    })


@staff_member_required
def dashboard_product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('dashboard:products')
    else:
        form = ProductForm()
    return render(request, 'dashboard/product_form.html', {'form': form, 'title': 'Add Product'})


@staff_member_required
def dashboard_product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('dashboard:products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'dashboard/product_form.html', {'form': form, 'title': 'Edit Product'})


@staff_member_required
def dashboard_product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
    return redirect('dashboard:products')


# --- Category Management ---
@staff_member_required
def dashboard_categories(request):
    categories = Category.objects.all()
    return render(request, 'dashboard/categories.html', {'categories': categories})


@staff_member_required
def dashboard_category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('dashboard:categories')
    else:
        form = CategoryForm()
    return render(request, 'dashboard/category_form.html', {'form': form, 'title': 'Add Category'})


@staff_member_required
def dashboard_category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('dashboard:categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'dashboard/category_form.html', {'form': form, 'title': 'Edit Category'})


@staff_member_required
def dashboard_category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
    return redirect('dashboard:categories')


# --- Order Management ---
@staff_member_required
def dashboard_orders(request):
    orders = Order.objects.all()
    status_filter = request.GET.get('status', '')
    if status_filter:
        orders = orders.filter(status=status_filter)
    return render(request, 'dashboard/orders.html', {
        'orders': orders,
        'status_filter': status_filter,
    })


@staff_member_required
def dashboard_order_detail(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    items = order.items.all()
    payment = Payment.objects.filter(order=order).first()

    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order status updated!')
            return redirect('dashboard:order_detail', order_id=order.order_id)
    else:
        form = OrderStatusForm(instance=order)

    return render(request, 'dashboard/order_detail.html', {
        'order': order,
        'items': items,
        'payment': payment,
        'form': form,
    })


# --- User Management ---
@staff_member_required
def dashboard_users(request):
    users = User.objects.filter(is_staff=False).order_by('-date_joined')
    query = request.GET.get('q', '')
    if query:
        users = users.filter(username__icontains=query)
    return render(request, 'dashboard/users.html', {'users': users, 'query': query})


# --- Reports ---
@staff_member_required
def dashboard_reports(request):
    total_revenue = Payment.objects.filter(status='completed').aggregate(
        total=Sum('amount'))['total'] or 0
    total_orders = Order.objects.count()
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

    # Category-wise sales
    category_sales = (
        OrderItem.objects
        .values('product__category__name')
        .annotate(total_sales=Sum('quantity'), total_revenue=Sum('price'))
        .order_by('-total_sales')
    )

    context = {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'avg_order_value': round(avg_order_value, 2),
        'category_sales': category_sales,
    }
    return render(request, 'dashboard/reports.html', context)