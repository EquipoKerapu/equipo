# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-24 20:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0018_auto_20161124_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='site_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
