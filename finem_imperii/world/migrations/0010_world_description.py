# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-02 16:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0009_auto_20170302_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='world',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
