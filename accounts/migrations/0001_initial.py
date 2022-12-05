# Generated by Django 4.1.3 on 2022-12-05 17:10

import accounts.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Committee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('Department', models.CharField(help_text='Enter your Deparment', max_length=20)),
                ('First_name', models.CharField(help_text='Enter your First name', max_length=20)),
                ('Last_name', models.CharField(help_text='Enter your Last name', max_length=20)),
                ('date_of_birth', models.DateField(help_text='Enter your Date of Birth')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(help_text='Enter Phone Number', max_length=128, region=None, unique=True)),
                ('email', models.EmailField(help_text='Enter your Email', max_length=255, unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Guide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(help_text='Enter your Designation', max_length=20)),
                ('department', models.CharField(help_text='Enter your deparment', max_length=20)),
                ('committee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Guide_Committee', to='Committee.committee')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Guide_User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'committee')},
            },
        ),
        migrations.CreateModel(
            name='Core',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SAPID', models.PositiveBigIntegerField()),
                ('department', models.CharField(help_text='Enter your deparment', max_length=20)),
                ('committee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Core_Committee', to='Committee.committee')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Core_Position', to='Committee.position', validators=[accounts.models.Core.positionValidator])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Core_User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'committee', 'position')},
            },
        ),
        migrations.CreateModel(
            name='CoCom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SAPID', models.PositiveBigIntegerField()),
                ('department', models.CharField(help_text='Enter your deparment', max_length=20)),
                ('committee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='CoCom_Committee', to='Committee.committee')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='CoCom_Position', to='Committee.position', validators=[accounts.models.CoCom.positionValidator])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='CoCom_User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'committee', 'position')},
            },
        ),
    ]
