from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('proyecto/<int:proyecto_pk>/comentar/', views.ComentarioCreateView.as_view(), name='create'),
]
