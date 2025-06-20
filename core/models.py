from django.db import models
from django.utils import timezone

class SiteStyle(models.Model):
    main_color = models.CharField(max_length=7, default="#b30000", help_text="اللون الرئيسي للموقع (الأزرار، العناوين)")
    secondary_color = models.CharField(max_length=7, default="#fff", help_text="اللون الثانوي (خلفية البطاقات)")
    background_color = models.CharField(max_length=7, default="#f7f8fa", help_text="لون خلفية الموقع")
    navbar_color = models.CharField(max_length=7, default="#b30000", help_text="لون شريط التنقل العلوي")
    navbar_text_color = models.CharField(max_length=7, default="#fff", help_text="لون نص شريط التنقل")
    footer_color = models.CharField(max_length=7, default="#1a2940", help_text="لون خلفية الفوتر")
    footer_text_color = models.CharField(max_length=7, default="#fff", help_text="لون نص الفوتر")
    card_radius = models.CharField(max_length=5, default="18px", help_text="درجة انحناء زوايا البطاقات")
    card_shadow = models.CharField(max_length=100, default="0 2px 16px #e6e6e6", help_text="تأثير ظل البطاقات")
    button_radius = models.CharField(max_length=5, default="18px", help_text="درجة انحناء زوايا الأزرار")
    button_shadow = models.CharField(max_length=100, default="none", help_text="تأثير ظل الأزرار")
    button_hover_color = models.CharField(max_length=7, default="#8c0000", help_text="لون الزر عند التحويم")
    text_color = models.CharField(max_length=7, default="#222", help_text="لون النص الأساسي")
    muted_text_color = models.CharField(max_length=7, default="#888", help_text="لون النص الثانوي/المساعد")
    heading_font = models.CharField(max_length=100, default="'Cairo', sans-serif", help_text="خط العناوين")
    body_font = models.CharField(max_length=100, default="'Cairo', sans-serif", help_text="خط النصوص")
    border_color = models.CharField(max_length=7, default="#e6e6e6", help_text="لون حدود البطاقات والعناصر")
    link_color = models.CharField(max_length=7, default="#b30000", help_text="لون الروابط")
    link_hover_color = models.CharField(max_length=7, default="#8c0000", help_text="لون الروابط عند التحويم")
    success_color = models.CharField(max_length=7, default="#28a745", help_text="لون النجاح/التنبيهات الإيجابية")
    warning_color = models.CharField(max_length=7, default="#ffc107", help_text="لون التحذير")
    danger_color = models.CharField(max_length=7, default="#dc3545", help_text="لون الخطر/الأخطاء")
    info_color = models.CharField(max_length=7, default="#17a2b8", help_text="لون المعلومات")
    border_radius_global = models.CharField(max_length=5, default="18px", help_text="درجة انحناء الزوايا العامة")
    
    class Meta:
        verbose_name = "إعدادات التصميم"
        verbose_name_plural = "إعدادات التصميم"

    def __str__(self):
        return "إعدادات التصميم للموقع" 