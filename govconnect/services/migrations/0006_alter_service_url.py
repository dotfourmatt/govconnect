# Generated by Django 3.2.9 on 2021-11-15 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_alter_service_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='url',
            field=models.URLField(max_length=400),
        ),
    ]
