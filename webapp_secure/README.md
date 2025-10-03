# WebApp Segura de Datos Personales

## Configuración
1. Renombra `.env.example` a `.env` y define:
```
APP_PASSWORD=tu_contraseña_segura
SECRET_KEY=clave_fernet_generada
```

2. Instala dependencias:
```
pip install -r requirements.txt
```

3. Ejecuta localmente:
```
uvicorn main:app --reload
```

4. Despliega en Render/Railway subiendo este proyecto.

