# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 21:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0007_charactermessage_safe'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagereceiver',
            name='favourite',
            field=models.BooleanField(default=False),
        ),
    ]