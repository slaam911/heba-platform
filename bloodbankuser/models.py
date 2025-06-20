from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.

class BloodBankUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('يجب إدخال البريد الإلكتروني')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class BloodBankUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True, verbose_name='اسم المستخدم')
    email = models.EmailField(unique=True, verbose_name='البريد الإلكتروني')
    bloodbank_name = models.CharField(max_length=150, verbose_name='اسم بنك الدم')
    hospital_name = models.CharField(max_length=150, verbose_name='اسم المستشفى التابع له')
    region = models.CharField(max_length=20, verbose_name='المنطقة')
    city = models.CharField(max_length=100, verbose_name='المدينة')
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
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False, verbose_name='تم اعتماد العضوية')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخر تحديث')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='bloodbankuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='bloodbankuser_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'bloodbank_name', 'region', 'city']

    objects = BloodBankUserManager()

    class Meta:
        verbose_name = 'عضوية بنك دم'
        verbose_name_plural = 'عضويات بنوك الدم'

    def __str__(self):
        return self.bloodbank_name
