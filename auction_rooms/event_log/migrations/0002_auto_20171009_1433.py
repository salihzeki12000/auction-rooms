# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-09 14:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_log', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventlog',
            name='type',
            field=models.IntegerField(choices=[(1, 'A new experience was created'), (2, 'A new auction was created'), (3, 'A bid was placed on an auction'), (4, 'Auction finished')]),
        ),
    ]
