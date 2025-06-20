from django.contrib import admin
from .models import Campaign, CampaignGallery

class CampaignGalleryInline(admin.TabularInline):
    model = CampaignGallery
    extra = 1
    fields = ('image', 'alt_text', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" style="border-radius:8px;box-shadow:0 2px 8px #ccc;" />'
        return "-"
    image_preview.allow_tags = True
    image_preview.short_description = 'معاينة الصورة'

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'region', 'city', 'start_date', 'end_date', 'get_current_status', 'created_at')
    list_filter = ('region', 'status', 'start_date', 'end_date')
    search_fields = ('title', 'region', 'city', 'organizer_bank', 'supervisor_name')
    inlines = [CampaignGalleryInline]
    readonly_fields = ('created_at', 'updated_at', 'cover_image_preview')
    fieldsets = (
        (None, {
            'fields': ('title', 'cover_image', 'cover_image_preview', 'description')
        }),
        ('الموقع', {
            'fields': ('location_name', 'google_maps_url', 'region', 'city', 'district')
        }),
        ('معلومات تنظيمية', {
            'fields': ('organizer_bank', 'partners', 'supervisor_name', 'supervisor_phone')
        }),
        ('التواريخ والحالة', {
            'fields': ('start_date', 'end_date', 'status', 'manual_status')
        }),
        ('أخرى', {
            'fields': ('notes', 'created_at', 'updated_at')
        }),
    )

    def cover_image_preview(self, obj):
        if obj.cover_image:
            return f'<img src="{obj.cover_image.url}" width="120" style="border-radius:8px;box-shadow:0 2px 8px #ccc;" />'
        return "-"
    cover_image_preview.allow_tags = True
    cover_image_preview.short_description = 'معاينة الصورة الرمزية'

    class Media:
        css = {'all': ('admin/css/widgets.css',)}

@admin.register(CampaignGallery)
class CampaignGalleryAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'image', 'alt_text', 'created_at')
    search_fields = ('campaign__title', 'alt_text')
    readonly_fields = ('created_at',)

# تعريب أسماء النماذج في لوحة التحكم
Campaign._meta.verbose_name = 'حملة تبرع'
Campaign._meta.verbose_name_plural = 'حملات التبرع'
CampaignGallery._meta.verbose_name = 'صورة إضافية للحملة'
CampaignGallery._meta.verbose_name_plural = 'معرض صور الحملات'
