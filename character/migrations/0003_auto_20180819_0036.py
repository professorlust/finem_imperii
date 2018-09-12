# Generated by Django 2.1 on 2018-08-18 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('unit', '0005_auto_20180819_0036'),
        ('character', '0002_auto_20171119_1349'),
    ]

    operations = [
        migrations.CreateModel(
            name='CharacterEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField()),
                ('type', models.CharField(choices=[('recruit_unit', 'recruit_unit'), ('travel', 'travel'), ('pause', 'pause'), ('unpause', 'unpause'), ('raise_unit', 'raise_unit')], db_index=True, max_length=20)),
                ('counter', models.IntegerField(blank=True, help_text='Counter for general use', null=True)),
                ('start_turn', models.IntegerField()),
                ('end_turn', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='character',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='world.Settlement'),
        ),
        migrations.AlterField(
            model_name='character',
            name='oath_sworn_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='organization.Organization'),
        ),
        migrations.AlterField(
            model_name='character',
            name='travel_destination',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='travellers_heading', to='world.Settlement'),
        ),
        migrations.AlterField(
            model_name='character',
            name='world',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='world.World'),
        ),
        migrations.AddField(
            model_name='characterevent',
            name='character',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='character.Character'),
        ),
        migrations.AddField(
            model_name='characterevent',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='unit.WorldUnit'),
        ),
    ]