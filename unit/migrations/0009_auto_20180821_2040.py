# Generated by Django 2.1 on 2018-08-21 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unit', '0008_auto_20180821_1916'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='worldunit',
            name='origin',
        ),
        migrations.AlterField(
            model_name='worldunit',
            name='type',
            field=models.CharField(choices=[('light infantry soldiers', 'light infantry soldiers'), ('pikemen', 'pikemen'), ('archers', 'archers'), ('cavalry', 'cavalry'), ('catapult', 'catapult'), ('siege tower', 'siege tower'), ('ram', 'ram')], max_length=30),
        ),
    ]
