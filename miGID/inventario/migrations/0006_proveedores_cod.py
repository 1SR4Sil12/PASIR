# Generated by Django 4.2.6 on 2023-11-21 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0005_proveedores'),
    ]

    operations = [
        migrations.AddField(
            model_name='proveedores',
            name='cod',
            field=models.IntegerField(default=0, verbose_name='Código'),
        ),
    ]
