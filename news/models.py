from django.db import models
from django.utils import timezone

# Create your models here.

class NewsSection(models.Model):
    STATUS_CHOICES = [
        ('active', 'مفعل'),
        ('inactive', 'موقوف مؤقتًا'),
        ('deleted', 'محذوف')
    ]
    name = models.CharField(max_length=100, verbose_name='اسم القسم')
    description = models.TextField(max_length=300, blank=True, verbose_name='وصف مختصر')
    icon = models.ImageField(upload_to='news/sections/', blank=True, null=True, verbose_name='صورة رمزية')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='الحالة')
    target_audience = models.CharField(max_length=100, blank=True, verbose_name='الفئة المستهدفة')
    priority = models.PositiveIntegerField(default=0, verbose_name='أولوية الظهور')
    related_campaign = models.ForeignKey('campaigns.Campaign', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='حملة مرتبطة')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'قسم أخبار'
        verbose_name_plural = 'أقسام الأخبار'
        ordering = ['-priority', 'name']

    def __str__(self):
        return self.name

class NewsArticle(models.Model):
    PUBLISH_STATUS = [
        ('published', 'منشور'),
        ('cancelled', 'ملغي'),
        ('pending', 'قيد التحقق'),
        ('scheduled', 'بانتظار النشر'),
        ('deleted', 'محذوف')
    ]
    section = models.ForeignKey(NewsSection, on_delete=models.PROTECT, related_name='articles', verbose_name='القسم الفرعي')
    title = models.CharField(max_length=200, verbose_name='العنوان الرئيسي')
    subtitle = models.CharField(max_length=300, blank=True, verbose_name='العنوان الفرعي')
    summary = models.TextField(max_length=240, verbose_name='ملخص الخبر')
    content = models.TextField(verbose_name='نص الخبر')
    main_image = models.ImageField(upload_to='news/articles/', blank=True, null=True, verbose_name='الصورة الرئيسية')
    status = models.CharField(max_length=20, choices=PUBLISH_STATUS, default='pending', verbose_name='حالة النشر')
    publish_time = models.DateTimeField(default=timezone.now, verbose_name='وقت النشر')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'خبر'
        verbose_name_plural = 'الأخبار'
        ordering = ['-publish_time', '-created_at']

    def __str__(self):
        return self.title

class NewsAttachment(models.Model):
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE, related_name='attachments', verbose_name='الخبر')
    image = models.ImageField(upload_to='news/attachments/', verbose_name='صورة مرفقة')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'صورة مرفقة للخبر'
        verbose_name_plural = 'الصور المرفقة للأخبار'

    def __str__(self):
        return f"مرفق لـ {self.article.title}"
