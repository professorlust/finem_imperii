# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-30 12:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0004_battlecharacter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='battleunit',
            name='battle',
        ),
        migrations.AddField(
            model_name='battleunit',
            name='owner',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='battle.BattleCharacter'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='battlecharacter',
            unique_together=set([('battle', 'character')]),
        ),
    ]
