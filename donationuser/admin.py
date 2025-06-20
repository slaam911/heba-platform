from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, SiteSettings, VerificationCode

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number', 'get_full_name', 'region', 'city', 'is_verified')
    search_fields = ('username', 'email', 'phone_number', 'first_name', 'last_name')
    ordering = ('-date_joined',)

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('verification_required', 'verify_email', 'verify_phone')

@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at', 'expires_at', 'is_used', 'verification_method')
    list_filter = ('is_used', 'verification_method')
    search_fields = ('user__username', 'user__email', 'code')
    ordering = ('-created_at',)
