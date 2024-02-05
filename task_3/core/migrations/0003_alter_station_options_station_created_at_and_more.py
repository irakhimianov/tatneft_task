# Generated by Django 4.2.9 on 2024-02-05 11:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_station_coordinates_alter_station_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='station',
            options={'ordering': ('-created_at',), 'verbose_name': 'заправочная станция', 'verbose_name_plural': 'заправочные станции'},
        ),
        migrations.AddField(
            model_name='station',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='когда создан'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='station',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='когда обновлен'),
        ),
        migrations.AlterField(
            model_name='fuelstation',
            name='currency',
            field=models.CharField(blank=True, db_index=True, max_length=255, verbose_name='валюта'),
        ),
    ]