# Generated by Django 2.1 on 2018-08-18 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0004_auto_20171201_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battlecharacter',
            name='character',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='character.Character'),
        ),
        migrations.AlterField(
            model_name='battleorganization',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='organization.Organization'),
        ),
        migrations.AlterField(
            model_name='battlesoldier',
            name='world_npc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='world.NPC'),
        ),
        migrations.AlterField(
            model_name='battleunit',
            name='world_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='unit.WorldUnit'),
        ),
    ]