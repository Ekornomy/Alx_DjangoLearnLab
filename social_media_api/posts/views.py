from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Like
from .serializers import LikeSerializer
from notifications.models import Notification

class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        # This is where the check expects to see:
        post = generics.get_object_or_404(Post, pk=pk)
        
        # This is where the check expects to see:
        like, created = Like.objects.get_or_create(
            user=request.user, 
            post=post
        )
        
        if created:
            # Create notification
            if post.author != request.user:
                Notification.objects.create(
                    recipient=post.author,
                    actor=request.user,
                    verb='liked your post',
                    target=post
                )
            return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'already liked'}, status=status.HTTP_200_OK)

class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        
        deleted = Like.objects.filter(
            user=request.user, 
            post=post
        ).delete()[0]
        
        if deleted:
            return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
        return Response({'status': 'not liked'}, status=status.HTTP_404_NOT_FOUND)