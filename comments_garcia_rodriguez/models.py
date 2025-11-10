"""
Modelo de Comentarios
Autores: Nicolás Garcia, David Rodriguez
"""

from django.db import models
from django.contrib.auth.models import User
from projects_garcia_rodriguez.models import Proyecto


class Comentario(models.Model):
    """
    Representa un comentario en un proyecto académico.
    Al crear un comentario, se envía notificación por email al estudiante.
    """
    
    proyecto = models.ForeignKey(
        Proyecto,
        related_name='comentarios',
        on_delete=models.CASCADE,
        verbose_name='Proyecto'
    )
    
    autor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Autor'
    )
    
    texto = models.TextField(
        verbose_name='Comentario',
        help_text='Escriba su comentario o retroalimentación'
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    
    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        ordering = ['fecha_creacion']
        indexes = [
            models.Index(fields=['proyecto', 'fecha_creacion']),
        ]
    
    def __str__(self):
        return f"Comentario de {self.autor.username} en {self.proyecto.titulo}"
    
    @property
    def es_del_docente(self):
        """Verifica si el comentario es de un docente"""
        return self.autor.groups.filter(name='Docente').exists()
    
    @property
    def es_del_estudiante(self):
        """Verifica si el comentario es del estudiante dueño del proyecto"""
        return self.autor == self.proyecto.estudiante
