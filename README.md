# Template de FastAPI

¡Bienvenido al template de FastAPI! Este proyecto es una plantilla base para crear APIs rápidas, escalables y mantenibles utilizando el framework **FastAPI**. Incluye una estructura organizada, configuraciones esenciales y herramientas listas para usar.

---

## 🚀 Características Principales

- **Estructura modular**: Organización clara de carpetas y archivos.
- **Autenticación JWT**: Seguridad integrada con tokens JWT.
- **Base de datos**: Configuración con **SQLAlchemy** y **Alembic** para migraciones.
- **Validación de datos**: Uso de **Pydantic** para esquemas y validación.
- **Testing**: Configuración básica con **pytest**.
- **Docker**: Listo para desplegar con **Docker** y **Docker Compose**.
- **Documentación automática**: Generación de docs con **Swagger UI** y **ReDoc**.

---

## 📂 Estructura del Proyecto

```
my_fastapi_project/
├── src/
│   ├── __init__.py
│   ├── api/                 # Endpoints de la API
│   │   ├── __init__.py
│   │   ├── v1/              # Versión 1 de la API
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/   # Definición de endpoints
│   │   │   │   ├── __init__.py
│   │   │   │   ├── users.py
│   │   │   └── routers.py   # Configuración de routers
│   ├── core/                # Configuraciones centrales
│   │   ├── __init__.py
│   │   ├── config.py        # Configuración de variables de entorno
│   │   └── security.py      # Lógica de autenticación y seguridad
│   ├── models/              # Modelos de datos (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── user.py
│   ├── schemas/             # Esquemas Pydantic
│   │   ├── __init__.py
│   │   ├── user.py
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
├── tests/                   # Pruebas unitarias y de integración
│   ├── __init__.py
│   ├── test_users.py
├── migrations/              # Migraciones de la base de datos (Alembic)
├── requirements.txt         # Dependencias del proyecto
├── .env                     # Variables de entorno
├── .gitignore               # Archivos ignorados por Git
├── Dockerfile               # Configuración para Docker
|── main.py                  # Punto de entrada de la aplicación
└── README.md                # Documentación del proyecto
```

---

## 🛠️ Configuración

### Variables de Entorno

El proyecto utiliza variables de entorno para configurar diferentes aspectos del proyecto. Estas variables se encuentran en el archivo `.env`:

```
# Configuración de la base de datos
DB_HOST=localhost
DB_PORT=5432
DB_NAME=my_database
DB_USER=my_user
DB_PASSWORD=my_password
```

### Dependencias

El proyecto utiliza las siguientes dependencias:

-
├── docker-compose.yml       # Configuración para Docker Compose
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
   git clone https://github.com/tu-usuario/mi-proyecto-fastapi.git
   cd mi-proyecto-fastapi
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
   - Crea un archivo `.env` en la raíz del proyecto.
   - Agrega las siguientes variables:
     ```plaintext
     DATABASE_URL=sqlite:///./test.db
     SECRET_KEY=my-secret-key
     ALGORITHM=HS256
     ACCESS_TOKEN_EXPIRE_MINUTES=30
     ```

5. **Ejecuta las migraciones** (si usas Alembic):
   ```bash
   alembic upgrade head
   ```

6. **Inicia la aplicación**:
   ```bash
   uvicorn app.main:app --reload
   ```

7. **Accede a la documentación**:
   - Abre tu navegador y ve a:
     - **Swagger UI**: http://127.0.0.1:8000/docs
     - **ReDoc**: http://127.0.0.1:8000/redoc

---

## 🐳 Despliegue con Docker

Si prefieres usar Docker, sigue estos pasos:

1. **Construye la imagen**:
   ```bash
   docker build -t mi-proyecto-fastapi .
   ```

2. **Ejecuta el contenedor**:
   ```bash
   docker run -d -p 8000:80 mi-proyecto-fastapi
   ```

3. **Accede a la aplicación**:
   - Abre tu navegador y ve a http://127.0.0.1:8000.

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