from django.contrib import admin
from django import forms
from .models import SiteStyle
from django.utils.safestring import mark_safe

@admin.register(SiteStyle)
class SiteStyleAdmin(admin.ModelAdmin):
    list_display = ('main_color', 'background_color', 'navbar_color', 'footer_color')
    fieldsets = (
        ("الألوان الرئيسية", {
            'fields': ('main_color', 'secondary_color', 'background_color', 'navbar_color', 'navbar_text_color', 'footer_color', 'footer_text_color', 'link_color', 'link_hover_color', 'success_color', 'warning_color', 'danger_color', 'info_color', 'text_color', 'muted_text_color', 'border_color')
        }),
        ("الخطوط", {
            'fields': ('heading_font', 'body_font')
        }),
        ("البطاقات والأزرار", {
            'fields': ('card_radius', 'card_shadow', 'button_radius', 'button_shadow', 'button_hover_color', 'border_radius_global')
        }),
    )
    readonly_fields = ()

    def has_add_permission(self, request):
        # السماح بالإضافة فقط إذا لم يوجد سجل إعدادات
        if SiteStyle.objects.exists():
            return False
        return True

    def changelist_view(self, request, extra_context=None):
        # إذا لم يوجد إعدادات، أنشئها تلقائياً
        if not SiteStyle.objects.exists():
            SiteStyle.objects.create()
        return super().changelist_view(request, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        # إضافة توضيحات لكل خاصية في صفحة التفاصيل
        extra_context = extra_context or {}
        extra_context['style_help'] = mark_safe("""
        <div style='background:#f7f8fa;padding:15px;border-radius:10px;margin-bottom:20px;'>
        <b>شرح إعدادات التصميم:</b><br>
        <ul style='line-height:2;'>
        <li><b>main_color:</b> اللون الرئيسي للأزرار والعناوين.</li>
        <li><b>secondary_color:</b> لون خلفية البطاقات أو العناصر الثانوية.</li>
        <li><b>background_color:</b> لون خلفية الموقع بالكامل.</li>
        <li><b>navbar_color:</b> لون شريط التنقل العلوي.</li>
        <li><b>navbar_text_color:</b> لون نص شريط التنقل.</li>
        <li><b>footer_color:</b> لون خلفية الفوتر السفلي.</li>
        <li><b>footer_text_color:</b> لون نص الفوتر السفلي.</li>
        <li><b>card_radius:</b> درجة انحناء زوايا البطاقات (px أو rem).</li>
        <li><b>card_shadow:</b> تأثير ظل البطاقات (box-shadow).</li>
        <li><b>button_radius:</b> درجة انحناء زوايا الأزرار.</li>
        <li><b>button_shadow:</b> تأثير ظل الأزرار.</li>
        <li><b>button_hover_color:</b> لون الزر عند التحويم.</li>
        <li><b>text_color:</b> لون النص الأساسي.</li>
        <li><b>muted_text_color:</b> لون النص الثانوي/المساعد.</li>
        <li><b>heading_font:</b> خط العناوين (مثال: 'Cairo', sans-serif).</li>
        <li><b>body_font:</b> خط النصوص العادية.</li>
        <li><b>border_color:</b> لون حدود البطاقات والعناصر.</li>
        <li><b>link_color:</b> لون الروابط.</li>
        <li><b>link_hover_color:</b> لون الروابط عند التحويم.</li>
        <li><b>success_color:</b> لون رسائل النجاح.</li>
        <li><b>warning_color:</b> لون رسائل التحذير.</li>
        <li><b>danger_color:</b> لون رسائل الخطأ.</li>
        <li><b>info_color:</b> لون رسائل المعلومات.</li>
        <li><b>border_radius_global:</b> درجة انحناء الزوايا العامة لكل العناصر.</li>
        </ul></div>
        """)
        return super().change_view(request, object_id, form_url, extra_context=extra_context) 