release: python manage.py migrate && python manage.py collectstatic --noinput && python manage.py create_default_superuser
web: gunicorn core.wsgi --log-file - 