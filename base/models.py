from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

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