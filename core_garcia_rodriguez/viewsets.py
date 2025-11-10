"""
API ViewSets para ProgreS.O.S.
Autores: David Rump, Nicolás Garcia
"""

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User

from projects_garcia_rodriguez.models import Proyecto
from comments_garcia_rodriguez.models import Comentario
from .serializers import (
    UserSerializer, 
    ProyectoSerializer, 
    ProyectoCreateSerializer,
    ComentarioSerializer,
    ComentarioCreateSerializer
)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Permiso personalizado: solo el dueño puede editar"""
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.estudiante == request.user


class ProyectoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar proyectos académicos.
    
    list: Listar todos los proyectos (estudiantes ven solo los suyos)
    create: Crear un nuevo proyecto
    retrieve: Ver detalles de un proyecto
    update: Actualizar un proyecto completo
    partial_update: Actualizar parcialmente un proyecto
    destroy: Eliminar un proyecto
    """
    queryset = Proyecto.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ProyectoCreateSerializer
        return ProyectoSerializer
    
    def get_queryset(self):
        """Estudiantes solo ven sus proyectos, docentes ven todos"""
        user = self.request.user
        if user.groups.filter(name='Docente').exists():
            return Proyecto.objects.all()
        return Proyecto.objects.filter(estudiante=user)
    
    def perform_create(self, serializer):
        """Asignar el estudiante automáticamente"""
        serializer.save(estudiante=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def calificar(self, request, pk=None):
        """
        Calificar un proyecto (solo docentes).
        
        Body: {"calificacion": 4.5, "estado": "aprobado"}
        """
        proyecto = self.get_object()
        
        # Verificar que sea docente
        if not request.user.groups.filter(name='Docente').exists():
            return Response(
                {'error': 'Solo los docentes pueden calificar'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        calificacion = request.data.get('calificacion')
        nuevo_estado = request.data.get('estado')
        
        if calificacion is not None:
            try:
                calificacion = float(calificacion)
                if 0 <= calificacion <= 5:
                    proyecto.calificacion = calificacion
                else:
                    return Response(
                        {'error': 'La calificación debe estar entre 0 y 5'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except ValueError:
                return Response(
                    {'error': 'Calificación inválida'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        if nuevo_estado:
            estados_validos = ['borrador', 'enviado', 'en_revision', 'aprobado', 'rechazado']
            if nuevo_estado in estados_validos:
                proyecto.estado = nuevo_estado
            else:
                return Response(
                    {'error': f'Estado inválido. Opciones: {", ".join(estados_validos)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        proyecto.save()
        serializer = ProyectoSerializer(proyecto)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def mis_proyectos(self, request):
        """Obtener solo los proyectos del usuario actual"""
        proyectos = Proyecto.objects.filter(estudiante=request.user)
        serializer = self.get_serializer(proyectos, many=True)
        return Response(serializer.data)


class ComentarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar comentarios.
    
    list: Listar todos los comentarios
    create: Crear un nuevo comentario
    retrieve: Ver detalles de un comentario
    update: Actualizar un comentario
    partial_update: Actualizar parcialmente un comentario
    destroy: Eliminar un comentario
    """
    queryset = Comentario.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ComentarioCreateSerializer
        return ComentarioSerializer
    
    def get_queryset(self):
        """Filtrar comentarios según proyecto si se proporciona"""
        queryset = Comentario.objects.all()
        proyecto_id = self.request.query_params.get('proyecto', None)
        if proyecto_id:
            queryset = queryset.filter(proyecto_id=proyecto_id)
        return queryset
    
    def perform_create(self, serializer):
        """Asignar el autor automáticamente"""
        serializer.save(autor=self.request.user)
    
    @action(detail=False, methods=['get'])
    def proyecto(self, request):
        """
        Obtener comentarios de un proyecto específico.
        
        Query params: ?proyecto_id=1
        """
        proyecto_id = request.query_params.get('proyecto_id')
        if not proyecto_id:
            return Response(
                {'error': 'Se requiere el parámetro proyecto_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        comentarios = Comentario.objects.filter(proyecto_id=proyecto_id)
        serializer = self.get_serializer(comentarios, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint para ver usuarios (solo lectura).
    
    list: Listar todos los usuarios
    retrieve: Ver detalles de un usuario
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Obtener información del usuario actual"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
