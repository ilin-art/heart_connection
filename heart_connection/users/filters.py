import django_filters
from .models import CustomUser


class CustomUserFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    gender = django_filters.ChoiceFilter(choices=CustomUser.GENDER_CHOICES)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'gender']
