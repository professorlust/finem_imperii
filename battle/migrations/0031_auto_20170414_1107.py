# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-14 09:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0030_auto_20170414_0911'),
    ]

    operations = [
        migrations.AddField(
            model_name='battlecontuberniuminturn',
            name='desired_x_pos',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='battlecontuberniuminturn',
            name='desired_z_pos',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='battlecontuberniuminturn',
            name='desires_pos',
            field=models.BooleanField(default=False),
        ),
    ]
