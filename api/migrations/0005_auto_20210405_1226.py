# Generated by Django 2.2.3 on 2021-04-05 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20210405_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='address',
            field=models.CharField(default='0A159A', max_length=255, null=True, unique=True),
        ),
    ]