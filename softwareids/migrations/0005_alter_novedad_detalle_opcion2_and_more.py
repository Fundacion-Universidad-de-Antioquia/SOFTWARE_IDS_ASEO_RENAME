# Generated by Django 5.0.4 on 2024-05-15 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('softwareids', '0004_novedad_detalle_opcion1_novedad_detalle_opcion2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='novedad',
            name='detalle_opcion2',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='novedad',
            name='detalle_opcion3',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
