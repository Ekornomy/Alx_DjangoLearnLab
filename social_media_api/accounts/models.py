from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )
    
    def __str__(self):
        return self.username
    
    def follow(self, user):
        """Follow another user"""
        self.following.add(user)
    
    def unfollow(self, user):
        """Unfollow another user"""
        self.following.remove(user)
    
    def is_following(self, user):
        """Check if following another user"""
        return self.following.filter(pk=user.pk).exists()
    
    def get_followers_count(self):
        """Get number of followers"""
        return self.followers.count()
    
    def get_following_count(self):
        """Get number of following"""
        return self.following.count()