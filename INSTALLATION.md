# Guía de Instalación y Configuración

## Prerrequisitos

### Software Requerido
- **Python 3.8+** (recomendado 3.11)
- **Node.js 16+** y npm
- **Git**
- **Visual Studio Code** (recomendado)

### Cuentas y Claves API (Opcional)
- **NASA API Key**: Obtener en [https://api.nasa.gov](https://api.nasa.gov) (opcional, se puede usar DEMO_KEY)

## Instalación Paso a Paso

### 1. Clonar el Repositorio

```bash
git clone https://github.com/MiguelGavito/HackNasa_Eq42.git
cd HackNasa_Eq42
```

### 2. Configurar el Backend (Python/FastAPI)

```bash
# Navegar a la carpeta backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
copy ..\\.env.example .env
# Editar .env con tus configuraciones
```

### 3. Configurar el Frontend (React)

```bash
# Navegar a la carpeta frontend
cd ../frontend

# Instalar dependencias
npm install

# Crear archivo de configuración local (opcional)
echo "REACT_APP_API_URL=http://localhost:8000" > .env.local
```

### 4. Configurar Base de Datos (Opcional)

Por defecto, la aplicación usa SQLite. Para desarrollo, esto es suficiente.

```bash
# Crear base de datos (se crea automáticamente al ejecutar)
cd ../backend
python -c "from app import app; print('Base de datos inicializada')"
```

## Ejecución de la Aplicación

### Ejecutar Backend

```bash
cd backend
# Asegurarse de que el entorno virtual esté activado
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Ejecutar servidor
python app.py
```

El backend estará disponible en: `http://localhost:8000`
Documentación de la API: `http://localhost:8000/docs`

### Ejecutar Frontend

```bash
# En una nueva terminal
cd frontend
npm start
```

El frontend estará disponible en: `http://localhost:3000`

## Verificación de la Instalación

### 1. Verificar Backend
```bash
curl http://localhost:8000/
# Debería retornar: {"message": "Meteor Madness API - NASA Hackathon 2025"}

curl http://localhost:8000/api/asteroids
# Debería retornar la lista de asteroides de ejemplo
```

### 2. Verificar Frontend
- Abrir `http://localhost:3000` en el navegador
- Deberías ver la página principal de Meteor Madness
- Navegar a "Simulación" y verificar que carga correctamente

### 3. Verificar Integración
- En la página de simulación, seleccionar un asteroide
- Configurar parámetros y ejecutar simulación
- Verificar que se muestran los resultados

## Configuración Avanzada

### Variables de Entorno

Editar el archivo `.env` en la carpeta backend:

```env
# API Keys
NASA_API_KEY=tu_api_key_aquí  # Obtener en api.nasa.gov

# Base de datos
DATABASE_URL=sqlite:///meteor_madness.db

# Servidor
HOST=0.0.0.0
PORT=8000
DEBUG=True

# CORS
CORS_ORIGINS=http://localhost:3000
```

### Configuración de Datos Reales de NASA

Para usar datos reales en lugar de datos de ejemplo:

1. Obtener API key de NASA en [https://api.nasa.gov](https://api.nasa.gov)
2. Configurar `NASA_API_KEY` en el archivo `.env`
3. Modificar `backend/app.py` para usar el servicio de NASA:

```python
# En backend/app.py, agregar:
from services.nasa_api import get_nasa_asteroids

@app.get("/api/asteroids/live")
async def get_live_asteroids():
    """Obtener asteroides reales de NASA"""
    return get_nasa_asteroids()
```

## Solución de Problemas

### Error: "ModuleNotFoundError"
```bash
# Asegurarse de que el entorno virtual esté activado
cd backend
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Error: "CORS"
- Verificar que el frontend esté corriendo en `http://localhost:3000`
- Verificar configuración de CORS en `backend/app.py`

### Error: "Port already in use"
```bash
# Cambiar puerto del backend
export PORT=8001  # macOS/Linux
set PORT=8001     # Windows

# O cambiar en el código app.py:
# uvicorn.run(app, host="0.0.0.0", port=8001)
```

### Frontend no conecta con Backend
- Verificar que ambos servidores estén corriendo
- Verificar URL en `frontend/src/services/api.js`
- Revisar consola del navegador para errores

## Desarrollo

### Estructura de Desarrollo
```
meteor-madness/
├── backend/        # Desarrollo de API y simulaciones
├── frontend/       # Desarrollo de UI/UX
├── simulation/     # Desarrollo de modelos físicos
├── data/          # Datasets y archivos de datos
└── docs/          # Documentación
```

### Comandos Útiles

```bash
# Backend - Ejecutar con recarga automática
cd backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Frontend - Modo desarrollo
cd frontend
npm run start

# Ejecutar tests
cd backend
python -m pytest tests/

cd frontend
npm test
```

### Herramientas de Desarrollo Recomendadas

- **VS Code Extensions**:
  - Python
  - ES7+ React/Redux/React-Native snippets
  - REST Client (para probar APIs)
  - GitLens

- **Postman o Insomnia**: Para probar endpoints de la API
- **React Developer Tools**: Para debugging del frontend

## Próximos Pasos

Después de la instalación exitosa:

1. **Explorar la Aplicación**: Navegar por todas las secciones
2. **Revisar la Documentación**: Leer `docs/README.md` para entender la arquitectura
3. **Personalizar**: Modificar parámetros de simulación según necesidades
4. **Contribuir**: Ver `CONTRIBUTING.md` para guías de contribución

¡La aplicación debería estar funcionando correctamente! 🚀