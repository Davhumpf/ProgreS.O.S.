"""
Management command para crear datos de prueba (seed data)
Autores: Nicolás Garcia, David Rodriguez
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from projects_garcia_rodriguez.models import Proyecto
from comments_garcia_rodriguez.models import Comentario


class Command(BaseCommand):
    help = 'Crea grupos, usuarios demo y datos de prueba para ProgreS.O.S.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('🚀 Iniciando creación de datos de prueba...'))

        # 1. Crear grupos
        self.stdout.write('\n📋 Creando grupos...')
        estudiante_group, created = Group.objects.get_or_create(name='Estudiante')
        if created:
            self.stdout.write(self.style.SUCCESS('  ✅ Grupo "Estudiante" creado'))
        else:
            self.stdout.write('  ℹ️  Grupo "Estudiante" ya existe')

        docente_group, created = Group.objects.get_or_create(name='Docente')
        if created:
            self.stdout.write(self.style.SUCCESS('  ✅ Grupo "Docente" creado'))
        else:
            self.stdout.write('  ℹ️  Grupo "Docente" ya existe')

        # 2. Crear usuarios demo
        self.stdout.write('\n👥 Creando usuarios demo...')
        
        # EMAIL ÚNICO PARA PRUEBAS
        TEST_EMAIL = 'scpu.v1@gmail.com'
        
        # Estudiantes
        estudiantes = []
        estudiantes_data = [
            ('estudiante_demo', 'Juan', 'Pérez'),
            ('maria_garcia', 'María', 'García'),
            ('carlos_lopez', 'Carlos', 'López'),
        ]

        for username, first_name, last_name in estudiantes_data:
            if not User.objects.filter(username=username).exists():
                estudiante = User.objects.create_user(
                    username=username,
                    email=TEST_EMAIL,  # Todos usan el mismo email
                    password='demo123',
                    first_name=first_name,
                    last_name=last_name
                )
                estudiante.groups.add(estudiante_group)
                estudiantes.append(estudiante)
                self.stdout.write(self.style.SUCCESS(f'  ✅ Estudiante: {username} / demo123 ({TEST_EMAIL})'))
            else:
                estudiante = User.objects.get(username=username)
                # Actualizar email si ya existe
                estudiante.email = TEST_EMAIL
                estudiante.save()
                estudiantes.append(estudiante)
                self.stdout.write(f'  ℹ️  Estudiante "{username}" ya existe - email actualizado')

        # Docente
        if not User.objects.filter(username='docente_demo').exists():
            docente = User.objects.create_user(
                username='docente_demo',
                email=TEST_EMAIL,  # Mismo email
                password='demo123',
                first_name='María',
                last_name='González'
            )
            docente.groups.add(docente_group)
            self.stdout.write(self.style.SUCCESS(f'  ✅ Docente: docente_demo / demo123 ({TEST_EMAIL})'))
        else:
            docente = User.objects.get(username='docente_demo')
            # Actualizar email si ya existe
            docente.email = TEST_EMAIL
            docente.save()
            self.stdout.write('  ℹ️  Docente "docente_demo" ya existe - email actualizado')

        # 3. Crear proyectos demo
        self.stdout.write('\n📁 Creando proyectos demo...')
        
        if Proyecto.objects.count() == 0:
            proyectos_data = [
                {
                    'estudiante': estudiantes[0],
                    'titulo': 'Sistema de Gestión de Biblioteca',
                    'descripcion': 'Aplicación web para gestionar préstamos de libros, catálogo y usuarios de una biblioteca universitaria.',
                    'estado': 'aprobado',
                    'calificacion': Decimal('4.8'),
                    'dias_atras': 30
                },
                {
                    'estudiante': estudiantes[0],
                    'titulo': 'API REST para E-commerce',
                    'descripcion': 'API RESTful desarrollada con Django para gestionar productos, órdenes y pagos de una tienda online.',
                    'estado': 'revision',
                    'calificacion': None,
                    'dias_atras': 10
                },
                {
                    'estudiante': estudiantes[1],
                    'titulo': 'Dashboard de Analítica',
                    'descripcion': 'Dashboard interactivo con Django y Chart.js para visualizar métricas de ventas en tiempo real.',
                    'estado': 'aprobado',
                    'calificacion': Decimal('4.5'),
                    'dias_atras': 25
                },
                {
                    'estudiante': estudiantes[1],
                    'titulo': 'Sistema de Tickets de Soporte',
                    'descripcion': 'Plataforma para gestionar tickets de soporte técnico con asignación automática y notificaciones.',
                    'estado': 'enviado',
                    'calificacion': None,
                    'dias_atras': 2
                },
                {
                    'estudiante': estudiantes[2],
                    'titulo': 'Blog Multi-usuario',
                    'descripcion': 'Blog colaborativo con sistema de roles, comentarios, categorías y búsqueda avanzada.',
                    'estado': 'revision',
                    'calificacion': None,
                    'dias_atras': 15
                },
            ]

            proyectos_creados = []
            for data in proyectos_data:
                fecha = timezone.now() - timedelta(days=data['dias_atras'])
                proyecto = Proyecto.objects.create(
                    estudiante=data['estudiante'],
                    titulo=data['titulo'],
                    descripcion=data['descripcion'],
                    estado=data['estado'],
                    calificacion=data['calificacion'],
                    fecha_envio=fecha
                )
                proyectos_creados.append(proyecto)
                self.stdout.write(self.style.SUCCESS(f'  ✅ Proyecto: {proyecto.titulo}'))

            # 4. Crear comentarios demo
            self.stdout.write('\n💬 Creando comentarios demo...')
            
            comentarios_data = [
                {
                    'proyecto': proyectos_creados[0],
                    'autor': docente,
                    'texto': '¡Excelente trabajo! El código está bien estructurado y sigue las mejores prácticas. La documentación es clara.',
                    'dias_atras': 28
                },
                {
                    'proyecto': proyectos_creados[0],
                    'autor': estudiantes[0],
                    'texto': 'Gracias por la retroalimentación. Implementé las sugerencias que me dio en la reunión.',
                    'dias_atras': 27
                },
                {
                    'proyecto': proyectos_creados[1],
                    'autor': docente,
                    'texto': 'Buen progreso, pero necesita más validaciones en los endpoints. Revisar autenticación JWT.',
                    'dias_atras': 9
                },
                {
                    'proyecto': proyectos_creados[2],
                    'autor': docente,
                    'texto': 'El dashboard está muy completo. Las visualizaciones son claras y responsivas.',
                    'dias_atras': 23
                },
                {
                    'proyecto': proyectos_creados[3],
                    'autor': docente,
                    'texto': 'Proyecto enviado. Pendiente revisión detallada.',
                    'dias_atras': 1
                },
                {
                    'proyecto': proyectos_creados[4],
                    'autor': docente,
                    'texto': 'El sistema de roles funciona bien. Falta implementar la búsqueda avanzada mencionada en la descripción.',
                    'dias_atras': 14
                },
                {
                    'proyecto': proyectos_creados[4],
                    'autor': estudiantes[2],
                    'texto': 'Estoy trabajando en la búsqueda avanzada. La tendré lista esta semana.',
                    'dias_atras': 13
                },
            ]

            for data in comentarios_data:
                fecha = timezone.now() - timedelta(days=data['dias_atras'])
                comentario = Comentario.objects.create(
                    proyecto=data['proyecto'],
                    autor=data['autor'],
                    texto=data['texto'],
                    fecha_creacion=fecha
                )
                self.stdout.write(self.style.SUCCESS(f'  ✅ Comentario en: {comentario.proyecto.titulo}'))

            self.stdout.write(self.style.SUCCESS('\n✅ ¡Datos de prueba creados exitosamente!'))
        else:
            self.stdout.write(self.style.WARNING('\n⚠️  Ya existen proyectos en la base de datos. No se crearon proyectos demo.'))

        # Resumen
        self.stdout.write('\n📊 Resumen:')
        self.stdout.write(f'   - Grupos: {Group.objects.count()}')
        self.stdout.write(f'   - Usuarios: {User.objects.count()}')
        self.stdout.write(f'   - Proyectos: {Proyecto.objects.count()}')
        self.stdout.write(f'   - Comentarios: {Comentario.objects.count()}')
        
        self.stdout.write(self.style.SUCCESS('\n🎉 ¡Listo! Puedes iniciar sesión con:'))
        self.stdout.write(self.style.SUCCESS('   📚 Estudiante: estudiante_demo / demo123'))
        self.stdout.write(self.style.SUCCESS('   👨‍🏫 Docente: docente_demo / demo123'))
