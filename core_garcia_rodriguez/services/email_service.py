"""
Servicio de Email con patrón Strategy (SOLID - Dependency Inversion)
Autores: Nicolás Garcia, David Rodriguez
"""

from abc import ABC, abstractmethod
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from typing import Dict, Any


class EmailService(ABC):
    """
    Interfaz abstracta para servicios de email.
    Permite cambiar la implementación sin afectar el código cliente.
    """
    
    @abstractmethod
    def notify_comment_created(self, proyecto, comentario) -> bool:
        """
        Envía notificación al estudiante cuando se crea un comentario.
        
        Args:
            proyecto: Instancia del modelo Proyecto
            comentario: Instancia del modelo Comentario
            
        Returns:
            bool: True si el email se envió correctamente
        """
        pass
    
    @abstractmethod
    def send_email(self, subject: str, to_emails: list, context: Dict[str, Any], 
                   template_name: str) -> bool:
        """
        Método genérico para enviar emails con template.
        
        Args:
            subject: Asunto del email
            to_emails: Lista de destinatarios
            context: Contexto para el template
            template_name: Nombre del template HTML
            
        Returns:
            bool: True si el email se envió correctamente
        """
        pass


class ConsoleEmailService(EmailService):
    """
    Implementación de EmailService que imprime en consola (desarrollo).
    """
    
    def notify_comment_created(self, proyecto, comentario) -> bool:
        """Notifica al estudiante sobre un nuevo comentario"""
        
        if comentario.autor == proyecto.estudiante:
            # No enviar email si el estudiante comenta su propio proyecto
            return True
        
        context = {
            'proyecto': proyecto,
            'comentario': comentario,
            'estudiante': proyecto.estudiante,
            'autor': comentario.autor,
        }
        
        subject = f'Nuevo comentario en tu proyecto: {proyecto.titulo}'
        to_emails = [proyecto.estudiante.email] if proyecto.estudiante.email else []
        
        if not to_emails:
            print(f"⚠️  Estudiante {proyecto.estudiante.username} no tiene email configurado")
            return False
        
        return self.send_email(
            subject=subject,
            to_emails=to_emails,
            context=context,
            template_name='emails/comment_created.html'
        )
    
    def send_email(self, subject: str, to_emails: list, context: Dict[str, Any],
                   template_name: str) -> bool:
        """Envía email usando el backend configurado"""
        
        try:
            # Renderizar template HTML
            html_message = render_to_string(template_name, context)
            
            # Renderizar template de texto plano
            text_template = template_name.replace('.html', '.txt')
            try:
                plain_message = render_to_string(text_template, context)
            except:
                plain_message = f"{subject}\n\n{context.get('texto', '')}"
            
            # Enviar email
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=to_emails,
                html_message=html_message,
                fail_silently=False,
            )
            
            print(f"✅ Email enviado: {subject} -> {to_emails}")
            return True
            
        except Exception as e:
            print(f"❌ Error enviando email: {str(e)}")
            return False


class SMTPEmailService(EmailService):
    """
    Implementación de EmailService para producción con SMTP.
    Usar cuando se configure EMAIL_BACKEND con SMTP real.
    """
    
    def notify_comment_created(self, proyecto, comentario) -> bool:
        """Implementación idéntica a ConsoleEmailService"""
        if comentario.autor == proyecto.estudiante:
            return True
        
        context = {
            'proyecto': proyecto,
            'comentario': comentario,
            'estudiante': proyecto.estudiante,
            'autor': comentario.autor,
        }
        
        subject = f'Nuevo comentario en tu proyecto: {proyecto.titulo}'
        to_emails = [proyecto.estudiante.email] if proyecto.estudiante.email else []
        
        if not to_emails:
            return False
        
        return self.send_email(
            subject=subject,
            to_emails=to_emails,
            context=context,
            template_name='emails/comment_created.html'
        )
    
    def send_email(self, subject: str, to_emails: list, context: Dict[str, Any],
                   template_name: str) -> bool:
        """Implementación idéntica a ConsoleEmailService"""
        try:
            html_message = render_to_string(template_name, context)
            text_template = template_name.replace('.html', '.txt')
            try:
                plain_message = render_to_string(text_template, context)
            except:
                plain_message = f"{subject}\n\n{context.get('texto', '')}"
            
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=to_emails,
                html_message=html_message,
                fail_silently=False,
            )
            
            return True
        except Exception as e:
            print(f"Error enviando email: {str(e)}")
            return False


def get_email_service() -> EmailService:
    """
    Factory function para obtener la implementación de EmailService.
    Lee la configuración desde settings.EMAIL_SERVICE_CLASS
    """
    from django.utils.module_loading import import_string
    
    service_class = getattr(settings, 'EMAIL_SERVICE_CLASS', 
                           'core_garcia_rodriguez.services.email_service.ConsoleEmailService')
    
    EmailServiceClass = import_string(service_class)
    return EmailServiceClass()
