# Generated by Django 2.2.3 on 2021-04-03 08:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='address',
            field=models.CharField(default='G1TfF', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='amount',
            field=models.DecimalField(decimal_places=6, default=1, max_digits=11, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
