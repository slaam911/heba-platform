from django.contrib import admin
from .models import BloodBankUser

@admin.register(BloodBankUser)
class BloodBankUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'bloodbank_name', 'manager_name', 'is_approved', 'created_at')
    search_fields = ('username', 'email', 'bloodbank_name', 'manager_name')
    list_filter = ('is_approved', 'region', 'city')
    readonly_fields = ('created_at', 'updated_at')
