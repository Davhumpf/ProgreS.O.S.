"""
ProgreS.O.S. URLs Configuration
Autores: David Rump, Nicolás Garcia
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger/OpenAPI Schema
schema_view = get_schema_view(
    openapi.Info(
        title="ProgreS.O.S. API",
        default_version='v1',
        description="""
        Sistema de Seguimiento de Proyectos Académicos
        
        **Autores:** David Rump, Nicolás Garcia
        
        Esta API permite:
        - Gestión de proyectos académicos
        - Sistema de comentarios con notificaciones
        - Visualización de usuarios
        
        **Roles:**
        - Estudiante: CRUD de proyectos propios
        - Docente: Revisión, calificación y aprobación
        
        **Autenticación:** Sesión de Django (debe estar logueado)
        """,
        contact=openapi.Contact(email="soporte@progresos.edu.co"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    patterns=[
        path('api/', include('core_garcia_rodriguez.api_urls')),
    ],
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Home
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    
    # Apps
    path('accounts/', include('accounts_garcia_rodriguez.urls')),
    path('projects/', include('projects_garcia_rodriguez.urls')),
    path('comments/', include('comments_garcia_rodriguez.urls')),
    
    # API REST
    path('api/', include('core_garcia_rodriguez.api_urls')),
    
    # Swagger/OpenAPI Documentation
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/schema/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]

# Media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom admin site header
admin.site.site_header = "ProgreS.O.S. Administración"
admin.site.site_title = "ProgreS.O.S."
admin.site.index_title = "Panel de Administración"
