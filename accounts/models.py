from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Token(models.Model):
    token = models.CharField(max_length=10, default="uilcpe2024")

    def __str__(self):
        return f"Permanent token"

class Moderator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=10, blank=False)
    created_at = models.DateTimeField(blank=False)

    def __str__(self):
        return self.user.username
    
class Visitor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(blank=False)
    is_authorized = models.BooleanField(blank=False)

    def __str__(self):
        return self.user.username
