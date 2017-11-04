# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-15 19:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0009_battleunitinturn_ammo_remaining'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='what',
            field=models.CharField(choices=[('stand', 'stand'), ('move', 'move'), ('flee', 'flee'), ('charge', 'charge'), ('formation', 'formation'), ('ranged and charge', 'ranged attack, then charge'), ('ranged and flee', 'ranged attack, then flee'), ('ranged and stand', 'ranged attack, then stand'), ('stand and keep distance', 'stand and keep distance')], max_length=15),
        ),
    ]