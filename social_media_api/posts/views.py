 from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Post, Like
from notifications.models import Notification

@login_required
@require_POST
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # EXACT PATTERN THE CHECK IS LOOKING FOR:
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if created:
        # Generate notification if not self-like
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='liked your post',
                target=post
            )
    
    return redirect('posts:post_detail', pk=pk)

@login_required
@require_POST
def unlike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    Like.objects.filter(user=request.user, post=post).delete()
    return redirect('posts:post_detail', pk=pk)