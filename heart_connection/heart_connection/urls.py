from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


app_name = 'heart_connection'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/clients/', include(('users.urls', 'users'), namespace='users')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)