from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from crispy_forms.bootstrap import FormActions
from .models import Comentario


class ComentarioForm(forms.ModelForm):
    """Formulario para crear comentarios en proyectos"""
    
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Escribe tu comentario o retroalimentación aquí...'
            }),
        }
        labels = {
            'texto': 'Comentario',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('texto', css_class='form-control'),
            FormActions(
                Submit('submit', 'Enviar Comentario', css_class='btn btn-primary')
            )
        )
