from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Campaign, CampaignGallery
from django.db.models import Q

def campaign_list(request):
    city = request.GET.get('city')
    status = request.GET.get('status')
    campaigns = Campaign.objects.all().order_by('-start_date')
    if city:
        campaigns = campaigns.filter(city=city)
    if status:
        campaigns = [c for c in campaigns if c.get_current_status() == status]
    else:
        campaigns = list(campaigns)
    cities = Campaign.objects.values_list('city', flat=True).distinct()
    return render(request, 'campaigns/campaign_list.html', {
        'campaigns': campaigns,
        'cities': cities,
        'selected_city': city,
        'selected_status': status,
    })

def campaign_detail(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    gallery = campaign.gallery.all()
    return render(request, 'campaigns/campaign_detail.html', {
        'campaign': campaign,
        'gallery': gallery,
    })

@login_required
def campaign_create(request):
    if request.method == 'POST':
        # سيتم إضافة المنطق لاحقاً
        messages.success(request, 'تم إنشاء الحملة بنجاح')
        return redirect('campaigns:list')
    return render(request, 'campaigns/create.html')

@login_required
def campaign_edit(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    if request.method == 'POST':
        # سيتم إضافة المنطق لاحقاً
        messages.success(request, 'تم تحديث الحملة بنجاح')
        return redirect('campaigns:detail', pk=pk)
    return render(request, 'campaigns/edit.html', {'campaign': campaign})

@login_required
def campaign_delete(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    if request.method == 'POST':
        campaign.delete()
        messages.success(request, 'تم حذف الحملة بنجاح')
        return redirect('campaigns:list')
    return render(request, 'campaigns/delete.html', {'campaign': campaign})
