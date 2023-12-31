# Generated by Django 4.2.1 on 2023-06-26 19:56

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0034_rename_rate_product_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=2, default=Decimal('0'), max_digits=3, null=True),
        ),
    ]
