from django.db import models
from django.conf import settings

# Create your models here.

NOTIFICATION_TYPE_CHOICES = [
    ('blood_request', 'طلب تبرع بالدم'),
    ('campaign', 'حملة تبرع'),
    ('system', 'إشعار نظام'),
    ('alert', 'تنبيه عاجل'),
]

NOTIFICATION_STATUS_CHOICES = [
    ('pending', 'معلق'),
    ('sent', 'تم الإرسال'),
    ('failed', 'فشل الإرسال'),
]

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='المستخدم')
    title = models.CharField(max_length=255, verbose_name='عنوان الإشعار')
    message = models.TextField(verbose_name='محتوى الإشعار')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES, verbose_name='نوع الإشعار')
    recipient = models.CharField(max_length=255, verbose_name='المستلم')
    status = models.CharField(max_length=20, choices=NOTIFICATION_STATUS_CHOICES, default='pending', verbose_name='حالة الإشعار')
    is_read = models.BooleanField(default=False, verbose_name='تم القراءة')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name='تاريخ الإرسال')
    read_at = models.DateTimeField(null=True, blank=True, verbose_name='تاريخ القراءة')
    metadata = models.JSONField(default=dict, blank=True, verbose_name='بيانات إضافية')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'إشعار'
        verbose_name_plural = 'الإشعارات'

    def __str__(self):
        return f"{self.title} - {self.user.get_full_name()}"
