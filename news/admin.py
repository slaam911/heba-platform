from django.contrib import admin
from django import forms
from .models import NewsSection, NewsArticle, NewsAttachment

class NewsAttachmentInline(admin.StackedInline):
    model = NewsAttachment
    extra = 1  # مربع واحد فقط افتراضيًا
    max_num = 20
    verbose_name = 'صورة مرفقة'
    verbose_name_plural = 'الصور المرفقة'
    
    class Media:
        js = ('admin/js/news_attachment_limit.js',)

@admin.register(NewsSection)
class NewsSectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'priority', 'target_audience', 'related_campaign', 'created_at')
    list_filter = ('status', 'priority')
    search_fields = ('name', 'description', 'target_audience')
    ordering = ('-priority', 'name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'status', 'publish_time', 'created_at')
    list_filter = ('status', 'section', 'publish_time')
    search_fields = ('title', 'subtitle', 'summary', 'content')
    ordering = ('-publish_time', '-created_at')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'publish_time'
    fieldsets = (
        (None, {
            'fields': ('title', 'subtitle', 'section', 'summary', 'content', 'main_image', 'status', 'publish_time', 'created_at', 'updated_at')
        }),
    )
    inlines = [NewsAttachmentInline]
    formfield_overrides = {
        NewsArticle._meta.get_field('content'): {'widget': forms.Textarea(attrs={'rows': 10, 'class': 'vLargeTextField', 'style': 'direction: rtl;'})},
    }

@admin.register(NewsAttachment)
class NewsAttachmentAdmin(admin.ModelAdmin):
    list_display = ('article', 'image', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('article__title',)
    readonly_fields = ('uploaded_at',)
