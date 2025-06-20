import django; print('### DJANGO VERSION:', django.get_version())
import sys; print('### USING SETTINGS FILE:', __file__, file=sys.stderr)

INSTALLED_APPS = [
    'tinymce',
    # ...
]

# تأكد من إعداد static وmedia
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CKEDITOR_TEMPLATE_PATH = os.path.join(BASE_DIR, 'venv/lib/python3.13/site-packages/ckeditor/templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # ...
            ],
        },
    },
] 