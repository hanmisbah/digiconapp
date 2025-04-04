from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Container, Image



User = get_user_model()

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)  # Properly hash passwords
        return user

# User Profile Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone_number', 'bio', 'profile_picture']

# Change Password Serializer
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = self.context['request'].user
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError({"old_password": "Incorrect password"})
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance

# ✅ Container Serializer
class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = ['id', 'container_number', 'created_at', 'uploaded_by']

# ✅ Image Serializer (For Image Uploading)
class ImageSerializer(serializers.ModelSerializer):  # ✅ Correct

    class Meta:
        model = Image  # Ensure it's referencing the correct model
        fields = ['id', 'container', 'image', 'uploaded_at']
