"""
API v1 URL configuration.
All API endpoints are versioned for future compatibility.
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Versioning - All endpoints under /api/v1/
    path('api/v1/', include('api.urls')),
    
    # Backward compatibility - Redirect old /api/ to /api/v1/
    path('api/', include('api.urls')),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('apidocs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui-legacy'),
] + staticfiles_urlpatterns()
