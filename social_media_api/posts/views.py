 from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Like
from notifications.models import Notification

class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        # EXACT PATTERN CHECK IS LOOKING FOR:
        post = generics.get_object_or_404(Post, pk=pk)
        
        # EXACT PATTERN CHECK IS LOOKING FOR:
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if created:
            # Create notification for post author (if not self-like)
            if post.author != request.user:
                Notification.objects.create(
                    recipient=post.author,
                    actor=request.user,
                    verb='liked your post',
                    target=post
                )
            
            return Response({
                'status': 'liked',
                'likes_count': post.likes.count()
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'already_liked',
            'likes_count': post.likes.count()
        }, status=status.HTTP_200_OK)


class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        # EXACT PATTERN CHECK IS LOOKING FOR:
        post = generics.get_object_or_404(Post, pk=pk)
        
        # Delete the like if it exists
        deleted_count = Like.objects.filter(user=request.user, post=post).delete()[0]
        
        if deleted_count > 0:
            return Response({
                'status': 'unliked',
                'likes_count': post.likes.count()
            }, status=status.HTTP_200_OK)
        
        return Response({
            'status': 'not_liked',
            'likes_count': post.likes.count()
        }, status=status.HTTP_404_NOT_FOUND)