from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, HTML
from crispy_forms.bootstrap import FormActions
from .models import Proyecto


class ProyectoForm(forms.ModelForm):
    """Formulario para crear/editar proyectos (estudiantes)"""
    
    class Meta:
        model = Proyecto
        fields = ['titulo', 'descripcion', 'documento']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 5}),
        }
        labels = {
            'titulo': 'Título del Proyecto',
            'descripcion': 'Descripción',
            'documento': 'Documento (PDF, DOC, DOCX)',
        }
        help_texts = {
            'documento': 'Máximo 10 MB. Formatos: PDF, DOC, DOCX',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            Field('titulo', css_class='form-control'),
            Field('descripcion', css_class='form-control'),
            Field('documento', css_class='form-control'),
            FormActions(
                Submit('submit', 'Guardar Proyecto', css_class='btn btn-primary'),
                HTML('<a href="{% url \'projects:list\' %}" class="btn btn-secondary">Cancelar</a>')
            )
        )


class ProyectoReviewForm(forms.ModelForm):
    """Formulario para que docentes revisen y califiquen proyectos"""
    
    class Meta:
        model = Proyecto
        fields = ['estado', 'calificacion']
        labels = {
            'estado': 'Estado del Proyecto',
            'calificacion': 'Calificación (0.0 - 5.0)',
        }
        help_texts = {
            'calificacion': 'Dejar vacío si aún no se califica',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('estado', css_class='col-md-6'),
                Column('calificacion', css_class='col-md-6'),
            ),
            FormActions(
                Submit('submit', 'Actualizar Estado', css_class='btn btn-primary'),
                HTML('<a href="{% url \'projects:list\' %}" class="btn btn-secondary">Cancelar</a>')
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        estado = cleaned_data.get('estado')
        calificacion = cleaned_data.get('calificacion')

        if estado == 'aprobado' and calificacion is None:
            raise forms.ValidationError(
                'Debe asignar una calificación para aprobar el proyecto.'
            )

        return cleaned_data


class ProyectoFilterForm(forms.Form):
    """Formulario para filtrar proyectos (docentes)"""
    
    ESTADO_CHOICES = [('', 'Todos los estados')] + Proyecto.ESTADO_CHOICES
    
    estado = forms.ChoiceField(
        choices=ESTADO_CHOICES,
        required=False,
        label='Estado',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    estudiante = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='Estudiante').order_by('first_name', 'last_name'),
        required=False,
        label='Estudiante',
        empty_label='Todos los estudiantes',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    buscar = forms.CharField(
        required=False,
        label='Buscar',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por título o descripción...'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_class = 'form-inline'
        self.helper.layout = Layout(
            Row(
                Column('estado', css_class='col-md-3'),
                Column('estudiante', css_class='col-md-3'),
                Column('buscar', css_class='col-md-4'),
                Column(
                    Submit('filtrar', 'Filtrar', css_class='btn btn-primary'),
                    css_class='col-md-2 d-flex align-items-end'
                ),
            )
        )
