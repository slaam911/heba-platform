from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
import random
import string
from .forms import UserRegistrationForm, UserLoginForm, VerificationCodeForm, BloodBankRegistrationForm, UserEditForm
from donationuser.models import CustomUser, SiteSettings, VerificationCode, City
from .models import BloodBankProfile
from django.views.decorators.http import require_http_methods
from django.contrib.auth.forms import AuthenticationForm

@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # تعطيل الحساب حتى يتم التحقق
            user.save()
            
            # إرسال بريد التحقق
            try:
                user.send_verification_email()
                messages.success(request, 'تم إنشاء حسابك بنجاح! يرجى التحقق من بريدك الإلكتروني لتفعيل الحساب.')
                return redirect('users:register_success')
            except Exception as e:
                messages.error(request, 'حدث خطأ أثناء إرسال بريد التحقق. يرجى المحاولة مرة أخرى.')
                return redirect('users:register')
        else:
            messages.error(request, 'يرجى تصحيح الأخطاء أدناه.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})

def register_success(request):
    return render(request, 'users/register_success.html')

def verify_code(request):
    if request.method == 'POST':
        form = VerificationCodeForm(request.POST, user=request.user)
        if form.is_valid():
            messages.success(request, 'تم التحقق من حسابك بنجاح!')
            return redirect('core:home')
    else:
        form = VerificationCodeForm(user=request.user)
    return render(request, 'users/verify_code.html', {'form': form})

def resend_code(request):
    if request.user.is_authenticated and not request.user.is_verified:
        try:
            request.user.send_verification_email()
            messages.success(request, 'تم إرسال رمز التحقق الجديد إلى بريدك الإلكتروني.')
        except Exception as e:
            messages.error(request, 'حدث خطأ أثناء إرسال رمز التحقق. يرجى المحاولة مرة أخرى.')
    return redirect('users:verify_code')

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('profile')
                else:
                    form.add_error(None, 'الحساب غير مفعل. يرجى التحقق من بريدك الإلكتروني.')
            else:
                form.add_error(None, 'اسم المستخدم أو كلمة المرور غير صحيحة.')
    else:
        form = UserLoginForm()
    
    return render(request, 'users/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'تم تسجيل الخروج بنجاح!')
    return redirect('users:login')

@login_required
def profile(request, username):
    if request.user.username != username:
        return redirect('users:public_profile', username=username)
    user = request.user
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث بياناتك بنجاح.')
            return redirect('users:profile_edit', username=user.username)
    else:
        form = UserEditForm(instance=user)
    return render(request, 'users/profile_edit.html', {'form': form, 'user': user})

def public_profile(request, username):
    user = get_object_or_404(CustomUser, username=username, is_active=True)
    # منطق الخصوصية: إظهار فقط البيانات العامة أو للأعضاء حسب user.privacy
    show_all = user.privacy == 'public' or (user.privacy == 'members' and request.user.is_authenticated)
    return render(request, 'users/public_profile.html', {'profile_user': user, 'show_all': show_all})

@require_http_methods(["GET"])
def get_cities(request):
    region = request.GET.get('region')
    if not region:
        return JsonResponse({'error': 'المنطقة مطلوبة'}, status=400)
    
    cities = City.objects.filter(region=region, is_active=True).values('id', 'name')
    return JsonResponse(list(cities), safe=False)

def select_registration_type(request):
    return render(request, 'users/select_registration_type.html')

def register_bloodbank(request):
    if request.method == 'POST':
        form = BloodBankRegistrationForm(request.POST)
        if form.is_valid():
            # حفظ البيانات في قاعدة البيانات وربطها بالمستخدم
            profile = BloodBankProfile.objects.create(
                user=request.user if request.user.is_authenticated else None,
                bloodbank_name=form.cleaned_data['bloodbank_name'],
                hospital_name=form.cleaned_data['hospital_name'],
                region=form.cleaned_data['region'],
                city=form.cleaned_data['city'],
                contact_number=form.cleaned_data['contact_number'],
                address=form.cleaned_data['address'],
                map_location=form.cleaned_data['map_location'],
                working_hours=form.cleaned_data['working_hours'],
                special_instructions=form.cleaned_data['special_instructions'],
                manager_name=form.cleaned_data['manager_name'],
                manager_phone=form.cleaned_data['manager_phone'],
                manager_email=form.cleaned_data['manager_email'],
                manager_position=form.cleaned_data['manager_position'],
                is_approved=False
            )
            messages.success(request, 'تم إرسال طلب تسجيل بنك الدم بنجاح! سيتم مراجعة الطلب من قبل الإدارة.')
            return render(request, 'users/bloodbank_register_success.html')
    else:
        form = BloodBankRegistrationForm()
    return render(request, 'users/bloodbank_register.html', {'form': form})

# صفحة عرض بيانات بنك الدم (تظهر فقط بعد الاعتماد)
@login_required
def bloodbank_profile(request):
    try:
        profile = request.user.bloodbank_profile
        if not profile.is_approved:
            return render(request, 'users/bloodbank_pending.html')
        return render(request, 'users/bloodbank_profile.html', {'profile': profile})
    except BloodBankProfile.DoesNotExist:
        return render(request, 'users/bloodbank_no_profile.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # رسالة ترحيبية مع رابط الملف التعريفي
            messages.success(request, 'شكرًا لانضمامك إلى منصة هبة! يمكنك الآن <a href="/users/profile/" class="fw-bold text-danger">الضغط هنا لإكمال بيانات ملفك التعريفي</a>.')
            return redirect('users:register_success')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'تم تسجيل الدخول بنجاح!')
            return redirect('home')
        else:
            messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة')
    return render(request, 'users/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'تم تسجيل الخروج بنجاح!')
    return redirect('home')

def get_cities(request):
    region = request.GET.get('region')
    if not region:
        return JsonResponse({'error': 'المنطقة مطلوبة'}, status=400)
    
    cities = City.objects.filter(region=region, is_active=True).values('id', 'name')
    return JsonResponse({'cities': list(cities)})
