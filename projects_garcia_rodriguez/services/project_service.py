"""
Servicio de Proyectos (Business Logic Layer)
Autores: Nicolás Garcia, David Rodriguez
Principios: Single Responsibility, Open/Closed
"""

from typing import Optional, List
from decimal import Decimal
from django.db.models import QuerySet, Q
from django.utils import timezone
from django.contrib.auth.models import User
from projects_garcia_rodriguez.models import Proyecto
import csv
from io import BytesIO
from django.http import HttpResponse


class ProjectService:
    """
    Servicio que encapsula la lógica de negocio de proyectos.
    Responsabilidad única: operaciones sobre proyectos.
    """
    
    @staticmethod
    def get_projects_for_student(student: User) -> QuerySet:
        """Obtiene todos los proyectos de un estudiante"""
        return Proyecto.objects.filter(estudiante=student).select_related('estudiante')
    
    @staticmethod
    def get_projects_for_teacher(filters: Optional[dict] = None) -> QuerySet:
        """
        Obtiene proyectos con filtros opcionales para docentes.
        
        Args:
            filters: Dict con 'estado' y/o 'estudiante_id'
        """
        queryset = Proyecto.objects.select_related('estudiante').all()
        
        if filters:
            if filters.get('estado'):
                queryset = queryset.filter(estado=filters['estado'])
            
            if filters.get('estudiante_id'):
                queryset = queryset.filter(estudiante_id=filters['estudiante_id'])
        
        return queryset
    
    @staticmethod
    def can_user_edit_project(user: User, proyecto: Proyecto) -> bool:
        """
        Verifica si un usuario puede editar un proyecto.
        
        Reglas:
        - Los DOCENTES pueden revisar/editar cualquier proyecto (cambiar estado y calificar)
        - El ESTUDIANTE dueño puede editar solo si no está aprobado
        """
        # Docentes pueden revisar cualquier proyecto
        if user.groups.filter(name='Docente').exists():
            return True
        
        # Estudiantes solo pueden editar sus proyectos si no están aprobados
        if proyecto.estudiante != user:
            return False
        
        return proyecto.puede_editarse
    
    @staticmethod
    def can_user_delete_project(user: User, proyecto: Proyecto) -> bool:
        """Verifica si un usuario puede eliminar un proyecto"""
        return proyecto.estudiante == user and proyecto.puede_editarse
    
    @staticmethod
    def change_project_state(proyecto: Proyecto, new_state: str, 
                           calificacion: Optional[Decimal] = None) -> Proyecto:
        """
        Cambia el estado de un proyecto y opcionalmente asigna calificación.
        Solo para docentes.
        
        Args:
            proyecto: Instancia del proyecto
            new_state: Nuevo estado ('enviado', 'revision', 'aprobado')
            calificacion: Calificación opcional (0.0 - 5.0)
        
        Returns:
            Proyecto actualizado
        """
        proyecto.estado = new_state
        proyecto.fecha_revision = timezone.now()
        
        if calificacion is not None:
            if 0.0 <= calificacion <= 5.0:
                proyecto.calificacion = calificacion
            else:
                raise ValueError("La calificación debe estar entre 0.0 y 5.0")
        
        proyecto.save()
        return proyecto
    
    @staticmethod
    def export_projects_to_csv(projects: QuerySet) -> HttpResponse:
        """
        Exporta proyectos a formato CSV.
        
        Args:
            projects: QuerySet de proyectos a exportar
        
        Returns:
            HttpResponse con archivo CSV
        """
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="proyectos_export.csv"'
        response.write('\ufeff')  # BOM para Excel UTF-8
        
        writer = csv.writer(response)
        
        # Headers
        writer.writerow([
            'ID',
            'Título',
            'Estudiante',
            'Estado',
            'Fecha Envío',
            'Fecha Revisión',
            'Calificación',
            'Total Comentarios'
        ])
        
        # Data rows
        for proyecto in projects:
            writer.writerow([
                proyecto.id,
                proyecto.titulo,
                proyecto.estudiante.get_full_name() or proyecto.estudiante.username,
                proyecto.get_estado_display(),
                proyecto.fecha_envio.strftime('%Y-%m-%d %H:%M'),
                proyecto.fecha_revision.strftime('%Y-%m-%d %H:%M') if proyecto.fecha_revision else 'N/A',
                f"{proyecto.calificacion:.2f}" if proyecto.calificacion else 'Sin calificar',
                proyecto.total_comentarios()
            ])
        
        return response
    
    @staticmethod
    def get_project_statistics() -> dict:
        """
        Obtiene estadísticas generales de proyectos.
        
        Returns:
            Dict con contadores por estado y promedios
        """
        from django.db.models import Count, Avg
        
        stats = Proyecto.objects.aggregate(
            total=Count('id'),
            enviados=Count('id', filter=Q(estado='enviado')),
            en_revision=Count('id', filter=Q(estado='revision')),
            aprobados=Count('id', filter=Q(estado='aprobado')),
            promedio_general=Avg('calificacion')
        )
        
        return stats
    
    @staticmethod
    def search_projects(query: str, user: Optional[User] = None) -> QuerySet:
        """
        Busca proyectos por título o descripción.
        
        Args:
            query: Texto a buscar
            user: Usuario opcional (si es estudiante, solo busca sus proyectos)
        
        Returns:
            QuerySet de proyectos que coinciden
        """
        queryset = Proyecto.objects.select_related('estudiante')
        
        if user and user.groups.filter(name='Estudiante').exists():
            queryset = queryset.filter(estudiante=user)
        
        if query:
            queryset = queryset.filter(
                Q(titulo__icontains=query) | Q(descripcion__icontains=query)
            )
        
        return queryset
