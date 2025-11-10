from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.ProyectoListView.as_view(), name='list'),
    path('<int:pk>/', views.ProyectoDetailView.as_view(), name='detail'),
    path('nuevo/', views.ProyectoCreateView.as_view(), name='create'),
    path('<int:pk>/editar/', views.ProyectoUpdateView.as_view(), name='update'),
    path('<int:pk>/eliminar/', views.ProyectoDeleteView.as_view(), name='delete'),
]
