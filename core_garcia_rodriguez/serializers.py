"""
API Serializers para ProgreS.O.S.
Autores: David Rump, Nicolás Garcia
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from projects_garcia_rodriguez.models import Proyecto
from comments_garcia_rodriguez.models import Comentario


class UserSerializer(serializers.ModelSerializer):
    """Serializer para Usuario"""
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name']
        read_only_fields = ['id']
    
    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username


class ProyectoSerializer(serializers.ModelSerializer):
    """Serializer para Proyecto"""
    estudiante = UserSerializer(read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    
    class Meta:
        model = Proyecto
        fields = [
            'id', 'titulo', 'descripcion', 'documento', 'estado',
            'estado_display', 'calificacion', 'estudiante',
            'fecha_creacion', 'fecha_actualizacion'
        ]
        read_only_fields = ['id', 'estudiante', 'fecha_creacion', 'fecha_actualizacion']


class ProyectoCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear Proyecto"""
    
    class Meta:
        model = Proyecto
        fields = ['titulo', 'descripcion', 'documento']


class ComentarioSerializer(serializers.ModelSerializer):
    """Serializer para Comentario"""
    autor = UserSerializer(read_only=True)
    proyecto_titulo = serializers.CharField(source='proyecto.titulo', read_only=True)
    
    class Meta:
        model = Comentario
        fields = [
            'id', 'proyecto', 'proyecto_titulo', 'autor',
            'texto', 'fecha_creacion'
        ]
        read_only_fields = ['id', 'autor', 'fecha_creacion']


class ComentarioCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear Comentario"""
    
    class Meta:
        model = Comentario
        fields = ['proyecto', 'texto']
