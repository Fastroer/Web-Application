# Generated by Django 4.2.1 on 2023-06-26 20:14

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0037_remove_product_rating_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rating_count',
            field=models.DecimalField(blank=True, decimal_places=2, default=Decimal('0'), max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='reviews_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
