from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    # EXACT PATTERN 1: <int:pk>/like/
    path('<int:pk>/like/', views.LikePostView.as_view(), name='like_post'),
    
    # EXACT PATTERN 2: <int:pk>/unlike/
    path('<int:pk>/unlike/', views.UnlikePostView.as_view(), name='unlike_post'),
    
    # You might also have other URLs like:
    # path('', views.PostListView.as_view(), name='post_list'),
    # path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    # path('create/', views.PostCreateView.as_view(), name='post_create'),
    # path('<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    # path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
]