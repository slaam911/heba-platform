from django.contrib import admin
from .models import BloodRequest

@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = (
        'patient_name', 'hospital_name', 'city', 'blood_type', 'units_needed',
        'status', 'created_at', 'is_critical'
    )
    list_filter = ('status', 'city', 'blood_type', 'is_critical', 'created_at')
    search_fields = ('patient_name', 'hospital_name', 'medical_file_number', 'contact_number')
    readonly_fields = ('created_at', 'updated_at', 'request_id')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('patient_name', 'medical_file_number', 'hospital_name', 'city', 'blood_type', 'blood_component', 'patient_age', 'patient_gender', 'units_needed', 'is_critical', 'contact_number', 'additional_info', 'status', 'rejection_reason', 'expires_at', 'request_id', 'created_at', 'updated_at')
        }),
    ) 