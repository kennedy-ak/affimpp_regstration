# Generated by Django 5.1.4 on 2024-12-30 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_program_registration2_delete_registration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefix', models.CharField(choices=[('Mr', 'Mr'), ('Mrs', 'Mrs'), ('Ms', 'Ms'), ('Dr', 'Dr'), ('Prof', 'Prof'), ('Engr', 'Engr')], max_length=5)),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('dob', models.DateField()),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=6)),
                ('nationality', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('address2', models.CharField(blank=True, max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('program_title', models.CharField(choices=[('Mining Level 3', 'Occupational Standards for Mining and Quarrying Technology National Certificate I (Level 3)'), ('Mines Engineering Level 4', 'Occupational Standards for Mines Systems Engineering National Certificate 2 (Level 4)'), ('Mines Engineering Diploma Level 5', 'OCCUPATIONAL STANDARDS FOR HIGHER NATIONAL DIPLOMA IN MINES SYSTEMS ENGINEERING (Level 5)')], max_length=255)),
                ('duration', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('education_level', models.CharField(max_length=100)),
                ('qualifications', models.TextField()),
                ('institutions_attended', models.TextField()),
                ('current_occupation', models.CharField(blank=True, max_length=100)),
                ('years_experience', models.IntegerField(default=0)),
                ('relevant_skills', models.TextField(blank=True)),
                ('photo', models.ImageField(upload_to='photos/')),
                ('birth_certificate', models.FileField(upload_to='documents/')),
                ('education_certificates', models.FileField(upload_to='documents/')),
                ('proof_of_payment', models.FileField(upload_to='documents/')),
            ],
        ),
        migrations.RemoveField(
            model_name='registration2',
            name='program',
        ),
        migrations.RemoveField(
            model_name='registration2',
            name='user',
        ),
        migrations.DeleteModel(
            name='Program',
        ),
        migrations.DeleteModel(
            name='Registration2',
        ),
    ]
