# Generated by Django 4.2.1 on 2023-06-11 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0026_remove_productcharacteristic_value_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcharacteristic',
            name='value',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.DeleteModel(
            name='ProductCharacteristicValue',
        ),
    ]
