# Generated by Django 5.2.3 on 2025-06-17 10:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_banner'),
    ]

    operations = [
        migrations.CreateModel(
            name='BannerButton',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50, verbose_name='نص الزر')),
                ('url', models.URLField(blank=True, max_length=300, verbose_name='رابط الزر')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='ترتيب الزر')),
                ('banner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buttons', to='core.banner', verbose_name='البنر')),
            ],
            options={
                'verbose_name': 'زر البنر',
                'verbose_name_plural': 'أزرار البنر',
                'ordering': ['order', 'id'],
            },
        ),
    ]
