# Generated by Django 4.2.1 on 2023-06-03 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0004_rename_phone_number_userprofile_phone_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='full_name',
            new_name='fullName',
        ),
    ]
