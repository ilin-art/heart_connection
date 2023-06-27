from django.contrib import admin
from .models import CustomUser


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'email', 'gender',)
    list_display_links = ('pk', 'first_name', 'last_name',)
    search_fields = ('first_name', 'last_name', 'email',)

admin.site.register(CustomUser, UserAdmin)