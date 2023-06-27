from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


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
