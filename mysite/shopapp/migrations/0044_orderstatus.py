# Generated by Django 4.2.1 on 2023-06-29 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0043_remove_order_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]
