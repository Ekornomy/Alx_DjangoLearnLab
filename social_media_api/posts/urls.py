from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    # ... other URLs
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('post/<int:pk>/unlike/', views.unlike_post, name='unlike_post'),
]