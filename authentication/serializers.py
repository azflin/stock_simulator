from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        if validated_data.get('email'):
            user.email = validated_data.get('email')
        user.set_password(validated_data['password'])
        user.save()
        return user
