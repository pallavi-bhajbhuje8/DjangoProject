from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    # Products
    path('products/', views.dashboard_products, name='products'),
    path('products/add/', views.dashboard_product_add, name='product_add'),
    path('products/<int:pk>/edit/', views.dashboard_product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.dashboard_product_delete, name='product_delete'),
    # Categories
    path('categories/', views.dashboard_categories, name='categories'),
    path('categories/add/', views.dashboard_category_add, name='category_add'),
    path('categories/<int:pk>/edit/', views.dashboard_category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.dashboard_category_delete, name='category_delete'),
    # Orders
    path('orders/', views.dashboard_orders, name='orders'),
    path('orders/<str:order_id>/', views.dashboard_order_detail, name='order_detail'),
    # Users
    path('users/', views.dashboard_users, name='users'),
    # Reports
    path('reports/', views.dashboard_reports, name='reports'),
]