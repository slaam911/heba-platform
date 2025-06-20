from django.urls import path
from . import views

app_name = 'bloodbankuser'

urlpatterns = [
    path('register/', views.bloodbankuser_register, name='bloodbankuser_register'),
    path('login/', views.bloodbankuser_login, name='bloodbankuser_login'),
    path('profile/', views.bloodbankuser_profile, name='bloodbankuser_profile'),
] 