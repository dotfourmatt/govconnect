# Generated by Django 3.2.9 on 2021-11-04 03:01

import django.contrib.postgres.fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_long', models.CharField(max_length=150)),
                ('name_short', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('url', models.URLField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='GovConnectUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email Address')),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Phone Number')),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('other_names', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=150), blank=True, null=True, size=None)),
                ('date_of_birth', models.DateField()),
                ('address', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=150), size=None)),
                ('primary_identification', models.CharField(choices=[('DL', 'Driver License'), ('ML', 'Marine License'), ('PP', 'Passport'), ('BC', 'Birth Certificate'), ('POA', 'Proof of Age Card'), ('PIC', 'Photo Identification Card')], default='DL', max_length=3)),
                ('primary_identification_number', models.CharField(max_length=50, unique=True)),
                ('other_identities', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), size=2), blank=True, null=True, size=None)),
                ('connected_services', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[], max_length=5), blank=True, null=True, size=None)),
                ('services_that_have_your_data', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=150), size=None), blank=True, null=True, size=None)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=False)),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_login_ip', models.GenericIPAddressField(blank=True, null=True)),
                ('secret_question', models.CharField(max_length=150)),
                ('secret_question_answer', models.CharField(max_length=150)),
                ('sms_one_time_password', models.BooleanField(default=False)),
                ('email_one_time_password', models.BooleanField(default=False)),
                ('passwordless_login', models.BooleanField(default=False)),
                ('physical_security_authentication', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
