# Generated by Django 4.2.1 on 2023-06-09 18:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0017_product_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='rating',
        ),
    ]
