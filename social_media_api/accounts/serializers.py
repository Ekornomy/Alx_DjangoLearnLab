from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    following_count = serializers.IntegerField(source='following.count', read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 
                  'bio', 'profile_picture', 'followers_count', 'following_count')
        read_only_fields = ('id',)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name', 'bio')
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords don't match"})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(style={'input_type': 'password'})
    
    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not (username or email):
            raise serializers.ValidationError("Username or email is required")
        
        if username:
            user = authenticate(username=username, password=password)
        else:
            try:
                user_obj = CustomUser.objects.get(email=email)
                user = authenticate(username=user_obj.username, password=password)
            except CustomUser.DoesNotExist:
                user = None
        
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        
        data['user'] = user
        return data