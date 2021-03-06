# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-19 12:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('world', '0001_initial'),
        ('character', '0001_initial'),
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='world.Settlement'),
        ),
        migrations.AddField(
            model_name='character',
            name='oath_sworn_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.Organization'),
        ),
        migrations.AddField(
            model_name='character',
            name='owner_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='character',
            name='travel_destination',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='travellers_heading', to='world.Settlement'),
        ),
        migrations.AddField(
            model_name='character',
            name='world',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='world.World'),
        ),
    ]
