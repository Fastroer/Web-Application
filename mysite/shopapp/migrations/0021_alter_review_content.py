# Generated by Django 4.2.1 on 2023-06-10 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0020_alter_product_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='content',
            field=models.TextField(blank=True),
        ),
    ]
