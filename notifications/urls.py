from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notification_list, name='list'),
    path('<int:pk>/', views.notification_detail, name='detail'),
    path('mark-all-read/', views.mark_all_read, name='mark_all_read'),
    path('<int:pk>/mark-read/', views.mark_read, name='mark_read'),
] 