# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-27 23:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0010_auto_20161027_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteuser',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]