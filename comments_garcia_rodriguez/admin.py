"""
Admin para Comentarios
Autores: Nicolás Garcia, David Rodriguez
"""

from django.contrib import admin
from .models import Comentario


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['proyecto', 'autor', 'fecha_creacion', 'texto_truncado']
    list_filter = ['fecha_creacion', 'autor']
    search_fields = ['proyecto__titulo', 'autor__username', 'texto']
    readonly_fields = ['fecha_creacion']
    
    def texto_truncado(self, obj):
        """Muestra los primeros 50 caracteres del comentario"""
        return obj.texto[:50] + '...' if len(obj.texto) > 50 else obj.texto
    texto_truncado.short_description = 'Comentario'
