from django.db import models

# Create your models here.

BLOOD_TYPE_CHOICES = [
    ('A+', 'A+'), ('A-', 'A-'),
    ('B+', 'B+'), ('B-', 'B-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'),
    ('O+', 'O+'), ('O-', 'O-'),
]

BLOOD_COMPONENT_CHOICES = [
    ('whole', 'دم كامل'),
    ('plasma', 'بلازما'),
    ('platelets', 'صفائح دموية'),
]

GENDER_CHOICES = [
    ('male', 'ذكر'),
    ('female', 'أنثى'),
]

REQUEST_STATUS_CHOICES = [
    ('pending', 'معلق'),
    ('review', 'قيد المراجعة'),
    ('approved', 'معتمد'),
    ('rejected', 'مرفوض'),
]

class BloodRequest(models.Model):
    case_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='اسم الحالة')
    blood_component = models.CharField(max_length=20, choices=BLOOD_COMPONENT_CHOICES, verbose_name='نوع الدم المطلوب')
    blood_type = models.CharField(max_length=5, choices=BLOOD_TYPE_CHOICES, verbose_name='فصيلة الدم المطلوبة')
    city = models.CharField(max_length=100, verbose_name='المدينة')
    hospital_name = models.CharField(max_length=255, verbose_name='اسم المستشفى')
    location_url = models.URLField(blank=True, null=True, verbose_name='رابط الموقع الجغرافي')
    units_needed = models.PositiveIntegerField(verbose_name='عدد الوحدات المطلوبة')
    is_critical = models.BooleanField(default=False, verbose_name='هل الحالة حرجة؟')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name='الجنس')
    age = models.PositiveIntegerField(verbose_name='العمر')
    contact_number = models.CharField(max_length=20, verbose_name='رقم التواصل')
    description = models.TextField(blank=True, null=True, verbose_name='وصف إضافي')
    medical_report = models.FileField(upload_to='medical_reports/', blank=True, null=True, verbose_name='تقرير طبي')
    status = models.CharField(max_length=20, choices=REQUEST_STATUS_CHOICES, default='pending', verbose_name='حالة الطلب')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخر تحديث')
    notes = models.TextField(blank=True, null=True, verbose_name='ملاحظات المشرف')

    def __str__(self):
        return f"{self.case_name or self.hospital_name} - {self.blood_type} ({self.city})"
