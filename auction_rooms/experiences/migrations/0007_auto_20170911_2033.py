# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-11 20:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experiences', '0006_experience_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='experience',
            old_name='image',
            new_name='banner_image',
        ),
    ]
