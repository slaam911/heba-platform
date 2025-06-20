from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import BloodBankProfile, City

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'is_active')
    list_filter = ('region', 'is_active')
    search_fields = ('name', 'region')
    ordering = ('region', 'name')
    list_editable = ('is_active',)
    fieldsets = (
        ('معلومات المدينة', {
            'fields': ('name', 'region', 'is_active')
        }),
    )

@admin.register(BloodBankProfile)
class BloodBankProfileAdmin(admin.ModelAdmin):
    list_display = ('bloodbank_name', 'region', 'city', 'manager_name', 'is_approved', 'created_at')
    list_filter = ('region', 'is_approved')
    search_fields = ('bloodbank_name', 'manager_name', 'manager_email', 'city__name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('معلومات بنك الدم', {
            'fields': ('bloodbank_name', 'hospital_name', 'region', 'city', 'contact_number', 'address', 'map_location', 'working_hours', 'special_instructions')
        }),
        ('معلومات المسؤول', {
            'fields': ('manager_name', 'manager_phone', 'manager_email', 'manager_position')
        }),
        ('إدارة', {
            'fields': ('is_approved', 'created_at', 'updated_at')
        }),
    )
