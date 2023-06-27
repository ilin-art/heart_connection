from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'gender', 'avatar')

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
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
