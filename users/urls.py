from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('select-registration/', views.select_registration_type, name='select_registration'),
    path('register/', views.register, name='register'),
    path('register/success/', views.register_success, name='register_success'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('<str:username>/', views.public_profile, name='public_profile'),
    path('<str:username>/edit/', views.profile, name='profile_edit'),
    path('verify/', views.verify_code, name='verify_code'),
    path('resend-code/', views.resend_code, name='resend_code'),
    path('api/cities/', views.get_cities, name='get_cities'),
    path('bloodbank/profile/', views.bloodbank_profile, name='bloodbank_profile'),
] 