# Generated by Django 2.1 on 2018-08-18 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('unit', '0004_auto_20171202_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worldunit',
            name='default_battle_orders',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='battle.Order'),
        ),
        migrations.AlterField(
            model_name='worldunit',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='world.Settlement'),
        ),
        migrations.AlterField(
            model_name='worldunit',
            name='origin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='units_originating', to='world.Settlement'),
        ),
        migrations.AlterField(
            model_name='worldunit',
            name='owner_character',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='character.Character'),
        ),
        migrations.AlterField(
            model_name='worldunit',
            name='recruitment_type',
            field=models.CharField(choices=[('conscription', 'conscription'), ('professional', 'professional'), ('mercenary', 'mercenary'), ('raised', 'raised')], max_length=30),
        ),
        migrations.AlterField(
            model_name='worldunit',
            name='world',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='world.World'),
        ),
    ]
