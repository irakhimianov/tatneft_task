# Generated by Django 4.2.9 on 2024-02-05 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='coordinates',
            field=models.CharField(blank=True, max_length=255, verbose_name='координаты'),
        ),
        migrations.AlterField(
            model_name='station',
            name='number',
            field=models.CharField(blank=True, db_index=True, max_length=255, verbose_name='номер'),
        ),
    ]
