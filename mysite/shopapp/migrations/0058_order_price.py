# Generated by Django 4.2.1 on 2023-06-30 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0057_delete_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]
