from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView

from projects_garcia_rodriguez.models import Proyecto
from .forms import ComentarioForm
from .services.comment_service import CommentService


class ComentarioCreateView(LoginRequiredMixin, CreateView):
    """Crear comentario en un proyecto"""
    form_class = ComentarioForm
    template_name = 'comments/comentario_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.proyecto = get_object_or_404(Proyecto, pk=kwargs['proyecto_pk'])
        
        # Verificar si el usuario puede comentar
        comment_service = CommentService()
        if not comment_service.can_user_comment(request.user, self.proyecto):
            messages.error(request, '❌ No puedes comentar en este proyecto.')
            return redirect('projects:detail', pk=self.proyecto.pk)
        
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            comment_service = CommentService()
            comment_service.create_comment(
                proyecto=self.proyecto,
                autor=self.request.user,
                texto=form.cleaned_data['texto']
            )
            messages.success(self.request, '✅ Comentario agregado exitosamente.')
        except ValueError as e:
            messages.error(self.request, f'❌ {str(e)}')
        
        return redirect('projects:detail', pk=self.proyecto.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proyecto'] = self.proyecto
        return context
