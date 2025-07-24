# MyDjangoProyectServer

## Requisitos previos
- Python 3.12 o superior
- MySQL Server
- Git (opcional)

## 1. Clonar el repositorio (si aplica)
```bash
git clone <url-del-repositorio>
cd MyDjangoProyectServer
```

## 2. Crear y activar un entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

## 4. Instalar y configurar MySQL

### Instalar MySQL Server
```bash
sudo apt update
sudo apt install mysql-server mysql-client
```

### Iniciar el servicio de MySQL
```bash
sudo systemctl start mysql
sudo systemctl enable mysql
```

### Configurar la base de datos y usuario
```bash
sudo mysql -u root -p
```
Dentro de la consola de MySQL:
```sql
CREATE DATABASE djagoBackend_db;
CREATE USER 'root'@'localhost' IDENTIFIED BY '627602';
GRANT ALL PRIVILEGES ON djagoBackend_db.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

> **Nota:** Si ya tienes el usuario root creado, solo asegúrate de que la contraseña coincida con la de `settings.py`.

## 5. Configuración de Django para MySQL
En `MyDjangoProyectServer/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'djagoBackend_db',
        'USER': 'root',
        'PASSWORD': '627602',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

import pymysql
pymysql.install_as_MySQLdb()
```

## 6. Migraciones y superusuario
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## 7. Ejecutar el servidor de desarrollo
```bash
python manage.py runserver
```

## 8. Acceder a la aplicación
Abre tu navegador y ve a: [http://localhost:8000/](http://localhost:8000/)

### Acceso desde otros dispositivos en la red local (IPv4)

Si quieres acceder a tu servidor Django desde otro dispositivo en la misma red, debes:

1. **Permitir conexiones externas en Django**
   - En `MyDjangoProyectServer/settings.py`, agrega tu IP local (por ejemplo, `192.168.1.10`) a la lista `ALLOWED_HOSTS`:
     ```python
     ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.1.10']
     ```

2. **Levantar el servidor en tu IP local**
   - Usa el siguiente comando para que Django escuche en todas las interfaces IPv4:
     ```bash
     python manage.py runserver 0.0.0.0:8000
     ```
   - O solo en tu IP local:
     ```bash
     python manage.py runserver 192.168.1.10:8000
     ```

3. **Acceder desde otro dispositivo**
   - En otro dispositivo conectado a la misma red WiFi/LAN, abre el navegador y entra a:
     ```
     http://192.168.1.10:8000/
     ```
   - Cambia `192.168.1.10` por la IP de tu PC si es diferente (puedes verla con `ip a` o `hostname -I`).

---

## 9. Endpoints de usuarios (API REST)

La app `users` permite el registro y login de usuarios mediante endpoints REST.

### Registro de usuario
- **URL:** `/users`
- **Método:** `POST`
- **Body (JSON):**
  ```json
  {
    "name": "Nombre",
    "lastname": "Apellido",
    "email": "correo@ejemplo.com",
    "phone": "123456789",
    "image": "url_o_texto_opcional",
    "password": "tu_contraseña",
    "notification_token": "token_opcional"
  }
  ```
- **Respuesta exitosa:**
  ```json
  {
    "id": 1,
    "name": "Nombre",
    "lastname": "Apellido",
    "email": "correo@ejemplo.com",
    "phone": "123456789",
    "image": "url_o_texto_opcional",
    "notification_token": "token_opcional"
  }
  ```

### Login de usuario
- **URL:** `/users/login`
- **Método:** `POST`
- **Body (JSON):**
  ```json
  {
    "email": "correo@ejemplo.com",
    "password": "tu_contraseña"
  }
  ```
- **Respuesta exitosa:**
  ```json
  {
    "id": 1,
    "name": "Nombre",
    "lastname": "Apellido",
    "email": "correo@ejemplo.com",
    "phone": "123456789",
    "image": "url_o_texto_opcional",
    "notification_token": "token_opcional"
  }
  ```
- **Respuesta de error:**
  ```json
  { "error": "El email o el password son incorrectos" }
  ```

### Notas sobre la API
- El password se almacena de forma segura usando bcrypt.
- El campo `image` y `notification_token` son opcionales.
- El email debe ser único.
- Todos los endpoints devuelven respuestas en formato JSON.

---

### Notas adicionales
- Si tienes problemas con `mysqlclient`, puedes usar `PyMySQL` (ya está configurado en este proyecto).
- Recuerda activar el entorno virtual cada vez que trabajes en el proyecto:
  ```bash
  source venv/bin/activate
  ```
- Para instalar dependencias adicionales, usa:
  ```bash
  pip install <paquete>
  pip freeze > requirements.txt
  ``` 