# Generated by Django 5.0.6 on 2024-06-18 02:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0002_remove_pedido_productos_pedido_fecha_actualizacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detallepedido',
            name='precio_unitario',
        ),
    ]
