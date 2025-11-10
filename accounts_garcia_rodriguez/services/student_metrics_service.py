"""
Servicio de Métricas de Estudiantes
Autores: Nicolás Garcia, David Rodriguez
Responsabilidad: Cálculo de promedios y estadísticas por estudiante
"""

from typing import Optional, Dict
from decimal import Decimal
from django.db.models import Avg, Count, Q, QuerySet
from django.contrib.auth.models import User
from django.core.cache import cache


class StudentMetricsService:
    """
    Servicio para calcular métricas y promedios de estudiantes.
    Principio de Responsabilidad Única: solo maneja métricas.
    """
    
    CACHE_TIMEOUT = 300  # 5 minutos
    
    @staticmethod
    def get_student_avg(student: User, use_cache: bool = True) -> Optional[Decimal]:
        """
        Calcula el promedio de calificaciones de un estudiante.
        Excluye proyectos sin calificación (null).
        
        Args:
            student: Usuario estudiante
            use_cache: Si usar caché (True por defecto)
        
        Returns:
            Decimal con el promedio o None si no hay calificaciones
        """
        cache_key = f'student_avg_{student.id}'
        
        if use_cache:
            cached_avg = cache.get(cache_key)
            if cached_avg is not None:
                return cached_avg
        
        result = student.proyectos.filter(
            calificacion__isnull=False
        ).aggregate(
            promedio=Avg('calificacion')
        )
        
        avg = result['promedio']
        
        if use_cache and avg is not None:
            cache.set(cache_key, avg, StudentMetricsService.CACHE_TIMEOUT)
        
        return avg
    
    @staticmethod
    def get_student_metrics(student: User) -> Dict:
        """
        Obtiene métricas completas de un estudiante.
        
        Returns:
            Dict con total_proyectos, proyectos_calificados, promedio, etc.
        """
        metrics = student.proyectos.aggregate(
            total_proyectos=Count('id'),
            proyectos_calificados=Count('id', filter=Q(calificacion__isnull=False)),
            proyectos_aprobados=Count('id', filter=Q(estado='aprobado')),
            proyectos_en_revision=Count('id', filter=Q(estado='revision')),
            proyectos_enviados=Count('id', filter=Q(estado='enviado')),
            promedio=Avg('calificacion', filter=Q(calificacion__isnull=False))
        )
        
        return metrics
    
    @staticmethod
    def get_all_students_avg() -> QuerySet:
        """
        Obtiene el promedio de todos los estudiantes.
        Solo incluye estudiantes con al menos un proyecto calificado.
        
        Returns:
            QuerySet de usuarios con annotate 'promedio' y 'total_calificados'
        """
        from django.conf import settings
        
        students = User.objects.filter(
            groups__name=settings.STUDENT_GROUP_NAME
        ).annotate(
            promedio=Avg('proyectos__calificacion', filter=Q(proyectos__calificacion__isnull=False)),
            total_proyectos=Count('proyectos'),
            total_calificados=Count('proyectos', filter=Q(proyectos__calificacion__isnull=False)),
            proyectos_aprobados=Count('proyectos', filter=Q(proyectos__estado='aprobado'))
        ).filter(
            total_proyectos__gt=0  # Solo estudiantes con proyectos
        ).order_by('-promedio')
        
        return students
    
    @staticmethod
    def export_student_metrics_to_csv(students: QuerySet = None) -> 'HttpResponse':
        """
        Exporta métricas de estudiantes a CSV.
        
        Args:
            students: QuerySet opcional de estudiantes. Si None, exporta todos.
        
        Returns:
            HttpResponse con archivo CSV
        """
        from django.http import HttpResponse
        import csv
        
        if students is None:
            students = StudentMetricsService.get_all_students_avg()
        
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="metricas_estudiantes.csv"'
        response.write('\ufeff')  # BOM
        
        writer = csv.writer(response)
        
        # Headers
        writer.writerow([
            'Estudiante',
            'Email',
            'Total Proyectos',
            'Proyectos Calificados',
            'Proyectos Aprobados',
            'Promedio'
        ])
        
        # Data
        for student in students:
            writer.writerow([
                student.get_full_name() or student.username,
                student.email or 'Sin email',
                getattr(student, 'total_proyectos', 0),
                getattr(student, 'total_calificados', 0),
                getattr(student, 'proyectos_aprobados', 0),
                f"{student.promedio:.2f}" if student.promedio else 'Sin calificar'
            ])
        
        return response
    
    @staticmethod
    def invalidate_student_cache(student: User):
        """
        Invalida el caché de métricas de un estudiante.
        Llamar cuando se actualiza/crea una calificación.
        """
        cache_key = f'student_avg_{student.id}'
        cache.delete(cache_key)
