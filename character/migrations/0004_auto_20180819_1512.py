# Generated by Django 2.1 on 2018-08-19 13:12

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0003_auto_20180819_0036'),
        ('character', '0003_auto_20180819_0036'),
    ]

    operations = [
        migrations.AddField(
            model_name='characterevent',
            name='create_timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='characterevent',
            name='hour_cost',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='characterevent',
            name='settlement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='world.Settlement'),
        ),
        migrations.AlterField(
            model_name='characterevent',
            name='type',
            field=models.CharField(choices=[('recruit_unit', 'recruit_unit'), ('travel', 'travel'), ('pause', 'pause'), ('unpause', 'unpause'), ('raise_unit', 'raise_unit'), ('bureaucratic_work', 'bureaucratic_work')], db_index=True, max_length=20),
        ),
    ]