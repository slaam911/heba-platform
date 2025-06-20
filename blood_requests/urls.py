from django.urls import path
from . import views

app_name = 'blood_requests'

urlpatterns = [
    path('', views.request_list, name='list'),
    path('create/', views.request_create, name='create'),
    path('<uuid:request_id>/', views.request_detail, name='detail'),
    path('<uuid:request_id>/success/', views.request_success, name='success'),
] 