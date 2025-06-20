from django.db import models
from django.utils import timezone
from django.utils.text import slugify
import uuid

class BloodRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'قيد التحقق'),
        ('approved', 'تم التحقق'),
        ('rejected', 'مرفوض'),
        ('completed', 'منتهي'),
        ('upcoming', 'قادم')
    ]
    
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-')
    ]
    
    BLOOD_COMPONENT_CHOICES = [
        ('whole', 'دم كامل'),
        ('plasma', 'بلازما'),
        ('platelets', 'صفائح دموية'),
        ('other', 'أخرى')
    ]
    
    GENDER_CHOICES = [
        ('male', 'ذكر'),
        ('female', 'أنثى')
    ]
    
    # معلومات المريض
    patient_name = models.CharField(max_length=100, verbose_name='اسم المريض')
    medical_file_number = models.CharField(max_length=50, verbose_name='رقم الملف الطبي')
    hospital_name = models.CharField(max_length=200, verbose_name='اسم المستشفى')
    city = models.ForeignKey('users.City', on_delete=models.PROTECT, verbose_name='المدينة')
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, verbose_name='فصيلة الدم المطلوبة')
    blood_component = models.CharField(max_length=20, choices=BLOOD_COMPONENT_CHOICES, verbose_name='نوع الدم المطلوب')
    patient_age = models.PositiveIntegerField(verbose_name='عمر المريض')
    patient_gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name='جنس المريض')
    units_needed = models.PositiveIntegerField(verbose_name='عدد الوحدات المطلوبة')
    is_critical = models.BooleanField(default=False, verbose_name='حالة حرجة')
    
    # معلومات التواصل
    contact_number = models.CharField(max_length=20, verbose_name='رقم للتواصل')
    additional_info = models.TextField(verbose_name='وصف إضافي للحالة')
    medical_report = models.FileField(upload_to='medical_reports/', verbose_name='التقرير الطبي')
    
    # معلومات النظام
    request_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='حالة الطلب')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name='تاريخ انتهاء الطلب')
    rejection_reason = models.TextField(null=True, blank=True, verbose_name='سبب الرفض')
    
    class Meta:
        verbose_name = 'طلب تبرع بالدم'
        verbose_name_plural = 'طلبات التبرع بالدم'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"طلب {self.request_id} - {self.patient_name}"
    
    def save(self, *args, **kwargs):
        if not self.request_id:
            self.request_id = uuid.uuid4()
        super().save(*args, **kwargs)
    
    @property
    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
    
    @property
    def time_remaining(self):
        if self.expires_at:
            remaining = self.expires_at - timezone.now()
            if remaining.total_seconds() > 0:
                return remaining
        return None 