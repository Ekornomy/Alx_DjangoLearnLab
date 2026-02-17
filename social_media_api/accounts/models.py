from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    followers = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        related_name='following',
        blank=True
    )
    
    def __str__(self):
        return self.username
    
    def followers_count(self):
        return self.followers.count()
    
    def following_count(self):
        return self.following.count()