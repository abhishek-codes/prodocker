# Generated by Django 3.2.9 on 2021-11-07 09:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=20, unique=True, validators=[django.core.validators.RegexValidator('^\\+[1-9]{1}[0-9]{7,16}$', message="Phone number must be entered in the         format: '+999999999'. Up to 15 digits allowed.")]),
        ),
    ]