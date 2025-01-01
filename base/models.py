from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.timezone import now

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'


class Registration(models.Model):
    # Personal Information
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="registrations")
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
    payment_status = models.BooleanField(default=False)  # Payment status for this specific course
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=250.00)  # Default course fee

    status = models.CharField(
        max_length=50,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )

    # Programme of Interest
    PROGRAM_CHOICES = [
        ('Mining Level 3', 'Occupational Standards for Mining and Quarrying Technology National Certificate I (Level 3)'),
        ('Mines Engineering Level 4', 'Occupational Standards for Mines Systems Engineering National Certificate 2 (Level 4)'),
        ('Mines Engineering Diploma Level 5', 'Occupational Standards for Higher National Diploma in Mines Systems Engineering (Level 5)'),
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
    
    date_submitted = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.program_title}"


class Transaction(models.Model):
    TRANSACTION_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('Paystack', 'Paystack'),
        ('Mobile Money', 'Mobile Money'),
        ('Bank Transfer', 'Bank Transfer'),
    ]

    transaction_id = models.CharField(max_length=50, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS_CHOICES, default='Pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='Paystack')
    reference = models.CharField(max_length=50, blank=True, null=True)  # Reference from Paystack or payment gateway
    date_created = models.DateTimeField(auto_now_add=True)
    date_settled = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.registration.program_title} - {self.user.username}"
