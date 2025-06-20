from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .models import BloodRequest
from .forms import BloodRequestForm

def request_list(request):
    """عرض قائمة طلبات التبرع بالدم"""
    requests = BloodRequest.objects.filter(status='approved').order_by('-created_at')
    return render(request, 'blood_requests/request_list.html', {
        'requests': requests
    })

def request_create(request):
    """إنشاء طلب تبرع بالدم جديد"""
    if request.method == 'POST':
        form = BloodRequestForm(request.POST, request.FILES)
        if form.is_valid():
            blood_request = form.save(commit=False)
            blood_request.status = 'pending'
            blood_request.save()
            return redirect('blood_requests:success', request_id=blood_request.request_id)
    else:
        form = BloodRequestForm()
    
    return render(request, 'blood_requests/request_form.html', {
        'form': form
    })

def request_detail(request, request_id):
    """عرض تفاصيل طلب تبرع بالدم"""
    blood_request = get_object_or_404(BloodRequest, request_id=request_id)
    return render(request, 'blood_requests/request_detail.html', {
        'request': blood_request,
        'request_url': request.build_absolute_uri()
    })

def request_success(request, request_id):
    """صفحة نجاح إنشاء طلب التبرع"""
    blood_request = get_object_or_404(BloodRequest, request_id=request_id)
    return render(request, 'blood_requests/request_success.html', {
        'request': blood_request
    }) 