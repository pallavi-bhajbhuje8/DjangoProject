from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.catalog, name='catalog'),
    path('course/<slug:slug>/', views.course_detail, name='course_detail'),
    path('course/<slug:course_slug>/lesson/<slug:lesson_slug>/', views.lesson_view, name='lesson'),
    path('course/<slug:course_slug>/quiz/<slug:lesson_slug>/', views.quiz_view, name='quiz'),
    path('checkout/<slug:slug>/', views.checkout, name='checkout'),
    path('receipt/<str:payment_id>/', views.receipt_view, name='receipt'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('instructor/', views.instructor_dashboard, name='instructor_dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
]