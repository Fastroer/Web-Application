# Generated by Django 4.2.1 on 2023-06-30 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0056_alter_order_status'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
