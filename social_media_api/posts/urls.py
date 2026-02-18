from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    # ... other URLs
    path('post/<int:pk>/like/', views.LikePostView.as_view(), name='like_post'),
    path('post/<int:pk>/unlike/', views.UnlikePostView.as_view(), name='unlike_post'),
]