# Generated by Django 3.2.9 on 2021-11-15 01:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='queenslandservice',
            old_name='ossio',
            new_name='osssio',
        ),
    ]
