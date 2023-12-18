from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):

    middle_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username




class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    # Add other profile fields if needed

    def __str__(self):
        return f'{self.user.username} Profile'


