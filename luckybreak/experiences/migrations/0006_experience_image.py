# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-11 20:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiences', '0005_auto_20170911_2022'),
    ]

    operations = [
        migrations.AddField(
            model_name='experience',
            name='image',
            field=models.ImageField(default='a', upload_to='experiences/'),
            preserve_default=False,
        ),
    ]
