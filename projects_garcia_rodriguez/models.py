"""
Modelo de Proyectos Académicos
Autores: Nicolás Garcia, David Rodriguez
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone


class Proyecto(models.Model):
    """
    Representa un proyecto académico enviado por un estudiante.
    
    Estados del proyecto:
    - enviado: Proyecto recién creado
    - revision: En proceso de revisión por docente
    - aprobado: Proyecto aprobado (bloquea nuevos comentarios)
    """
    
    ESTADO_CHOICES = [
        ('enviado', 'Enviado'),
        ('revision', 'En Revisión'),
        ('aprobado', 'Aprobado'),
    ]
    
    titulo = models.CharField(
        max_length=200,
        verbose_name='Título',
        help_text='Título descriptivo del proyecto'
    )
    
    descripcion = models.TextField(
        verbose_name='Descripción',
        help_text='Descripción detallada del proyecto'
    )
    
    estudiante = models.ForeignKey(
        User,
        related_name='proyectos',
        on_delete=models.CASCADE,
        verbose_name='Estudiante',
        limit_choices_to={'groups__name': 'Estudiante'}
    )
    
    documento = models.FileField(
        upload_to='proyectos/%Y/%m/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
        verbose_name='Documento',
        help_text='Archivo del proyecto (PDF, DOC, DOCX)'
    )
    
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='enviado',
        verbose_name='Estado'
    )
    
    fecha_envio = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Envío'
    )
    
    fecha_revision = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de Revisión',
        help_text='Fecha de la última revisión'
    )
    
    calificacion = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        verbose_name='Calificación',
        help_text='Calificación del proyecto (0.0 - 5.0)'
    )
    
    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
        ordering = ['-fecha_envio']
        indexes = [
            models.Index(fields=['estado', '-fecha_envio']),
            models.Index(fields=['estudiante', '-fecha_envio']),
        ]
    
    def __str__(self):
        return f"{self.titulo} - {self.estudiante.get_full_name() or self.estudiante.username}"
    
    def save(self, *args, **kwargs):
        """Override para actualizar fecha_revision al cambiar estado"""
        if self.pk:
            old = Proyecto.objects.filter(pk=self.pk).first()
            if old and old.estado != self.estado:
                self.fecha_revision = timezone.now()
        super().save(*args, **kwargs)
    
    @property
    def esta_aprobado(self):
        """Verifica si el proyecto está aprobado"""
        return self.estado == 'aprobado'
    
    @property
    def puede_editarse(self):
        """Verifica si el proyecto puede ser editado por el estudiante"""
        return self.estado != 'aprobado'
    
    @property
    def permite_comentarios(self):
        """Verifica si se pueden agregar comentarios"""
        return self.estado != 'aprobado'
    
    def get_badge_class(self):
        """Retorna la clase CSS del badge según el estado"""
        badges = {
            'enviado': 'bg-info',
            'revision': 'bg-warning',
            'aprobado': 'bg-success',
        }
        return badges.get(self.estado, 'bg-secondary')
    
    def total_comentarios(self):
        """Retorna el total de comentarios del proyecto"""
        return self.comentarios.count()
