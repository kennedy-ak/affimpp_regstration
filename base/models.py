from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.timezone import now

User = get_user_model()
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    firstname = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=100,null=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'
    



class Registration(models.Model):
    # Personal Information
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="registrations",)
    PREFIX_CHOICES = [
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Ms', 'Ms'),
        ('Dr', 'Dr'),
        ('Prof', 'Prof'),
        ('Engr', 'Engr'),
    ]
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    prefix = models.CharField(max_length=5, choices=PREFIX_CHOICES)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    nationality = models.CharField(max_length=100)
    address = models.TextField()
    address2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    status = models.CharField(
        max_length=50,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )
    # Programme of Interest
    PROGRAM_CHOICES = [
        ('Mining Level 3', 'Occupational Standards for Mining and Quarrying Technology National Certificate I (Level 3)'),
        ('Mines Engineering Level 4', 'Occupational Standards for Mines Systems Engineering National Certificate 2 (Level 4)'),
        ('Mines Engineering Diploma Level 5', 'OCCUPATIONAL STANDARDS FOR HIGHER NATIONAL DIPLOMA IN MINES SYSTEMS ENGINEERING (Level 5)'),
    ]
    program_title = models.CharField(max_length=255, choices=PROGRAM_CHOICES)
  

    # Educational Background
    education_level = models.CharField(max_length=100)
    qualifications = models.TextField()
    institutions_attended = models.TextField()

    # Work Experience
    current_occupation = models.CharField(max_length=100, blank=True)
    years_experience = models.IntegerField(default=0)
    relevant_skills = models.TextField(blank=True)

    # Files
    photo = models.ImageField(upload_to='photos/')
    birth_certificate = models.FileField(upload_to='documents/')
    education_certificates = models.FileField(upload_to='documents/')
    proof_of_payment = models.FileField(upload_to='documents/')
    date_submitted = models.DateTimeField(default=now)    # Automatically se

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.program_title}"
