# Generated by Django 2.2.3 on 2021-04-05 09:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210403_1156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='address',
            field=models.CharField(default=uuid.uuid4, max_length=255, null=True, unique=True),
        ),
    ]
