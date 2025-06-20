from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
import random
import string

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

USER_TYPE_CHOICES = [
    ('donor', 'متبرع'),
    ('blood_bank', 'بنك دم'),
    ('supervisor', 'مشرف'),
    ('admin', 'مدير'),
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

# تم حذف نموذج CustomUser و SiteSettings و VerificationCode من هنا بعد نقلهم إلى donationuser

class BloodBankProfile(models.Model):
    # user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='bloodbank_profile', verbose_name='المستخدم المسؤول')  # تم حذف هذا الحقل
    bloodbank_name = models.CharField(max_length=150, verbose_name='اسم بنك الدم')
    hospital_name = models.CharField(max_length=150, verbose_name='اسم المستشفى التابع له')
    region = models.CharField(max_length=20, choices=REGION_CHOICES, verbose_name='المنطقة')
    city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True, verbose_name='المدينة')
    contact_number = models.CharField(max_length=20, verbose_name='رقم التواصل')
    address = models.TextField(verbose_name='العنوان')
    map_location = models.CharField(max_length=100, blank=True, null=True, verbose_name='إحداثيات الموقع')
    working_hours = models.CharField(max_length=100, verbose_name='أوقات العمل (الأيام - الساعات)')
    special_instructions = models.TextField(blank=True, null=True, verbose_name='تعليمات خاصة')
    # معلومات المسؤول
    manager_name = models.CharField(max_length=100, verbose_name='اسم المسؤول')
    manager_phone = models.CharField(max_length=20, verbose_name='رقم هاتف المسؤول')
    manager_email = models.EmailField(verbose_name='البريد الإلكتروني للمسؤول')
    manager_position = models.CharField(max_length=100, verbose_name='المسمى الوظيفي')
    is_approved = models.BooleanField(default=False, verbose_name='تم اعتماد العضوية')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخر تحديث')

    class Meta:
        verbose_name = 'بيانات بنك الدم'
        verbose_name_plural = 'بيانات بنوك الدم'

    def __str__(self):
        return self.bloodbank_name
