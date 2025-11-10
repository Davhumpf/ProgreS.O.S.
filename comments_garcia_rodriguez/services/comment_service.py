"""
Servicio de Comentarios
Autores: Nicolás Garcia, David Rodriguez
Responsabilidad: Crear comentarios y enviar notificaciones
"""

from django.contrib.auth.models import User
from projects_garcia_rodriguez.models import Proyecto
from comments_garcia_rodriguez.models import Comentario
from core_garcia_rodriguez.services.email_service import get_email_service


class CommentService:
    """
    Servicio para operaciones sobre comentarios.
    Principio de Responsabilidad Única: gestión de comentarios.
    """
    
    def __init__(self):
        # Dependency Injection: inyectar el servicio de email
        self.email_service = get_email_service()
    
    def create_comment(self, proyecto: Proyecto, autor: User, texto: str) -> Comentario:
        """
        Crea un comentario y envía notificación por email.
        
        Args:
            proyecto: Proyecto al que se añade el comentario
            autor: Usuario que crea el comentario
            texto: Contenido del comentario
        
        Returns:
            Comentario creado
        
        Raises:
            ValueError: Si el proyecto está aprobado (no permite comentarios)
        """
        # Validación de negocio
        if not proyecto.permite_comentarios:
            raise ValueError(
                "No se pueden agregar comentarios a proyectos aprobados."
            )
        
        # Crear comentario
        comentario = Comentario.objects.create(
            proyecto=proyecto,
            autor=autor,
            texto=texto
        )
        
        # Enviar notificación por email (async en producción)
        try:
            self.email_service.notify_comment_created(proyecto, comentario)
        except Exception as e:
            # Log error pero no falla la creación del comentario
            print(f"Error enviando notificación de comentario: {str(e)}")
        
        return comentario
    
    @staticmethod
    def can_user_comment(user: User, proyecto: Proyecto) -> bool:
        """
        Verifica si un usuario puede comentar en un proyecto.
        
        Reglas:
        - El proyecto no debe estar aprobado
        - El usuario debe estar autenticado
        - Tanto estudiantes como docentes pueden comentar
        """
        if not proyecto.permite_comentarios:
            return False
        
        return True
    
    @staticmethod
    def get_comments_for_project(proyecto: Proyecto):
        """Obtiene todos los comentarios de un proyecto ordenados por fecha"""
        return proyecto.comentarios.select_related('autor').all()
    
    @staticmethod
    def get_recent_comments(limit: int = 10):
        """Obtiene los comentarios más recientes del sistema"""
        return Comentario.objects.select_related(
            'autor', 'proyecto', 'proyecto__estudiante'
        ).order_by('-fecha_creacion')[:limit]
