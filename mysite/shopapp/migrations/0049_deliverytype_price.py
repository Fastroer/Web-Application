# Generated by Django 4.2.1 on 2023-06-29 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0048_deliverytype_paymenttype'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliverytype',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]
