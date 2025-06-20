import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from donationuser.models import CustomUser

# إنشاء المستخدم الفائق الصلاحيات
CustomUser.objects.create_superuser(
    username='slaam911',
    email='slaam911@gmail.com',
    password='0567003775@@',
    user_type='admin',
    phone_number='0567003775',
    city='الرياض'
) 