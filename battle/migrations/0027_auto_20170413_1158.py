# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-13 09:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0026_auto_20170410_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='what',
            field=models.CharField(choices=[('stand', 'stand'), ('flee', 'flee'), ('charge', 'charge'), ('formation', 'formation'), ('ranged', 'ranged')], max_length=15),
        ),
    ]
