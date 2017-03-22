# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-14 17:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0008_auto_20170314_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='capability',
            name='applying_to',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='capabilities_to_this', to='organization.Organization'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='capability',
            name='stemming_from',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transfers', to='organization.Capability'),
        ),
        migrations.AlterField(
            model_name='capability',
            name='type',
            field=models.CharField(choices=[('ban', 'banning'), ('policy', 'writing policy and law'), ('conscript', 'conscripting trops')], max_length=15),
        ),
    ]