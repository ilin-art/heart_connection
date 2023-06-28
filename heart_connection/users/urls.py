from django.urls import path
from .views import CustomUserCreateAPIView, CustomAuthTokenView, UserMatchView, UserListView


app_name = 'users'

urlpatterns = [
    path('create/', CustomUserCreateAPIView.as_view(), name='user_create'),
    path('api-token-auth/', CustomAuthTokenView.as_view(), name='api_token_auth'),
    path('<int:pk>/match/', UserMatchView.as_view(), name='client-match'),
    path('list/', UserListView.as_view(), name='user-list'),
]
