from django.db import models
from tinymce.models import HTMLField

BLOOD_TYPE_CHOICES = [
    ('A+', 'A+'), ('A-', 'A-'),
    ('B+', 'B+'), ('B-', 'B-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'),
    ('O+', 'O+'), ('O-', 'O-'),
]

CAMPAIGN_STATUS_CHOICES = [
    ('upcoming', 'قادمة'),
    ('active', 'جارية'),
    ('ended', 'منتهية'),
    ('draft', 'مسودة'),
    ('cancelled', 'ملغاة'),
]

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

class Campaign(models.Model):
    title = models.CharField(max_length=255, verbose_name='عنوان الحملة')
    cover_image = models.ImageField(upload_to='campaigns/covers/', verbose_name='الصورة الرمزية', blank=True, null=True)
    description = HTMLField(verbose_name='وصف الحملة')
    location_name = models.CharField(max_length=255, verbose_name='اسم الموقع/المقر', blank=True, null=True)
    google_maps_url = models.URLField(blank=True, null=True, verbose_name='رابط Google Maps')
    region = models.CharField(max_length=20, choices=REGION_CHOICES, verbose_name='المنطقة', blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name='المدينة', blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True, verbose_name='الحي')
    organizer_bank = models.CharField(max_length=255, verbose_name='اسم بنك الدم المنظم', blank=True, null=True)
    partners = models.CharField(max_length=255, blank=True, null=True, verbose_name='الشركاء (اختياري)')
    supervisor_name = models.CharField(max_length=100, verbose_name='اسم المشرف/المنسق', blank=True, null=True)
    supervisor_phone = models.CharField(max_length=20, verbose_name='رقم التواصل للمشرف', blank=True, null=True)
    start_date = models.DateTimeField(verbose_name='تاريخ البداية')
    end_date = models.DateTimeField(verbose_name='تاريخ الانتهاء')
    status = models.CharField(max_length=20, choices=CAMPAIGN_STATUS_CHOICES, default='upcoming', verbose_name='حالة الحملة')
    manual_status = models.BooleanField(default=False, verbose_name='تفعيل التحكم اليدوي بالحالة')
    notes = models.TextField(blank=True, null=True, verbose_name='ملاحظات')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخر تحديث')

    def __str__(self):
        return self.title

    def get_current_status(self):
        from django.utils import timezone
        now = timezone.now()
        if self.manual_status:
            return self.status
        if self.start_date > now:
            return 'upcoming'
        elif self.start_date <= now <= self.end_date:
            return 'active'
        else:
            return 'ended'

class CampaignGallery(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='gallery', verbose_name='الحملة')
    image = models.ImageField(upload_to='campaigns/gallery/', verbose_name='صورة إضافية')
    alt_text = models.CharField(max_length=255, blank=True, null=True, verbose_name='وصف للصورة')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"صورة لحملة: {self.campaign.title}"
