"""
Admin para Proyectos
Autores: Nicolás Garcia, David Rodriguez
"""

from django.contrib import admin
from .models import Proyecto


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'estudiante', 'estado', 'calificacion', 'fecha_envio']
    list_filter = ['estado', 'fecha_envio']
    search_fields = ['titulo', 'estudiante__username', 'estudiante__first_name', 'estudiante__last_name']
    readonly_fields = ['fecha_envio', 'fecha_revision']
    
    fieldsets = (
        ('Información General', {
            'fields': ('titulo', 'descripcion', 'estudiante', 'documento')
        }),
        ('Estado y Calificación', {
            'fields': ('estado', 'calificacion')
        }),
        ('Fechas', {
            'fields': ('fecha_envio', 'fecha_revision'),
            'classes': ('collapse',)
        }),
    )
