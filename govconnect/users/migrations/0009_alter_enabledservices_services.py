# Generated by Django 3.2.9 on 2021-11-15 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20211115_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enabledservices',
            name='services',
            field=models.JSONField(default={'Federal': {'Centrelink': False, 'Child Support': False, 'Medicare': False}}),
        ),
    ]