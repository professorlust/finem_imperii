# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-15 18:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0008_auto_20171015_2013'),
    ]

    operations = [
        migrations.AddField(
            model_name='battleunitinturn',
            name='ammo_remaining',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]