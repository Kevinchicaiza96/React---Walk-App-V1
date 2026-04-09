from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('core.urls')),
    path('', include('users.urls')),
    path('', include('community.urls')),
    path('', include('routes.urls')),
    path('', include('ranking.urls')),
    path('juegos/', include('games.urls')),

    
    path('api/auth/token/refresh/', TokenRefreshView.as_view()),
    path('api/auth/',       include('users.api_urls')),    
    path('api/comunidad/',  include('community.api_urls')),
    path('api/rutas/',      include('routes.api_urls')),
    path('api/ranking/',    include('ranking.api_urls')),
    path('api/juegos/',     include('games.api_urls')),
    path('api/admin/', include('users.api_urls_admin')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)