from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from .models import Proyecto
from .forms import ProyectoForm, ProyectoReviewForm, ProyectoFilterForm
from .services.project_service import ProjectService


class IsStudentMixin(UserPassesTestMixin):
    """Mixin para verificar que el usuario es estudiante"""
    def test_func(self):
        return self.request.user.groups.filter(name='Estudiante').exists()


class IsTeacherMixin(UserPassesTestMixin):
    """Mixin para verificar que el usuario es docente"""
    def test_func(self):
        return self.request.user.groups.filter(name='Docente').exists()


class ProyectoListView(LoginRequiredMixin, ListView):
    """Lista de proyectos (con filtros para docentes)"""
    model = Proyecto
    template_name = 'projects/proyecto_list.html'
    context_object_name = 'proyectos'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        
        # Estudiantes solo ven sus proyectos
        if user.groups.filter(name='Estudiante').exists():
            qs = ProjectService.get_projects_for_student(user)
        else:
            # Docentes ven todos con filtros
            filters = {
                'estado': self.request.GET.get('estado', ''),
                'estudiante_id': self.request.GET.get('estudiante', ''),
            }
            qs = ProjectService.get_projects_for_teacher(filters)
            
            # Búsqueda por texto
            buscar = self.request.GET.get('buscar', '').strip()
            if buscar:
                qs = qs.filter(
                    Q(titulo__icontains=buscar) | Q(descripcion__icontains=buscar)
                )
        
        return qs.order_by('-fecha_envio')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_teacher'] = self.request.user.groups.filter(name='Docente').exists()
        context['is_student'] = self.request.user.groups.filter(name='Estudiante').exists()
        
        # Agregar formulario de filtros para docentes
        if context['is_teacher']:
            context['filter_form'] = ProyectoFilterForm(self.request.GET)
            context['statistics'] = ProjectService.get_project_statistics()
        
        return context


class ProyectoDetailView(LoginRequiredMixin, DetailView):
    """Detalle de un proyecto con comentarios"""
    model = Proyecto
    template_name = 'projects/proyecto_detail.html'
    context_object_name = 'proyecto'

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        
        # Estudiantes solo pueden ver sus propios proyectos
        if user.groups.filter(name='Estudiante').exists():
            qs = qs.filter(estudiante=user)
        
        return qs.select_related('estudiante').prefetch_related('comentarios__autor')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_edit'] = ProjectService.can_user_edit_project(
            self.request.user, self.object
        )
        context['can_delete'] = ProjectService.can_user_delete_project(
            self.request.user, self.object
        )
        context['is_teacher'] = self.request.user.groups.filter(name='Docente').exists()
        context['is_student'] = self.request.user.groups.filter(name='Estudiante').exists()
        return context


class ProyectoCreateView(LoginRequiredMixin, IsStudentMixin, CreateView):
    """Crear nuevo proyecto (solo estudiantes)"""
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'projects/proyecto_form.html'
    success_url = reverse_lazy('projects:list')

    def form_valid(self, form):
        form.instance.estudiante = self.request.user
        form.instance.estado = 'enviado'
        messages.success(self.request, '✅ Proyecto creado exitosamente.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nuevo Proyecto'
        return context


class ProyectoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Editar proyecto existente"""
    model = Proyecto
    template_name = 'projects/proyecto_form.html'

    def test_func(self):
        proyecto = self.get_object()
        return ProjectService.can_user_edit_project(self.request.user, proyecto)

    def get_form_class(self):
        # Docentes usan ProyectoReviewForm, estudiantes ProyectoForm
        if self.request.user.groups.filter(name='Docente').exists():
            return ProyectoReviewForm
        return ProyectoForm

    def get_success_url(self):
        return reverse_lazy('projects:detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        if isinstance(form, ProyectoReviewForm):
            messages.success(self.request, '✅ Proyecto revisado y actualizado.')
        else:
            messages.success(self.request, '✅ Proyecto actualizado exitosamente.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.groups.filter(name='Docente').exists():
            context['titulo'] = 'Revisar Proyecto'
        else:
            context['titulo'] = 'Editar Proyecto'
        return context


class ProyectoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Eliminar proyecto (solo estudiante dueño y si no está aprobado)"""
    model = Proyecto
    template_name = 'projects/proyecto_confirm_delete.html'
    success_url = reverse_lazy('projects:list')

    def test_func(self):
        proyecto = self.get_object()
        return ProjectService.can_user_delete_project(self.request.user, proyecto)

    def delete(self, request, *args, **kwargs):
        messages.success(request, '✅ Proyecto eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)
