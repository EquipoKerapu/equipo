# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-22 22:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20161121_0001'),
        ('students', '0016_auto_20161110_2232'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='studentcoursemapping',
            unique_together=set([('student', 'course')]),
        ),
    ]