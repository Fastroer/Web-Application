# Generated by Django 4.2.1 on 2023-06-30 08:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0009_cart_cartitem'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserOrder',
        ),
    ]
