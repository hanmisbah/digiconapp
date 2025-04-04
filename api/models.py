from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
import os
from datetime import date

# Custom User Model
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.username


# Function to generate the image upload path dynamically
def upload_to(instance, filename):
    return os.path.join('container_images', str(instance.container.container_number), str(date.today()), filename)


# Container Model - Represents each unique container
class Container(models.Model):
    container_number = models.CharField(max_length=100, unique=True)  # Unique identifier
    created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Track uploader

    def __str__(self):
        return self.container_number


# Image Model - Stores images linked to a container
class Image(models.Model):
    container = models.ForeignKey(Container, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="container_images/%Y/%m/%d/")  
    uploaded_at = models.DateTimeField(auto_now_add=True)  # ✅ Correct field
  # Auto timestamp

    def __str__(self):
        return f"Image {self.id} for Container {self.container.container_number}"
