from django.urls import path
from . import views

app_name = 'blood_donation'

urlpatterns = [
    path('', views.donation_list, name='list'),
    path('<int:pk>/', views.donation_detail, name='detail'),
    path('create/', views.donation_create, name='create'),
    path('<int:pk>/edit/', views.donation_edit, name='edit'),
    path('<int:pk>/delete/', views.donation_delete, name='delete'),
] 