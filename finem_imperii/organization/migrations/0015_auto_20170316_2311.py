# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-16 22:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0014_policydocument_last_modified_turn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='capability',
            name='type',
            field=models.CharField(choices=[('ban', 'ban'), ('policy', 'write policy and law'), ('conscript', 'conscript trops')], max_length=15),
        ),
    ]
