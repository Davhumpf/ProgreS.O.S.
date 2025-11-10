"""
API URLs para ProgreS.O.S.
Autores: David Rump, Nicolás Garcia
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core_garcia_rodriguez.viewsets import (
    ProyectoViewSet,
    ComentarioViewSet,
    UserViewSet
)

# Router para la API REST
router = DefaultRouter()
router.register(r'proyectos', ProyectoViewSet, basename='proyecto')
router.register(r'comentarios', ComentarioViewSet, basename='comentario')
router.register(r'usuarios', UserViewSet, basename='usuario')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
]
