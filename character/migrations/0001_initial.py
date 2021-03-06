# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-19 12:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('cash', models.IntegerField(default=0)),
                ('hours_in_turn_left', models.IntegerField(default=360)),
                ('profile', models.CharField(choices=[('commander', 'commander'), ('trader', 'trader'), ('bureaucrat', 'bureaucrat')], max_length=20)),
                ('last_activation_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('paused', models.BooleanField(default=False)),
            ],
        ),
    ]
