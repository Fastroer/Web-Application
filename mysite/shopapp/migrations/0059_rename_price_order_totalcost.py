# Generated by Django 4.2.1 on 2023-06-30 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0058_order_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='price',
            new_name='totalCost',
        ),
    ]