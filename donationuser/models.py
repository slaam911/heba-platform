from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import random
import string
from django.utils import timezone
from django.contrib.postgres.fields import JSONField
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.conf import settings

REGION_CHOICES = [
    ('riyadh', 'الرياض'),
    ('makkah', 'مكة المكرمة'),
    ('madinah', 'المدينة المنورة'),
    ('eastern', 'المنطقة الشرقية'),
    ('asir', 'عسير'),
    ('tabuk', 'تبوك'),
    ('hail', 'حائل'),
    ('northern_border', 'الحدود الشمالية'),
    ('jazan', 'جازان'),
    ('najran', 'نجران'),
    ('bahah', 'الباحة'),
    ('jawf', 'الجوف'),
    ('qassim', 'القصيم'),
]

class City(models.Model):
    name = models.CharField(max_length=100, verbose_name='اسم المدينة')
    region = models.CharField(max_length=20, choices=REGION_CHOICES, verbose_name='المنطقة')
    is_active = models.BooleanField(default=True, verbose_name='نشط')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    class Meta:
        verbose_name = 'مدينة'
        verbose_name_plural = 'المدن'
        ordering = ['region', 'name']

    def __str__(self):
        return f"{self.name} - {self.get_region_display()}"

class CustomUser(AbstractUser):
    GENDER_CHOICES = [('', 'غير محدد'), ('male', 'ذكر'), ('female', 'أنثى')]
    NATIONALITY_CHOICES = [
        ('SA', 'سعودي'),
        ('OTHER', 'أخرى'),
    ]
    REGION_CHOICES = REGION_CHOICES
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    # الاسم الثلاثي
    first_name = models.CharField(_('الاسم الأول'), max_length=30)
    middle_name = models.CharField(_('اسم الأب'), max_length=30)
    last_name = models.CharField(_('اسم العائلة'), max_length=30)
    # رقم الجوال
    phone_number = models.CharField(_('رقم الجوال'), max_length=10, unique=True, validators=[RegexValidator(r'^\d{10}$', 'رقم الجوال يجب أن يكون 10 أرقام')])
    # البريد الإلكتروني
    email = models.EmailField(_('البريد الإلكتروني'), unique=True)
    # اسم المستخدم (إنجليزي فقط، ≤25 حرف، فريد)
    username = models.CharField(_('اسم المستخدم'), max_length=25, unique=True, validators=[RegexValidator(r'^[a-zA-Z0-9]+$', 'اسم المستخدم يجب أن يكون أحرف وأرقام إنجليزية فقط')])
    # صورة رمزية
    avatar = models.ImageField(_('الصورة الرمزية'), upload_to='avatars/', blank=True, null=True, default='images/default-avatar.png')
    # الجنس
    gender = models.CharField(_('الجنس'), max_length=10, choices=[('male', 'ذكر'), ('female', 'أنثى')], blank=True, null=True)
    # العمر
    age = models.PositiveIntegerField(_('العمر'), blank=True, null=True)
    # المنطقة والمدينة والحي
    region = models.CharField(_('المنطقة'), max_length=20, choices=REGION_CHOICES)
    city = models.CharField(_('المدينة'), max_length=100, blank=True, null=True)
    district = models.CharField(_('الحي'), max_length=100, blank=True, null=True)
    # حسابات التواصل الاجتماعي (قائمة ديناميكية)
    social_accounts = models.JSONField(_('حسابات التواصل الاجتماعي'), blank=True, null=True, default=dict)
    # معلومات صحية
    blood_type = models.CharField(_('فصيلة الدم'), max_length=3, choices=BLOOD_TYPE_CHOICES, default='A+')
    has_donated = models.BooleanField(_('هل سبق لك التبرع بالدم؟'), default=False)
    previous_blood_bank = models.CharField(_('اسم بنك الدم الذي تبرعت فيه مؤخرًا'), max_length=200, blank=True, null=True)
    has_chronic_disease = models.BooleanField(_('هل لديك أمراض مزمنة؟'), default=False)
    chronic_disease_type = models.CharField(_('اسم المرض المزمن'), max_length=200, blank=True, null=True)
    # خيارات الخصوصية
    privacy = models.CharField(_('خصوصية الملف'), max_length=20, choices=[('public', 'عام'), ('members', 'للأعضاء فقط'), ('private', 'خاص')], default='members')
    # عدد مرات التبرع، الشارات، الأوسمة (قابلة للتوسع)
    donation_count = models.PositiveIntegerField(_('عدد مرات التبرع'), default=0)
    badges = models.JSONField(_('الشارات/الأوسمة'), blank=True, null=True, default=dict)
    # باقي الحقول الافتراضية (is_active, is_staff, ...)
    is_verified = models.BooleanField(_('تم التحقق'), default=False)
    verification_code = models.CharField(_('رمز التحقق'), max_length=6, blank=True, null=True)
    verification_code_created_at = models.DateTimeField(_('تاريخ إنشاء رمز التحقق'), null=True, blank=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    class Meta:
        verbose_name = _('مستخدم')
        verbose_name_plural = _('المستخدمين')
    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"
    def get_full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"
    def send_verification_email(self):
        # TODO: تنفيذ إرسال البريد الإلكتروني
        pass
    def get_avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return f"{settings.STATIC_URL}images/default-avatar.png"

class SiteSettings(models.Model):
    verification_required = models.BooleanField(default=True, verbose_name='تفعيل التحقق')
    verify_email = models.BooleanField(default=True, verbose_name='تفعيل التحقق بالبريد الإلكتروني')
    verify_phone = models.BooleanField(default=True, verbose_name='تفعيل التحقق بالجوال')
    require_full_name = models.BooleanField(default=True, verbose_name='الاسم الثلاثي')
    require_age = models.BooleanField(default=True, verbose_name='العمر')
    require_nationality = models.BooleanField(default=True, verbose_name='الجنسية')
    require_city = models.BooleanField(default=True, verbose_name='المدينة')
    require_blood_type = models.BooleanField(default=True, verbose_name='فصيلة الدم')
    require_previous_donation = models.BooleanField(default=True, verbose_name='التبرع السابق')
    require_chronic_diseases = models.BooleanField(default=True, verbose_name='الأمراض المزمنة')
    class Meta:
        verbose_name = 'إعدادات الموقع'
        verbose_name_plural = 'إعدادات الموقع'
    def __str__(self):
        return 'إعدادات الموقع'

class VerificationCode(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='المستخدم')
    code = models.CharField(max_length=6, verbose_name='رمز التحقق')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    expires_at = models.DateTimeField(verbose_name='تاريخ الانتهاء')
    is_used = models.BooleanField(default=False, verbose_name='تم الاستخدام')
    verification_method = models.CharField(max_length=10, choices=[('email', 'البريد الإلكتروني'), ('phone', 'الجوال')], verbose_name='طريقة التحقق')
    class Meta:
        verbose_name = 'رمز تحقق'
        verbose_name_plural = 'رموز التحقق'
    def __str__(self):
        return f"رمز التحقق لـ {self.user.username}"
    @classmethod
    def generate_code(cls, user, verification_method):
        cls.objects.filter(user=user, is_used=False).delete()
        code = ''.join(random.choices(string.digits, k=6))
        expires_at = timezone.now() + timezone.timedelta(minutes=15)
        return cls.objects.create(
            user=user,
            code=code,
            expires_at=expires_at,
            verification_method=verification_method
        )
