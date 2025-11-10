# 🎓 ProgreS.O.S. - Sistema de Seguimiento de Proyectos Académicos

**Autores:** David Rump & Nicolás Garcia  
**Proyecto:** Examen Final - Electiva Django 2025  
**Fecha:** Noviembre 2025

---

## 📋 Descripción

ProgreS.O.S. (Progress Student Operating System) es un sistema web completo para la gestión de proyectos académicos. Permite a estudiantes enviar sus proyectos con documentación adjunta, y a docentes revisarlos, calificarlos y aprobarlos con un sistema de comentarios que envía notificaciones por email automáticamente.

### ✨ Características Principales

#### 🔐 **Autenticación y Permisos**
- Sistema de login/logout integrado con Django
- Dos roles: **Estudiante** y **Docente**
- Permisos granulares por grupo de usuario
- Perfil de usuario personalizado

#### 📁 **Gestión Completa de Proyectos**
- **Estudiantes:** Crear, editar, eliminar y enviar proyectos
- **Docentes:** Revisar, calificar (0-5), aprobar/rechazar
- Estados: Borrador, Enviado, En Revisión, Aprobado, Rechazado
- Carga de documentos (PDF, DOC, DOCX)

#### 💬 **Sistema de Comentarios con Notificaciones**
- Comentarios en tiempo real entre docente y estudiante
- **Notificaciones automáticas por email** cuando se recibe un comentario
- Emails con plantillas HTML elegantes
- Bloqueados automáticamente cuando el proyecto es aprobado

#### 📊 **Dashboard y Métricas**
- Promedio automático por estudiante
- Excluye proyectos sin calificar
- Dashboard docente con estadísticas completas
- Perfil estudiante con historial de proyectos

#### 📤 **Exportación de Datos**
- Exportar proyectos a **CSV**
- Generar reportes en **PDF** profesionales
- Filtros avanzados por estado, estudiante y fecha

#### 🔌 **API REST Completa**
- **Swagger UI** con documentación interactiva
- Endpoints para proyectos, comentarios y usuarios
- Autenticación por sesión de Django
- Permisos según rol (estudiante/docente)

#### 🎨 **Diseño Moderno y Responsivo**
- Paleta de colores rojiza elegante (#8B1E3F)
- Hover effects y animaciones suaves
- Iconos Font Awesome 6
- Mobile-first: optimizado para móviles y tablets
- Bootstrap 5 + CSS personalizado

---

## 🚀 Instalación y Configuración

### Requisitos Previos

- Python 3.11+
- pip
- virtualenv

### 1. Clonar/Descargar el Proyecto

```bash
cd ProgreS.O.S
```

### 2. Crear y Activar Entorno Virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**requirements.txt:**
```
Django==5.0
django-crispy-forms==2.1
crispy-bootstrap5==2.0.0
djangorestframework==3.14.0
drf-yasg==1.21.7
weasyprint==60.1
Pillow==10.1.0
pytest==7.4.3
pytest-django==4.7.0
pytest-cov==4.1.0
black==23.12.0
isort==5.13.2
flake8==6.1.0
```

### 4. Configurar Base de Datos

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear Datos de Prueba (Automático)

**Comando mágico que crea todo:**
```bash
python manage.py seed_data
```

Este comando crea automáticamente:
- ✅ Grupos (Estudiante y Docente)
- ✅ 3 estudiantes demo (estudiante_demo, maria_garcia, carlos_lopez)
- ✅ 1 docente demo (docente_demo)
- ✅ 5 proyectos de ejemplo
- ✅ 7 comentarios distribuidos

**Credenciales de acceso:**
```
📚 Estudiantes:
   - estudiante_demo / demo123 (Juan Pérez)
   - maria_garcia / demo123 (María García)
   - carlos_lopez / demo123 (Carlos López)

👨‍🏫 Docente:
   - docente_demo / demo123 (Prof. González)
```

### 6. Ejecutar Servidor

```bash
python manage.py runserver
```

**URLs principales:**
- 🏠 Home: http://127.0.0.1:8000/
- 🔐 Login: http://127.0.0.1:8000/accounts/login/
- 📁 Proyectos: http://127.0.0.1:8000/projects/
- 📊 Dashboard: http://127.0.0.1:8000/accounts/dashboard/
- 📖 API Docs: http://127.0.0.1:8000/api/docs/
- ⚙️ Admin: http://127.0.0.1:8000/admin/

---

## 📁 Estructura del Proyecto

```
ProgreS.O.S/
├── config/                    # Configuración Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── core/                      # App núcleo
│   ├── services/
│   │   └── email_service.py   # Servicio de emails (SOLID)
│   └── utils.py
│
├── accounts/                  # Autenticación y usuarios
│   ├── services/
│   │   └── student_metrics_service.py  # Cálculo de promedios
│   ├── templates/accounts/
│   ├── views.py
│   └── urls.py
│
├── projects/                  # Gestión de proyectos
│   ├── services/
│   │   └── project_service.py  # Lógica de negocio
│   ├── templates/projects/
│   ├── models.py              # Modelo Proyecto
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   ├── api_urls.py            # Endpoints REST
│   └── serializers.py
│
├── comments/                  # Sistema de comentarios
│   ├── services/
│   │   └── comment_service.py
│   ├── templates/comments/
│   ├── models.py              # Modelo Comentario
│   ├── forms.py
│   ├── views.py
│   └── urls.py
│
├── static/                    # Archivos estáticos
│   ├── css/
│   │   └── main.css           # Estética rojiza
│   ├── js/
│   └── images/
│       └── favicon.ico
│
├── media/                     # Archivos subidos
│   └── proyectos/
│
├── templates/                 # Templates globales
│   ├── base.html              # Template base
│   ├── home.html
│   └── emails/
│       ├── comment_created.html
│       └── comment_created.txt
│
├── tests/                     # Tests con pytest
│   ├── test_projects.py
│   ├── test_comments.py
│   └── test_metrics.py
│
├── fixtures/                  # Datos iniciales
│   └── initial_data.json
│
├── manage.py
├── requirements.txt
├── .gitignore
├── pytest.ini
├── .flake8
└── README.md
```

---

## 🎨 Arquitectura SOLID

### 1. Single Responsibility Principle (SRP)
- **ProjectService**: solo lógica de proyectos
- **CommentService**: solo lógica de comentarios
- **StudentMetricsService**: solo cálculo de métricas
- **EmailService**: solo envío de emails

### 2. Open/Closed Principle (OCP)
- Servicios extensibles sin modificar código existente
- Nuevas exportaciones (Excel, JSON) sin cambiar clases

### 3. Liskov Substitution Principle (LSP)
- `EmailService` es interfaz abstracta
- `ConsoleEmailService` y `SMTPEmailService` son intercambiables

### 4. Interface Segregation Principle (ISP)
- Interfaces pequeñas y específicas
- No métodos innecesarios en servicios

### 5. Dependency Inversion Principle (DIP)
- Vistas dependen de interfaces (`EmailService`), no de implementaciones
- Inyección de dependencias via settings

---

## 🔐 Roles y Permisos

### Estudiante
- ✅ Ver solo sus proyectos
- ✅ Crear nuevos proyectos
- ✅ Editar proyectos (si no están aprobados)
- ✅ Eliminar proyectos (si no están aprobados)
- ✅ Comentar en proyectos (si no están aprobados)
- ✅ Ver su promedio de calificaciones
- ❌ No puede cambiar estados ni calificar

### Docente
- ✅ Ver todos los proyectos
- ✅ Filtrar por estado y estudiante
- ✅ Cambiar estado de proyectos
- ✅ Asignar calificaciones
- ✅ Comentar en cualquier proyecto
- ✅ Ver métricas de todos los estudiantes
- ✅ Exportar datos (CSV/PDF)
- ❌ No puede crear proyectos

---

## 📊 Flujo de Estados

```
┌─────────┐        ┌──────────┐        ┌──────────┐
│ ENVIADO │───────▶│ REVISIÓN │───────▶│ APROBADO │
└─────────┘        └──────────┘        └──────────┘
     │                  │                    │
     └──────────────────┴────────────────────┘
          Permite comentarios         🔒 Bloqueado
```

1. **Enviado**: Estado inicial al crear proyecto
2. **Revisión**: Docente está revisando (permite comentarios)
3. **Aprobado**: Proyecto aprobado (bloquea nuevos comentarios)

---

## 📧 Sistema de Correos Electrónicos

### ¿Cómo Funciona?

El sistema envía **emails automáticos** cuando alguien comenta en un proyecto. Es como WhatsApp pero con emails.

#### 🔄 Flujo Completo:

1. **Docente comenta** en el proyecto de un estudiante
2. El sistema **detecta automáticamente** que hay un comentario nuevo
3. Se **genera un email HTML elegante** con el comentario
4. El email se **envía automáticamente** al estudiante
5. El estudiante **recibe notificación** en su correo

### 🛠️ Configuración Actual (Desarrollo)

**Ahora mismo el sistema está configurado para DESARROLLO:**

```python
# En .env (archivo que acabas de crear)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

**¿Qué significa esto?**
- ✅ Los emails NO se envían a correos reales
- ✅ Los emails se **muestran en la terminal** (consola)
- ✅ Perfecto para desarrollo y pruebas
- ✅ No necesitas configurar nada más

**Ejemplo de lo que verás en la terminal:**
```
--------------------------------------------------
Subject: Nuevo comentario en tu proyecto: Mi Proyecto
From: noreply@progresos.edu.co
To: estudiante@demo.com
--------------------------------------------------

[HTML del email con el comentario]

✅ Email enviado a estudiante@demo.com
--------------------------------------------------
```

### 📬 Configuración para Producción (Emails Reales)

**Cuando quieras enviar emails REALES a Gmail:**

#### Paso 1: Configurar Gmail
1. Ve a tu cuenta de Google
2. Activa **verificación en 2 pasos** (obligatorio)
3. Ve a https://myaccount.google.com/apppasswords
4. Crea una contraseña de aplicación para "Correo"
5. Google te dará un código de 16 caracteres (ejemplo: `abcd efgh ijkl mnop`)

#### Paso 2: Editar el archivo `.env`
```bash
# Comenta esta línea (agregar # al inicio):
# EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Descomenta y completa estas líneas (quitar el #):
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
DEFAULT_FROM_EMAIL=ProgreS.O.S. <tu-email@gmail.com>
```

#### Paso 3: Reiniciar el servidor
```bash
# Ctrl+C para detener
python manage.py runserver
```

**¡Listo!** Ahora los emails se enviarán a correos reales.

### 📝 Plantillas de Email

El sistema tiene 2 plantillas HTML elegantes:

1. **`comment_created.html`** - Se envía cuando hay un comentario nuevo
   - Muestra quién comentó
   - El texto del comentario
   - Link al proyecto

2. **`project_created.html`** - Se envía cuando se crea un proyecto
   - Título y descripción del proyecto
   - Estado inicial

**Diseño:**
- 🎨 Colores rojizos del proyecto
- 📱 Responsive (se ve bien en móvil)
- ✨ HTML profesional

### 🧪 Probar el Sistema de Emails

```bash
# 1. Inicia sesión como docente_demo / demo123
# 2. Ve a cualquier proyecto
# 3. Agrega un comentario
# 4. Mira la TERMINAL donde corre el servidor
# 5. Verás el email completo que se "envió"
```

### ❓ Preguntas Frecuentes

**Q: ¿Por qué no veo emails en mi bandeja?**  
A: Porque está en modo desarrollo (consola). Los emails solo se muestran en la terminal.

**Q: ¿Cómo envío emails reales?**  
A: Sigue los pasos de "Configuración para Producción" arriba.

**Q: ¿Puedo usar otro servicio que no sea Gmail?**  
A: Sí, solo cambia `EMAIL_HOST` y el puerto. Por ejemplo Outlook: `smtp-mail.outlook.com:587`

**Q: ¿Los estudiantes reciben notificación también?**  
A: Sí, cuando un docente comenta, el estudiante recibe email. Y viceversa.

---

## 🧪 Testing

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Con cobertura
pytest --cov=projects --cov=comments --cov=accounts

# Tests específicos
pytest tests/test_projects.py
pytest tests/test_comments.py -v
```

---

## 📡 API REST (Swagger)

### 📖 Acceder a la Documentación

**Swagger UI (Interactivo):** http://127.0.0.1:8000/api/docs/

### 🔌 Endpoints Disponibles

#### Proyectos (`/api/proyectos/`)
```
GET    /api/proyectos/                    Lista todos los proyectos
POST   /api/proyectos/                    Crear nuevo proyecto
GET    /api/proyectos/{id}/               Ver detalle de proyecto
PUT    /api/proyectos/{id}/               Actualizar proyecto completo
PATCH  /api/proyectos/{id}/               Actualizar proyecto parcial
DELETE /api/proyectos/{id}/               Eliminar proyecto
POST   /api/proyectos/{id}/calificar/     Calificar (solo docente)
GET    /api/proyectos/mis_proyectos/      Proyectos del usuario actual
```

#### Comentarios (`/api/comentarios/`)
```
GET    /api/comentarios/                  Lista todos los comentarios
POST   /api/comentarios/                  Crear comentario
GET    /api/comentarios/{id}/             Ver detalle
PUT    /api/comentarios/{id}/             Actualizar comentario
DELETE /api/comentarios/{id}/             Eliminar comentario
GET    /api/comentarios/proyecto/?proyecto_id=1  Comentarios de un proyecto
```

#### Usuarios (`/api/usuarios/`)
```
GET    /api/usuarios/                     Lista usuarios
GET    /api/usuarios/{id}/                Ver perfil de usuario
GET    /api/usuarios/me/                  Mi perfil
```

### 🔐 Autenticación

La API usa **autenticación por sesión de Django**. 

**Para probar en Swagger:**
1. Abre http://127.0.0.1:8000/api/docs/
2. Haz clic en "Authorize" (arriba a la derecha)
3. Si ya estás logueado en Django, puedes probar directamente
4. Si no, inicia sesión en http://127.0.0.1:8000/accounts/login/

**Ejemplo con Python:**
```python
import requests

# Login primero
session = requests.Session()
session.post('http://127.0.0.1:8000/accounts/login/', data={
    'username': 'estudiante_demo',
    'password': 'demo123'
})

# Usar la API
response = session.get('http://127.0.0.1:8000/api/proyectos/')
proyectos = response.json()
print(proyectos)
```

---

## 📤 Exportaciones

### CSV
- **Proyectos**: `/projects/export/csv/`
- **Métricas**: `/accounts/metrics/export/csv/`

### PDF
- **Proyectos**: `/projects/export/pdf/`
- **Métricas**: `/accounts/metrics/export/pdf/`

Los archivos se descargan automáticamente con nombres descriptivos.

---

## 🎨 Personalización de Estilos

### Paleta de Colores (Rojiza Elegante)

```css
:root {
  --primary: #8B1E3F;        /* Rojo burdeos principal */
  --primary-accent: #B23A48; /* Rojo claro acento */
  --bg-light: #FAF7F8;       /* Fondo claro */
  --neutral-600: #6C757D;    /* Gris neutro */
  --neutral-100: #F1F3F5;    /* Gris muy claro */
}
```

### Modificar Estilos

Editar `static/css/main.css` para personalizar:
- Colores de botones y badges
- Tipografía (Inter, Lora)
- Espaciado y componentes

---

## 📱 Optimización Mobile

### Dispositivos Objetivo
- **Galaxy S24**: 412x915 px
- **iPhone 13/14/15**: 390x844 px

### Características Mobile-First
- ✅ Navegación colapsable
- ✅ Tablas responsive con scroll horizontal
- ✅ Cards apiladas en una columna
- ✅ Botones táctiles ≥44px
- ✅ Formularios optimizados
- ✅ Imágenes y documentos escalables

### Probar en Móvil

**Chrome DevTools:**
1. F12 → Toggle device toolbar
2. Seleccionar "Galaxy S24" o "iPhone 14 Pro"
3. Navegar por la aplicación

---

## 🔧 Configuración de Producción

### Variables de Entorno

Crear archivo `.env`:
```
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=progresos.com,www.progresos.com
DATABASE_URL=postgres://user:pass@localhost/progresos
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Comandos para Deploy

```bash
# Colectar archivos estáticos
python manage.py collectstatic --noinput

# Migrar base de datos
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar con Gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

---

## 📝 Uso del Sistema

### Como Estudiante

1. **Login** con credenciales de estudiante
2. **Dashboard**: ver resumen y promedio general
3. **Mis Proyectos**: crear, editar, eliminar proyectos
4. **Detalle**: ver comentarios del docente
5. **Comentar**: responder retroalimentación (si no está aprobado)

### Como Docente

1. **Login** con credenciales de docente
2. **Dashboard**: ver estadísticas y promedios de estudiantes
3. **Proyectos**: filtrar por estado/estudiante
4. **Revisar**: cambiar estado y asignar calificación
5. **Comentar**: dar retroalimentación
6. **Exportar**: descargar datos en CSV o PDF

---

## 🐛 Troubleshooting

### Problema: Error al migrar base de datos
```bash
# Eliminar migraciones y base de datos
rm db.sqlite3
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Recrear
python manage.py makemigrations
python manage.py migrate
```

### Problema: Archivos estáticos no cargan
```bash
# Verificar configuración
python manage.py collectstatic

# En desarrollo
DEBUG = True  # en settings.py
```

### Problema: Email no se envía
- Verificar `EMAIL_BACKEND` en settings.py
- En desarrollo usa `console.EmailBackend` (imprime en terminal)
- Verificar que el estudiante tenga email configurado

### Problema: No puedo acceder a /admin/
```bash
# Crear superusuario
python manage.py createsuperuser
```

---

## 📚 Recursos Adicionales

- **Django Docs**: https://docs.djangoproject.com/
- **DRF Docs**: https://www.django-rest-framework.org/
- **Bootstrap 5**: https://getbootstrap.com/docs/5.0/
- **WeasyPrint**: https://weasyprint.org/

---

## ✅ Checklist de Funcionalidades

### Core Features
- [x] Sistema de autenticación (Login/Logout)
- [x] Roles: Estudiante y Docente
- [x] CRUD completo de proyectos
- [x] Sistema de comentarios
- [x] **Notificaciones por email automáticas**
- [x] Dashboard con métricas
- [x] Cálculo de promedios por estudiante
- [x] Filtrado y búsqueda de proyectos
- [x] Estados de proyecto (Borrador → Enviado → Revisión → Aprobado)

### Extras Implementados
- [x] API REST completa con Django REST Framework
- [x] Documentación Swagger/OpenAPI interactiva
- [x] Exportación a CSV y PDF
- [x] Diseño responsive mobile-first
- [x] Paleta de colores personalizada (rojiza elegante)
- [x] Iconos Font Awesome
- [x] Hover effects y animaciones CSS
- [x] Plantillas de email HTML profesionales
- [x] Command `seed_data` para datos de prueba
- [x] Permisos granulares por grupo
- [x] Validaciones de formularios
- [x] Manejo de archivos (documentos PDF/DOC)

---

## 🚀 Comandos Rápidos

```bash
# Iniciar proyecto desde cero
python manage.py migrate
python manage.py seed_data
python manage.py runserver

# Crear backup de datos
python manage.py dumpdata > backup.json

# Restaurar datos
python manage.py loaddata backup.json
```

---

## 👥 Autores

**David Rump & Nicolás Garcia**

Proyecto desarrollado para la Electiva de Django 2025

---

## 📄 Licencia

Proyecto académico - Examen Final Electiva Django 2025

---

## 🎉 Estado del Proyecto

✅ **PROYECTO 100% COMPLETO Y FUNCIONAL**

- ✅ Todas las funcionalidades core implementadas
- ✅ Diseño pulido y profesional
- ✅ API REST documentada con Swagger
- ✅ Sistema de emails configurado (desarrollo y producción)
- ✅ Datos de prueba listos (`seed_data`)
- ✅ README completo y detallado

**¡Listo para presentar y defender! 🎓**

---


### Extras Implementados
- ✅ API REST con Swagger
- ✅ Cálculo de promedios por estudiante
- ✅ Arquitectura SOLID
- ✅ Tests con pytest
- ✅ Mobile-first design
- ✅ Exportación CSV/PDF
- ✅ Sistema de comentarios con emails
- ✅ Caché para optimización

---

**¡Proyecto listo para presentar! 🎉**