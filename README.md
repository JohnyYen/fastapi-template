# Template de FastAPI

¡Bienvenido al template de FastAPI! Este proyecto es una plantilla base para crear APIs rápidas, escalables y mantenibles utilizando el framework **FastAPI**. Incluye una estructura organizada, configuraciones esenciales y herramientas listas para usar.

---

## 🚀 Características Principales

- **Estructura modular**: Organización clara de carpetas y archivos.
- **Autenticación JWT**: Seguridad integrada con tokens JWT.
- **Base de datos**: Configuración con **SQLAlchemy** (async) y **Alembic** para migraciones.
- **Validación de datos**: Uso de **Pydantic** para esquemas y validación.
- **Testing**: Configuración básica con **pytest**.
- **Docker**: Listo para desplegar con **Docker** y **Docker Compose**.
- **Documentación automática**: Generación de docs con **Swagger UI** y **ReDoc**.
- **CRUD completo**: Implementación base de operaciones CRUD con patrón Repository.
- **Gestión de usuarios**: Endpoints para registro, login y cambio de contraseña.

---

## 📂 Estructura del Proyecto

```
fastapi-template/
├── src/
│   ├── __init__.py
│   ├── api/                 # Endpoints de la API
│   │   ├── __init__.py
│   │   ├── v1/              # Versión 1 de la API
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/   # Definición de endpoints
│   │   │   │   ├── __init__.py
│   │   │   │   ├── user.py
│   │   │   │   ├── auth.py
│   │   │   └── routers.py   # Configuración de routers
│   ├── core/                # Configuraciones centrales
│   │   ├── __init__.py
│   │   ├── config.py        # Configuración de variables de entorno
│   │   ├── security.py      # Lógica de autenticación y seguridad
│   │   ├── deps.py          # Dependencias (get_current_user, etc)
│   │   └── exceptions.py    # Excepciones personalizadas
│   ├── models/              # Modelos de datos (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── role.py
│   ├── schemas/             # Esquemas Pydantic
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── auth.py
│   │   ├── base.py
│   ├── services/            # Lógica de negocio
│   │   ├── __init__.py
│   │   ├── user_service.py
│   ├── db/                  # Configuración de la base de datos
│   │   ├── __init__.py
│   │   ├── base.py         # Clase base de modelos
│   │   ├── session.py       # Sesión de la base de datos
│   │   └── repositories/    # Repositorios (patrón Repository)
│   │       ├── __init__.py
│   │       ├── user_repository.py
│   └── utils/               # Utilidades comunes
│       ├── __init__.py
│       └── helpers.py
├── migrations/              # Migraciones de la base de datos (Alembic)
│   ├── README
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── tests/                   # Pruebas unitarias y de integración
├── requirements.txt         # Dependencias del proyecto
├── .env.example            # Ejemplo de variables de entorno
├── .gitignore               # Archivos ignorados por Git
├── Dockerfile               # Configuración para Docker
├── docker-compose.yml       # Configuración para Docker Compose
├── alembic.ini             # Configuración de Alembic
├── main.py                  # Punto de entrada de la aplicación
└── README.md                # Documentación del proyecto
```

---

## 🛠️ Requisitos Previos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

- **Python 3.9 o superior**.
- **Pip** (gestor de paquetes de Python).
- **Docker** (opcional, para despliegue en contenedores).
- **Git** (opcional, para control de versiones).

---

## 🚀 Instalación

Sigue estos pasos para configurar el proyecto en tu máquina local:

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/fastapi-template.git
   cd fastapi-template
   ```

2. **Crea un entorno virtual** (opcional pero recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura las variables de entorno**:
   - Copia el archivo `.env.example` a `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edita `.env` y configura tus variables:
     ```plaintext
     DATABASE_URL=sqlite+aiosqlite:///./test.db
     SECRET_KEY=tu_clave_secreta_aqui
     ALGORITHM=HS256
     ACCESS_TOKEN_EXPIRE_MINUTES=30
     ```

5. **(Opcional) Configura las migraciones de base de datos con Alembic**:
   ```bash
   alembic upgrade head
   ```

6. **Inicia la aplicación**:
   ```bash
   uvicorn main:app --reload
   ```

7. **Accede a la documentación**:
   - Abre tu navegador y ve a:
     - **Swagger UI**: http://127.0.0.1:8000/docs
     - **ReDoc**: http://127.0.0.1:8000/redoc

---

## 🔐 Autenticación

La API incluye un sistema completo de autenticación basado en JWT:

### Endpoints de Autenticación

1. **Registro de usuario**: `POST /api/v1/auth/register`
   - Crea un nuevo usuario en el sistema
   - Requiere: username, email, password

2. **Inicio de sesión**: `POST /api/v1/auth/login`
   - Autentica al usuario y devuelve un token JWT
   - Requiere: email, password

3. **Cambio de contraseña**: `POST /api/v1/auth/change-password`
   - Cambia la contraseña del usuario autenticado
   - Requiere: current_password, new_password
   - Necesita token JWT válido

### Uso del Token JWT

Después de iniciar sesión, usa el token en las solicitudes protegidas:

```
Authorization: Bearer TU_TOKEN_JWT_AQUI
```

---

## 🗄️ Base de Datos

El proyecto utiliza SQLAlchemy con soporte asíncrono:

- **Motor de base de datos**: SQLite (por defecto, configurable)
- **ORM**: SQLAlchemy 2.0+
- **Migraciones**: Alembic

### Modelos Disponibles

1. **User**: Modelo de usuario con campos:
   - id (Integer, PK)
   - username (String, único)
   - email (String, único)
   - hashed_password (String)
   - is_active (Boolean)
   - created_at (DateTime)
   - updated_at (DateTime)
   - role_id (FK a Role)

2. **Role**: Modelo de roles de usuario:
   - id (Integer, PK)
   - name_role (String, único)

### Repositorios

Cada modelo tiene un repositorio asociado que implementa operaciones CRUD:

- `UserRepository`: Operaciones CRUD para usuarios
- Métodos especiales: authenticate, get_by_email, get_by_username

---

## 🔄 CRUD Base

El proyecto implementa un patrón Repository con servicios para operaciones CRUD:

### UserRepository
Implementa operaciones básicas de base de datos:
- `get_by_id()`: Obtiene usuario por ID
- `get_all()`: Obtiene lista de usuarios
- `create()`: Crea nuevo usuario
- `update()`: Actualiza usuario
- `delete()`: Eliminación suave (soft delete)
- `authenticate()`: Autenticación de usuario

### UserService
Capa de servicio que encapsula la lógica de negocio:
- `get_user_by_id()`: Obtiene usuario por ID
- `get_all_users()`: Obtiene lista de usuarios
- `create_user()`: Crea nuevo usuario
- `update_user()`: Actualiza usuario
- `delete_user()`: Elimina usuario
- `change_user_password()`: Cambia contraseña de usuario

---

## 🐳 Despliegue con Docker

Si prefieres usar Docker, sigue estos pasos:

1. **Construye la imagen**:
   ```bash
   docker build -t fastapi-template .
   ```

2. **Ejecuta el contenedor**:
   ```bash
   docker run -d -p 8000:80 fastapi-template
   ```

3. **Accede a la aplicación**:
   - Abre tu navegador y ve a http://127.0.0.1:8000.

### Docker Compose

También puedes usar docker-compose:

```bash
docker-compose up -d
```

---

## 🧪 Ejecución de Pruebas

Para ejecutar las pruebas unitarias y de integración:

1. **Instala las dependencias de testing** (si no lo has hecho):
   ```bash
   pip install -r requirements.txt
   ```

2. **Ejecuta las pruebas**:
   ```bash
   pytest
   ```

---

## 📚 Documentación Adicional

- **FastAPI Official Documentation**: https://fastapi.tiangolo.com/
- **SQLAlchemy Documentation**: https://www.sqlalchemy.org/
- **Pydantic Documentation**: https://pydantic-docs.helpmanual.io/
- **Alembic Documentation**: https://alembic.sqlalchemy.org/
- **Docker Documentation**: https://docs.docker.com/

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si encuentras un error o tienes una sugerencia, abre un **issue** o envía un **pull request**.

1. Haz un **fork** del repositorio.
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`).
3. Haz commit de tus cambios (`git commit -m 'Agrega nueva funcionalidad'`).
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un **pull request**.

---

## 📄 Licencia

Este proyecto está bajo la licencia **MIT**. Para más detalles, consulta el archivo [LICENSE](LICENSE).

---

## ✨ Créditos

- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLAlchemy**: https://www.sqlalchemy.org/
- **Pydantic**: https://pydantic-docs.helpmanual.io/

---

¡Gracias por usar este template! Si tienes alguna pregunta, no dudes en contactarme. 🚀