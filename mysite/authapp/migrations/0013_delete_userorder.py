# Generated by Django 4.2.1 on 2023-07-02 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0012_delete_card'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserOrder',
        ),
    ]