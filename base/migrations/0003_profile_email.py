# Generated by Django 5.1.4 on 2024-12-30 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_profile_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
