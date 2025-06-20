from django.shortcuts import render
from campaigns.models import Campaign
from blood_requests.models import BloodRequest
from donationuser.models import CustomUser
from news.models import NewsArticle, NewsSection
from django.utils import timezone
from django.http import HttpResponse
from .models import SiteStyle

def home(request):
    now = timezone.now()
    context = {
        'total_donors': CustomUser.objects.count(),
        'total_donations': BloodRequest.objects.count(),
        'total_campaigns': Campaign.objects.count(),
        'latest_campaigns': Campaign.objects.filter(status='active').order_by('-created_at')[:3],
        'latest_blood_requests': BloodRequest.objects.filter(status='approved').exclude(expires_at=None).order_by('-created_at')[:6],
        'latest_news_articles': NewsArticle.objects.filter(status='published', publish_time__lte=timezone.now()).order_by('-publish_time')[:3],
        'news_sections': NewsSection.objects.filter(status='active').order_by('-priority', 'name'),
    }
    return render(request, 'core/home.html', context) 