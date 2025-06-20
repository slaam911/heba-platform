from django.shortcuts import render, get_object_or_404
from .models import NewsArticle, NewsSection
from django.utils import timezone

# Create your views here.

def news_archive(request):
    section_id = request.GET.get('section')
    news_sections = NewsSection.objects.filter(status='active').order_by('-priority', 'name')
    articles = NewsArticle.objects.filter(status='published', publish_time__lte=timezone.now()).order_by('-publish_time')
    if section_id:
        articles = articles.filter(section_id=section_id)
    context = {
        'news_sections': news_sections,
        'articles': articles,
        'selected_section': int(section_id) if section_id else None,
    }
    return render(request, 'news/news_archive.html', context)

def news_detail(request, pk):
    article = get_object_or_404(NewsArticle, pk=pk, status='published', publish_time__lte=timezone.now())
    attachments = article.attachments.all()
    return render(request, 'news/news_detail.html', {
        'article': article,
        'attachments': attachments,
    })

def news_section(request, section_id):
    section = get_object_or_404(NewsSection, pk=section_id, status='active')
    articles = section.articles.filter(status='published', publish_time__lte=timezone.now()).order_by('-publish_time')
    return render(request, 'news/news_section.html', {
        'section': section,
        'articles': articles,
    })
