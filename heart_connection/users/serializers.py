from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'gender', 'avatar')

    def create(self, validated_data):
        avatar = self.context['request'].FILES.get('avatar')

        user = CustomUser(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            gender=validated_data['gender'],
            avatar=avatar,
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
