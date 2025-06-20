from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from donationuser.models import CustomUser, SiteSettings, VerificationCode, City
from django.utils import timezone
import re
import json

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='البريد الإلكتروني')
    phone_number = forms.CharField(max_length=15, required=True, label='رقم الجوال')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'مطلوب. 25 حرف أو أقل. أحرف وأرقام فقط.'
        self.fields['password1'].help_text = 'كلمة المرور يجب أن تحتوي على 8 أحرف على الأقل، حرف كبير، حرف صغير، رقم ورمز خاص.'
        self.fields['password2'].help_text = 'أدخل نفس كلمة المرور للتأكيد.'
        self.fields['username'].label = 'اسم المستخدم'
        self.fields['password1'].label = 'كلمة المرور'
        self.fields['password2'].label = 'تأكيد كلمة المرور'
        # إخفاء الحقول الأخرى إذا وجدت
        for field in list(self.fields.keys()):
            if field not in self.Meta.fields:
                self.fields.pop(field)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) > 25:
            raise ValidationError('اسم المستخدم يجب أن لا يتجاوز 25 حرف.')
        
        if not re.match(r'^[a-zA-Z0-9]+$', username):
            raise ValidationError('اسم المستخدم يجب أن يحتوي على أحرف وأرقام فقط.')
        
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError('اسم المستخدم مستخدم بالفعل. الرجاء اختيار اسم مستخدم آخر.')
        return username

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError('كلمة المرور يجب أن تكون 8 أحرف على الأقل.')
        
        if not re.search(r'[A-Z]', password):
            raise ValidationError('كلمة المرور يجب أن تحتوي على حرف كبير واحد على الأقل.')
        
        if not re.search(r'[a-z]', password):
            raise ValidationError('كلمة المرور يجب أن تحتوي على حرف صغير واحد على الأقل.')
        
        if not re.search(r'[0-9]', password):
            raise ValidationError('كلمة المرور يجب أن تحتوي على رقم واحد على الأقل.')
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError('كلمة المرور يجب أن تحتوي على رمز خاص واحد على الأقل.')
        
        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('البريد الإلكتروني مستخدم بالفعل. الرجاء استخدام بريد إلكتروني آخر.')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not re.match(r'^\d{10}$', phone_number):
            raise ValidationError('رقم الجوال يجب أن يكون 10 أرقام.')
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            raise ValidationError('رقم الهاتف مستخدم بالفعل. الرجاء استخدام رقم هاتف آخر.')
        return phone_number

    def clean_social_accounts(self):
        social_accounts = self.cleaned_data.get('social_accounts')
        if social_accounts:
            try:
                accounts = json.loads(social_accounts)
                if not isinstance(accounts, dict):
                    raise ValidationError('صيغة حسابات التواصل الاجتماعي غير صحيحة.')
                return accounts
            except json.JSONDecodeError:
                raise ValidationError('صيغة حسابات التواصل الاجتماعي غير صحيحة.')
        return {}

    def clean(self):
        cleaned_data = super().clean()
        has_donated = cleaned_data.get('has_donated')
        previous_blood_bank = cleaned_data.get('previous_blood_bank')
        has_chronic_disease = cleaned_data.get('has_chronic_disease')
        chronic_disease_type = cleaned_data.get('chronic_disease_type')

        if has_donated == True and not previous_blood_bank:
            self.add_error('previous_blood_bank', 'يرجى إدخال اسم بنك الدم')

        if has_chronic_disease == True and not chronic_disease_type:
            self.add_error('chronic_disease_type', 'يرجى إدخال نوع المرض')

        # التحقق من أن المستخدم اختار قيمة غير "غير محدد" في الحقول المطلوبة
        for field in ['gender', 'blood_type', 'has_donated', 'has_chronic_disease']:
            if cleaned_data.get(field) == '' or cleaned_data.get(field) == 'غير محدد':
                self.add_error(field, 'يرجى اختيار قيمة صحيحة')

        return cleaned_data

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='اسم المستخدم')
    password = forms.CharField(widget=forms.PasswordInput, label='كلمة المرور')

class VerificationCodeForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        min_length=6,
        label='رمز التحقق',
        widget=forms.TextInput(attrs={'placeholder': 'أدخل رمز التحقق المكون من 6 أرقام'})
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if not self.user:
            raise ValidationError('خطأ في التحقق من المستخدم.')
        
        try:
            verification = VerificationCode.objects.get(
                user=self.user,
                code=code,
                is_used=False,
                expires_at__gt=timezone.now()
            )
            verification.is_used = True
            verification.save()
            self.user.is_verified = True
            self.user.save()
            return code
        except VerificationCode.DoesNotExist:
            raise ValidationError('رمز التحقق غير صحيح أو منتهي الصلاحية.')

class BloodBankRegistrationForm(forms.Form):
    # معلومات بنك الدم
    bloodbank_name = forms.CharField(max_length=150, required=True, label='اسم بنك الدم')
    hospital_name = forms.CharField(max_length=150, required=True, label='اسم المستشفى التابع له')
    region = forms.ChoiceField(choices=CustomUser.REGION_CHOICES, required=True, label='المنطقة')
    city = forms.ModelChoiceField(queryset=City.objects.filter(is_active=True), required=True, label='المدينة')
    contact_number = forms.CharField(max_length=20, required=True, label='رقم التواصل')
    address = forms.CharField(widget=forms.Textarea(attrs={'rows':2}), required=True, label='العنوان')
    map_location = forms.CharField(widget=forms.HiddenInput(), required=False, label='موقع بنك الدم على الخريطة')
    working_hours = forms.CharField(max_length=100, required=True, label='أوقات العمل (الأيام - الساعات)')
    special_instructions = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), required=False, label='تعليمات خاصة')

    # معلومات مسؤول بنك الدم
    manager_name = forms.CharField(max_length=100, required=True, label='اسم المسؤول')
    manager_phone = forms.CharField(max_length=20, required=True, label='رقم هاتف المسؤول')
    manager_email = forms.EmailField(required=True, label='البريد الإلكتروني للمسؤول')
    manager_position = forms.CharField(max_length=100, required=True, label='المسمى الوظيفي')

class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        exclude = ('username', 'date_joined', 'last_login', 'password', 'is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions', 'verification_code', 'verification_code_created_at')
        widgets = {
            'avatar': forms.FileInput(),
            'region': forms.Select(choices=CustomUser.REGION_CHOICES),
            'gender': forms.Select(choices=CustomUser.GENDER_CHOICES),
            'blood_type': forms.Select(choices=CustomUser.BLOOD_TYPE_CHOICES),
            'privacy': forms.Select(choices=[('public', 'عام'), ('members', 'للأعضاء فقط'), ('private', 'خاص')]),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['district'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['phone_number'].widget = forms.TextInput(attrs={'class': 'form-control'})
        self.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control'})
        self.fields['avatar'].widget.attrs.update({'class': 'form-control'}) 