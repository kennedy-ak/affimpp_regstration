# Generated by Django 5.1.4 on 2024-12-30 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_registration_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=50),
        ),
    ]
