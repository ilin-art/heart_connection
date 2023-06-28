from django.contrib import admin
from .models import CustomUser, Rating


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'email', 'gender',)
    list_display_links = ('pk', 'first_name', 'last_name',)
    search_fields = ('first_name', 'last_name', 'email',)

admin.site.register(CustomUser, UserAdmin)

class RatingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'from_user', 'to_user', 'rating',)
    list_display_links = ('pk', 'from_user', 'to_user', 'rating',)
    search_fields = ('from_user', 'to_user', 'rating',)

admin.site.register(Rating, RatingAdmin)