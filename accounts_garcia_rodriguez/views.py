from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages

from .services.student_metrics_service import StudentMetricsService


class CustomLoginView(DjangoLoginView):
    """Vista de login personalizada"""
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        # Redirigir al dashboard correspondiente
        if self.request.user.groups.filter(name='Docente').exists():
            return '/accounts/dashboard/'
        return '/projects/'

    def form_valid(self, form):
        messages.success(self.request, f'¡Bienvenido, {form.get_user().get_full_name() or form.get_user().username}!')
        return super().form_valid(form)


@login_required
def logout_view(request):
    """Cerrar sesión"""
    logout(request)
    messages.info(request, 'Has cerrado sesión exitosamente.')
    return redirect('home')


class ProfileView(LoginRequiredMixin, TemplateView):
    """Perfil del usuario con métricas (estudiantes)"""
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        context['is_student'] = user.groups.filter(name='Estudiante').exists()
        context['is_teacher'] = user.groups.filter(name='Docente').exists()
        
        # Métricas para estudiantes
        if context['is_student']:
            from projects_garcia_rodriguez.models import Proyecto
            
            metrics_service = StudentMetricsService()
            context['metrics'] = metrics_service.get_student_metrics(user)
            context['promedio'] = metrics_service.get_student_avg(user)
            
            # Proyectos calificados (ordenados por fecha de revisión)
            context['proyectos_calificados'] = Proyecto.objects.filter(
                estudiante=user,
                calificacion__isnull=False
            ).order_by('-fecha_revision')
        
        return context


class IsTeacherMixin(UserPassesTestMixin):
    """Mixin para verificar que el usuario es docente"""
    def test_func(self):
        return self.request.user.groups.filter(name='Docente').exists()


class DashboardView(LoginRequiredMixin, IsTeacherMixin, TemplateView):
    """Dashboard para docentes con métricas de todos los estudiantes"""
    template_name = 'accounts/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        metrics_service = StudentMetricsService()
        context['students'] = metrics_service.get_all_students_avg()
        
        return context
