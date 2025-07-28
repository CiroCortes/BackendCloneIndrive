# MyDjangoProyectServer

Backend API REST desarrollado en Django con autenticación JWT, sistema de roles y gestión de usuarios.

## 🚀 Características

- **Autenticación JWT** con tokens personalizados
- **Sistema de roles** (CLIENT, ADMIN, etc.)
- **API REST** completa para gestión de usuarios
- **Subida de imágenes** con almacenamiento local
- **Base de datos MySQL** con PyMySQL
- **Protección de rutas** con permisos personalizados
- **Validación de contraseñas** con bcrypt

## 📋 Requisitos previos

- Python 3.12 o superior
- MySQL Server 8.0+
- Git (opcional)

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd MyDjangoProyectServer
```

### 2. Crear y activar entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar MySQL

#### Instalar MySQL Server
```bash
sudo apt update
sudo apt install mysql-server mysql-client
```

#### Iniciar el servicio
```bash
sudo systemctl start mysql
sudo systemctl enable mysql
```

#### Configurar base de datos
```bash
sudo mysql -u root -p
```

Dentro de MySQL:
```sql
CREATE DATABASE djagoBackend_db;
CREATE USER 'root'@'localhost' IDENTIFIED BY '627602';
GRANT ALL PRIVILEGES ON djagoBackend_db.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 5. Configurar variables de entorno

En `MyDjangoProyectServer/settings.py`:
```python
GLOBAL_IP = '192.168.1.10'  # Tu IP local
GLOBAL_HOST = '3000'         # Puerto del servidor
ALLOWED_HOSTS = [GLOBAL_IP]
```

### 6. Ejecutar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Crear roles iniciales
```bash
python manage.py shell
```

En el shell de Django:
```python
from roles.models import Role
Role.objects.create(id='CLIENT', name='Cliente', image='client.png', route='/client')
Role.objects.create(id='ADMIN', name='Administrador', image='admin.png', route='/admin')
exit()
```

### 8. Ejecutar el servidor
```bash
python manage.py runserver 192.168.1.10:3000
```

## 📁 Estructura del proyecto

```
MyDjangoProyectServer/
├── authentication/          # Autenticación JWT
│   ├── views.py            # Login y registro
│   ├── urls.py             # Rutas de auth
│   └── customJWTAuthentication.py  # Autenticador personalizado
├── users/                   # Gestión de usuarios
│   ├── models.py           # Modelo User personalizado
│   ├── views.py            # CRUD de usuarios
│   ├── urls.py             # Rutas de usuarios
│   └── serializers.py      # Serializadores
├── roles/                   # Sistema de roles
│   ├── models.py           # Modelo Role
│   └── serializers.py      # Serializadores de roles
├── MyDjangoProyectServer/   # Configuración principal
│   ├── settings.py         # Configuración Django
│   └── urls.py             # URLs principales
└── media/                   # Archivos subidos
```

## 🔐 Autenticación JWT

### Configuración
- **Access Token:** 3 horas
- **Refresh Token:** 1 día
- **Algoritmo:** HS256
- **Header:** Bearer

### Flujo de autenticación
1. **Registro:** POST `/auth/register`
2. **Login:** POST `/auth/login`
3. **Usar token:** Incluir `Authorization: Bearer <token>` en headers

## 📡 API Endpoints

### 🔑 Autenticación

#### Registro de usuario
- **URL:** `POST /auth/register`
- **Body:**
```json
{
    "name": "Juan",
    "lastname": "Pérez",
    "email": "juan@ejemplo.com",
    "phone": "123456789",
    "password": "contraseña123",
    "image": "url_opcional",
    "notification_token": "token_opcional"
}
```
- **Respuesta:**
```json
{
    "user": {
        "id": 1,
        "name": "Juan",
        "lastname": "Pérez",
        "email": "juan@ejemplo.com",
        "phone": "123456789",
        "image": "http://192.168.1.10:3000/media/uploads/users/1/imagen.jpg",
        "notification_token": "token_opcional",
        "roles": [{"id": "CLIENT", "name": "Cliente"}]
    },
    "token": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Login de usuario
- **URL:** `POST /auth/login`
- **Body:**
```json
{
    "email": "juan@ejemplo.com",
    "password": "contraseña123"
}
```
- **Respuesta:** Igual que registro

### 👥 Gestión de usuarios

#### Obtener todos los usuarios
- **URL:** `GET /users/`
- **Headers:** `Authorization: Bearer <token>`
- **Respuesta:**
```json
[
    {
        "id": 1,
        "name": "Juan",
        "lastname": "Pérez",
        "email": "juan@ejemplo.com",
        "phone": "123456789",
        "image": "http://192.168.1.10:3000/media/uploads/users/1/imagen.jpg",
        "notification_token": "token_opcional",
        "roles": [{"id": "CLIENT", "name": "Cliente"}]
    }
]
```

#### Obtener usuario por ID
- **URL:** `GET /users/findById/<id>`
- **Headers:** `Authorization: Bearer <token>`
- **Respuesta:** Objeto usuario individual

#### Actualizar usuario
- **URL:** `PUT /users/<id>`
- **Headers:** `Authorization: Bearer <token>`
- **Body:**
```json
{
    "name": "Juan Carlos",
    "lastname": "Pérez López",
    "phone": "987654321"
}
```
- **Nota:** Solo el propio usuario puede actualizarse

#### Actualizar usuario con imagen
- **URL:** `PUT /users/upload/<id>`
- **Headers:** `Authorization: Bearer <token>`
- **Body:** `multipart/form-data`
  - `file`: Archivo de imagen
  - `name`, `lastname`, `phone`: Campos opcionales

## 🔒 Seguridad

### Protección de rutas
- **Rutas públicas:** `/auth/register`, `/auth/login`
- **Rutas protegidas:** Todas las demás requieren token JWT
- **Validación de permisos:** Usuarios solo pueden modificar su propio perfil

### Encriptación
- **Contraseñas:** Encriptadas con bcrypt
- **Tokens:** Firmados con HS256
- **Base de datos:** Conexión segura con MySQL

## 🗄️ Base de datos

### Modelos principales

#### User
```python
- id (AutoField, PK)
- name (CharField)
- lastname (CharField)
- email (EmailField, unique)
- phone (CharField)
- image (CharField, nullable)
- password (CharField, bcrypt)
- notification_token (CharField, nullable)
- created_at (DateTimeField)
- updated_at (DateTimeField)
- roles (ManyToManyField -> Role)
```

#### Role
```python
- id (CharField, PK)
- name (CharField, unique)
- image (CharField)
- route (CharField)
- created_at (DateTimeField)
- updated_at (DateTimeField)
```

#### UserHasRole (Tabla pivote)
```python
- id_user (ForeignKey -> User)
- id_rol (ForeignKey -> Role)
- unique_together: (id_user, id_rol)
```

## 🚀 Despliegue

### Variables de entorno
```python
# settings.py
GLOBAL_IP = '192.168.1.10'  # Tu IP
GLOBAL_HOST = '3000'         # Puerto
ALLOWED_HOSTS = [GLOBAL_IP]
```

### Comando de inicio
```bash
python manage.py runserver 192.168.1.10:3000
```

### Acceso desde red local
- **URL:** `http://192.168.1.10:3000`
- **API:** `http://192.168.1.10:3000/users/`
- **Admin:** `http://192.168.1.10:3000/admin/`

## 🛠️ Desarrollo

### Comandos útiles
```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Shell de Django
python manage.py shell

# Verificar sintaxis
python manage.py check
```

### Estructura de archivos de imagen
```
media/
└── uploads/
    └── users/
        └── <user_id>/
            └── <filename>
```

## 📝 Notas importantes

- **Tokens JWT:** Se generan automáticamente en login/registro
- **Imágenes:** Se almacenan en `media/uploads/users/<id>/`
- **Roles:** Se asignan automáticamente (CLIENT) en registro
- **Validación:** Emails únicos, contraseñas encriptadas
- **CORS:** Configurado para desarrollo local

## 🔧 Solución de problemas

### Error de conexión MySQL
```bash
sudo systemctl status mysql
sudo mysql_secure_installation
```

### Error de migraciones
```bash
python manage.py makemigrations --empty users
python manage.py migrate --fake-initial
```

### Error de permisos
```bash
sudo chown -R $USER:$USER media/
chmod -R 755 media/
```

---

**Desarrollado con Django 4.2.11 y Django REST Framework 3.14.0** 