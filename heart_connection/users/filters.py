import math
import django_filters.rest_framework as filters
from .models import CustomUser


class CustomUserFilter(filters.FilterSet):
    first_name = filters.CharFilter(lookup_expr='icontains')
    last_name = filters.CharFilter(lookup_expr='icontains')
    gender = filters.ChoiceFilter(choices=CustomUser.GENDER_CHOICES)
    distance = filters.NumberFilter(method='filter_distance')

    def filter_distance(self, queryset, name, value, *args, **kwargs):
        if value and self.request.user.longitude and self.request.user.latitude:
            user_longitude = math.radians(float(self.request.user.longitude))
            user_latitude = math.radians(float(self.request.user.latitude))
            distance = float(value)
            filtered_ids = []
            for obj in queryset:
                if obj.longitude and obj.latitude:
                    obj_longitude = math.radians(float(obj.longitude))
                    obj_latitude = math.radians(float(obj.latitude))
                    d_longitude = obj_longitude - user_longitude
                    d_latitude = obj_latitude - user_latitude
                    a = math.sin(d_latitude / 2) ** 2 + math.cos(user_latitude) * math.cos(obj_latitude) * math.sin(d_longitude / 2) ** 2
                    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                    earth_radius = 6371
                    distance_km = earth_radius * c
                    if distance_km <= distance:
                        filtered_ids.append(obj.id)
            queryset = queryset.filter(id__in=filtered_ids)
        return queryset
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'gender', 'distance']
