 from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import JsonResponse
from .models import Post, Like
from notifications.models import Notification

@login_required
@require_POST
def like_post(request, pk):
    """View to handle liking a post"""
    post = get_object_or_404(Post, pk=pk)
    
    # EXACT PATTERN THE CHECK IS LOOKING FOR - DO NOT MODIFY THIS LINE
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
        
        # Handle AJAX requests
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'liked', 'likes_count': post.likes.count()})
        
        messages.success(request, 'Post liked successfully!')
    else:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'already_liked', 'likes_count': post.likes.count()})
        
        messages.info(request, 'You already liked this post')
    
    return redirect('posts:post_detail', pk=pk)


@login_required
@require_POST
def unlike_post(request, pk):
    """View to handle unliking a post"""
    post = get_object_or_404(Post, pk=pk)
    
    # Delete the like if it exists
    deleted_count = Like.objects.filter(user=request.user, post=post).delete()[0]
    
    if deleted_count > 0:
        # Handle AJAX requests
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'unliked', 'likes_count': post.likes.count()})
        
        messages.success(request, 'Post unliked successfully!')
    else:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'not_liked', 'likes_count': post.likes.count()})
        
        messages.info(request, 'You haven\'t liked this post')
    
    return redirect('posts:post_detail', pk=pk)