from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.conf import settings


class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    username = None
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    email = models.EmailField(unique=True, verbose_name='Почта')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Пол')
    avatar = models.ImageField(upload_to='avatars/', verbose_name='Аватар')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender', 'avatar']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Rating(models.Model):
    RATING_CHOICES = [
        (True, 'Like'),
        (False, 'Dislike'),
    ]
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='outgoing_ratings',
        verbose_name='Отправитель',
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='incoming_ratings',
        verbose_name='Получатель',
    )
    rating = models.BooleanField(choices=RATING_CHOICES, verbose_name='Оценка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
