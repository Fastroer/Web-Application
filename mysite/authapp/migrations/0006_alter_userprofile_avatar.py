# Generated by Django 4.2.1 on 2023-06-03 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0005_rename_full_name_userprofile_fullname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='media/avatars/'),
        ),
    ]
