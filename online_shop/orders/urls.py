from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('history/', views.order_history, name='order_history'),
    path('<str:order_id>/', views.order_detail, name='order_detail'),
    path('<str:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    path('<str:order_id>/receipt/', views.download_receipt, name='download_receipt'),
]