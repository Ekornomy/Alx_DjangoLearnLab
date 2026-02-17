from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Like
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer, LikeSerializer
from notifications.models import Notification


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the author
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Post CRUD operations
    """
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'content']
    filterset_fields = ['author']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PostDetailSerializer
        return PostSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """Get all comments for a specific post"""
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        """Like a post"""
        post = self.get_object()
        
        # Check if already liked
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if created:
            # Create notification for post author
            if post.author != request.user:  # Don't notify if liking own post
                Notification.objects.create(
                    recipient=post.author,
                    actor=request.user,
                    verb='like',
                    content_type=ContentType.objects.get_for_model(post),
                    object_id=post.id
                )
            
            return Response({
                "message": "Post liked successfully",
                "likes_count": post.likes.count()
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "message": "Post already liked"
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        """Unlike a post"""
        post = self.get_object()
        
        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return Response({
                "message": "Post unliked successfully",
                "likes_count": post.likes.count()
            }, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({
                "message": "You haven't liked this post"
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def likes(self, request, pk=None):
        """Get all users who liked this post"""
        post = self.get_object()
        likes = post.likes.all()
        serializer = LikeSerializer(likes, many=True, context={'request': request})
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Comment CRUD operations
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['content']
    
    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        
        # Create notification for post author
        if comment.post.author != self.request.user:
            Notification.objects.create(
                recipient=comment.post.author,
                actor=self.request.user,
                verb='comment',
                content_type=ContentType.objects.get_for_model(comment.post),
                object_id=comment.post.id
            )
    
    def get_queryset(self):
        """
        Optionally filter comments by post
        """
        queryset = Comment.objects.all()
        post_id = self.request.query_params.get('post', None)
        if post_id is not None:
            queryset = queryset.filter(post_id=post_id)
        return queryset


class FeedView(generics.ListAPIView):
    """
    View to get feed of posts from users that the current user follows.
    Returns posts ordered by creation date, showing the most recent posts at the top.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def get_queryset(self):
        user = self.request.user
        # Get users that the current user follows
        following_users = user.following.all()
        # Filter posts by authors in following_users and order by creation date (most recent first)
        return Post.objects.filter(author__in=following_users).order_by('-created_at')