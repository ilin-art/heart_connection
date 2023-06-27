from django.urls import path
from .views import CustomUserCreateAPIView


app_name = 'users'

urlpatterns = [
    path('create/', CustomUserCreateAPIView.as_view(), name='user_create'),
]
