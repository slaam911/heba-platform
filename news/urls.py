from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('archive/', views.news_archive, name='archive'),
    path('article/<int:pk>/', views.news_detail, name='detail'),
    path('section/<int:section_id>/', views.news_section, name='section'),
] 