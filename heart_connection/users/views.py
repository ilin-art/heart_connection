from django.contrib.auth import get_user_model
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import status, generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer, CustomAuthTokenSerializer, RatingSerializer
from .models import Rating
from scripts.send_email import send_notification


User = get_user_model()


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([AllowAny])
class CustomUserCreateAPIView(APIView):

    def post(self, request, format=None):
        serializer = CustomUserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthTokenView(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class UserMatchView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RatingSerializer

    def create(self, request, *args, **kwargs):
        to_user = self.get_object()
        to_user_id = kwargs.get('pk')
        from_user = request.user
        from_user_id = request.user.id
        rating = request.data.get('rating')
        if from_user_id == to_user_id:
            return Response(
                {'detail': 'Нельзя оценивать самого себя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        existing_rating_from = Rating.objects.filter(
            from_user=from_user_id,
            to_user=to_user_id
        ).first()
        if existing_rating_from:
            # Если оценка от from_user уже существует, обновляем ее значение
            existing_rating_from.rating = rating
            existing_rating_from.save()
            serializer = self.get_serializer(existing_rating_from)
        else:
            # Если оценка от from_user не существует, создаем новую оценку
            rating_data = {
                'from_user': from_user_id,
                'to_user': to_user_id,
                'rating': rating
            }
            serializer = self.get_serializer(data=rating_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        # Проверяем, есть ли взаимная симпатия
        exists_rating_to = Rating.objects.filter(
            from_user=to_user_id,
            to_user=from_user_id,
            rating=True
        ).exists()
        exists_rating_from = Rating.objects.filter(
            from_user=from_user_id,
            to_user=to_user_id,
            rating=True
        ).exists()
        if exists_rating_from and exists_rating_to:
            message_from_user = f'Вы понравились {to_user.first_name}! Почта участника: {to_user.email}'
            # send_notification(from_user.email, message_from_user)
            print(message_from_user)
            message_to_user = f'Вы понравились {from_user.first_name}! Почта участника: {from_user.email}'
            # send_notification(to_user.email, message_to_user)
            print(message_to_user)
            return Response({'detail': 'Взаимная симпатия'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
