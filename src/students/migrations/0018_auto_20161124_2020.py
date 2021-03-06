# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-24 20:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0017_auto_20161122_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professorcoursemapping',
            name='course',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='professor_mapping', to='courses.Course'),
        ),
        migrations.AlterField(
            model_name='studentcoursemapping',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_mapping', to='courses.Course'),
        ),
    ]
