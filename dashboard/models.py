from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone


from django.contrib.auth import get_user_model
from django.conf import settings
import secrets

class Comment(models.Model):
    email = models.EmailField(max_length=59)
    title = models.CharField(max_length=20)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = ("email")
    REQUIRED_FIELDS = ["username"]
    
    def __str__(self):
        return self.email
    

class OtpToken(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="otps")
    otp_code = models.CharField(max_length=6, default=secrets.token_hex(3))
    otp_created_at = models.DateTimeField(auto_now_add=True)
    otp_expires_at = models.DateTimeField(blank=True, null=True)
    
    # def __str__(self):
    #     return self.user.username

    