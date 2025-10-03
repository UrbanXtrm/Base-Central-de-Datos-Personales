# Base Centralizada de Datos Personales

Esta aplicación proporciona una API y una pequeña interfaz web para centralizar en una sola base de datos en la nube la información personal, médica, profesional y de seguridad social de un individuo.

## Características principales

- **Modelo unificado** para almacenar datos personales, historial médico, trayectoria educativa y profesional, y registros de seguridad social.
- **API REST** construida con [FastAPI](https://fastapi.tiangolo.com/) que permite gestionar toda la información desde aplicaciones externas.
- **Base de datos SQL** gestionada con [SQLModel](https://sqlmodel.tiangolo.com/). Por defecto utiliza SQLite, pero está lista para conectarse a motores en la nube (PostgreSQL, MySQL) cambiando la cadena de conexión.
- **Interfaz web mínima** basada en HTMX para consultar y registrar datos desde el navegador.
- **Documentación interactiva** disponible automáticamente en `/docs` y `/redoc`.

## Requisitos

- Python 3.11
- [Poetry](https://python-poetry.org/) para gestionar las dependencias (opcional pero recomendado)

## Instalación

```bash
poetry install
```

Si prefieres usar `pip`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> El archivo `requirements.txt` se puede generar con `poetry export -f requirements.txt --output requirements.txt --without-hashes`.

## Uso

1. Crea la base de datos y arranca la aplicación:

   ```bash
   poetry run uvicorn app.main:app --reload
   ```

   Por defecto la base de datos se crea en `app.db`. Para apuntar a una base de datos en la nube define la variable de entorno `DATABASE_URL`, por ejemplo:

   ```bash
   export DATABASE_URL="postgresql+psycopg2://usuario:password@host:5432/basedatos"
   ```

2. Abre `http://127.0.0.1:8000` para acceder a la interfaz web.
3. La documentación interactiva está disponible en `http://127.0.0.1:8000/docs`.

## Endpoints principales

- `GET /persons`: lista todas las personas registradas.
- `POST /persons`: crea una nueva persona.
- `PATCH /persons/{id}` / `DELETE /persons/{id}`: actualiza o elimina una persona.
- `POST /records/medical`: crea un registro médico asociado a una persona (equivalente para educación, empleo, seguridad social y documentos).
- `GET /profiles/{id}`: obtiene la ficha completa de la persona con todos los registros asociados lista para integrar con otros sistemas.

## Estructura de la base de datos

- `Person`: Datos generales de la persona.
- `MedicalRecord`: Historial médico con diagnósticos, alergias y tratamientos.
- `EducationRecord`: Formación académica y certificaciones.
- `EmploymentRecord`: Experiencia profesional y puestos desempeñados.
- `SocialSecurityRecord`: Información de seguridad social y afiliaciones.
- `Document`: Archivos de referencia como identificaciones, pólizas o títulos (solo metadatos; la subida de archivos se gestiona externamente).

## Extensión y despliegue

- Para desplegar en un servicio gestionado (Railway, Render, Fly.io, etc.) configura la variable `DATABASE_URL` con la cadena de conexión del proveedor.
- La autenticación está pensada para integrarse con un proveedor externo (OAuth, SSO). Actualmente la API asume un entorno confiable.
- Puedes ampliar el esquema de datos añadiendo nuevos modelos y relacionándolos con `Person`.

## Licencia

Esta aplicación se distribuye bajo la licencia MIT incluida en el archivo `LICENSE`.
