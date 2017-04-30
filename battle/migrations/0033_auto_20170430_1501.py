# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-30 13:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0032_battlecontuberniuminturn_moved_this_turn'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='battlecontuberniuminturn',
            unique_together=set([('battle_turn', 'x_pos', 'z_pos')]),
        ),
        migrations.AlterIndexTogether(
            name='battlecontuberniuminturn',
            index_together=set([]),
        ),
    ]