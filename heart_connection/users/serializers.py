from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import CustomUser, Rating


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'id', 'email', 'password', 'first_name', 'last_name',
            'gender', 'avatar', 'longitude', 'latitude'
        )

    def create(self, validated_data):
        avatar = self.context['request'].FILES.get('avatar')
        image = Image.open(avatar)
        watermark = Image.open('media/watermark/watermark.png')
        image.paste(watermark, (0, 0), watermark)
        output = BytesIO()
        image.save(output, format='PNG')
        output.seek(0)
        processed_avatar = InMemoryUploadedFile(
            output, None, f'{avatar.name.split(".")[0]}_processed.png', 'image/png', output.tell(), None
        )
        user = CustomUser(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            gender=validated_data['gender'],
            avatar=processed_avatar,
            longitude=validated_data['longitude'],
            latitude=validated_data['latitude'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                msg = 'Невозможно аутентифицировать с предоставленными данными'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Пожалуйста, предоставьте адрес электронной почты и пароль'
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs


class RatingSerializer(serializers.ModelSerializer):
    rating = serializers.BooleanField()

    class Meta:
        model = Rating
        fields = ('from_user', 'to_user', 'rating')
