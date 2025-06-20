from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import BloodBankUserRegistrationForm


def bloodbankuser_register(request):
    if request.method == 'POST':
        form = BloodBankUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # يمكن إرسال إشعار أو رسالة نجاح هنا
            return render(request, 'bloodbankuser/bloodbankuser_register_success.html')
    else:
        form = BloodBankUserRegistrationForm()
    return render(request, 'bloodbankuser/bloodbankuser_register.html', {'form': form})


def bloodbankuser_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('bloodbankuser:bloodbankuser_profile')
            else:
                form.add_error(None, 'بيانات الدخول غير صحيحة أو ليس لديك عضوية بنك دم')
    else:
        form = AuthenticationForm()
    return render(request, 'bloodbankuser/bloodbankuser_login.html', {'form': form})


@login_required
def bloodbankuser_profile(request):
    user = request.user
    return render(request, 'bloodbankuser/bloodbankuser_profile.html', {'profile': user})
