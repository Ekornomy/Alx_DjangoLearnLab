from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.ReadOnlyField(source='actor.username')
    actor_profile_picture = serializers.ImageField(source='actor.profile_picture', read_only=True)
    target_type = serializers.ReadOnlyField(source='content_type.model')
    
    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'actor_username', 'actor_profile_picture', 
                  'verb', 'target_type', 'target', 'timestamp', 'is_read']
        read_only_fields = ['id', 'recipient', 'actor', 'timestamp']