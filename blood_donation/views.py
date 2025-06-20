from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BloodRequest

def donation_list(request):
    donations = BloodRequest.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'blood_donation/list.html', {'donations': donations})

def donation_detail(request, pk):
    donation = get_object_or_404(BloodRequest, pk=pk)
    return render(request, 'blood_donation/detail.html', {'donation': donation})

@login_required
def donation_create(request):
    if request.method == 'POST':
        # سيتم إضافة المنطق لاحقاً
        messages.success(request, 'تم إنشاء طلب التبرع بنجاح')
        return redirect('blood_donation:list')
    return render(request, 'blood_donation/create.html')

@login_required
def donation_edit(request, pk):
    donation = get_object_or_404(BloodRequest, pk=pk)
    if request.method == 'POST':
        # سيتم إضافة المنطق لاحقاً
        messages.success(request, 'تم تحديث طلب التبرع بنجاح')
        return redirect('blood_donation:detail', pk=pk)
    return render(request, 'blood_donation/edit.html', {'donation': donation})

@login_required
def donation_delete(request, pk):
    donation = get_object_or_404(BloodRequest, pk=pk)
    if request.method == 'POST':
        donation.delete()
        messages.success(request, 'تم حذف طلب التبرع بنجاح')
        return redirect('blood_donation:list')
    return render(request, 'blood_donation/delete.html', {'donation': donation})
