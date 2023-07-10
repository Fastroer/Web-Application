# Generated by Django 4.2.1 on 2023-06-09 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0014_alter_review_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.DecimalField(choices=[(0.0, '0.0'), (0.5, '0.5'), (1.0, '1.0'), (1.5, '1.5'), (2.0, '2.0'), (2.5, '2.5'), (3.0, '3.0'), (3.5, '3.5'), (4.0, '4.0'), (4.5, '4.5'), (5.0, '5.0'), (5.5, '5.5'), (6.0, '6.0'), (6.5, '6.5'), (7.0, '7.0'), (7.5, '7.5'), (8.0, '8.0'), (8.5, '8.5'), (9.0, '9.0'), (9.5, '9.5'), (10.0, '10.0')], decimal_places=1, default=0, max_digits=3),
        ),
    ]