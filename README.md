# Meteor Madness 🌟

## Descripción del Proyecto

**Meteor Madness** es una herramienta interactiva de visualización y simulación que utiliza datos reales de la NASA para ayudar a los usuarios a modelar escenarios de impacto de asteroides, predecir consecuencias y evaluar posibles estrategias de mitigación.

### Problema a Resolver

Un asteroide cercano a la Tierra recientemente identificado, "Impactador-2025", representa una amenaza potencial para nuestro planeta. Los conjuntos de datos de la NASA incluyen información sobre asteroides conocidos y el Servicio Geológico de los Estados Unidos proporciona información crítica que podría permitir modelar los efectos de los impactos de asteroides. Sin embargo, estos datos necesitan integrarse para permitir una visualización y una toma de decisiones efectivas.

### Objetivo

Desarrollar una herramienta interactiva de visualización y simulación que utilice datos reales para ayudar a los usuarios a modelar escenarios de impacto de asteroides, predecir consecuencias y evaluar posibles estrategias de mitigación.

## Características Principales

- 🚀 **Asteroid Launcher**: Simulador interactivo estilo neal.fun para experimentar con impactos
- 🌍 **Visualización 3D Interactiva**: Representa la Tierra y asteroides en tiempo real
- 📊 **Simulación de Impactos**: Modela diferentes escenarios de impacto con cálculos físicos
- 📈 **Análisis de Riesgos**: Evalúa y predice consecuencias de impactos
- 🛰️ **Datos de NASA**: Integración con datasets oficiales de asteroides
- 🎯 **Estrategias de Mitigación**: Evaluación de posibles soluciones
- 📱 **Interfaz Responsive**: Accesible desde diferentes dispositivos

## Arquitectura del Proyecto

```
meteor-madness/
├── frontend/           # Aplicación React para UI
├── backend/            # API REST con Python (FastAPI/Flask)
├── simulation/         # Motor de simulación de impactos
├── data/              # Datasets y archivos de datos
├── docs/              # Documentación técnica
└── tests/             # Pruebas unitarias e integración
```

## Tecnologías Utilizadas

### Frontend
- React.js
- Three.js (visualización 3D)
- D3.js (gráficos y datos)
- Material-UI o Tailwind CSS

### Backend
- Python
- FastAPI o Flask
- NumPy/Pandas (procesamiento de datos)
- SQLite o PostgreSQL (base de datos)

### Simulación
- Python científico (SciPy, NumPy)
- Bibliotecas de astronomía (Astropy)
- Modelos físicos de impacto

### APIs Externas
- NASA Small-Body Database
- NASA JPL Horizons
- USGS Earthquake Data

## Instalación y Configuración

### Prerrequisitos
- Node.js (v14+)
- Python (v3.8+)
- Git

### Configuración del Entorno

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/MiguelGavito/HackNasa_Eq42.git
   cd HackNasa_Eq42
   ```

2. **Backend**
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

3. **Frontend**
   ```bash
   cd frontend
   npm install
   ```

## Uso

### Ejecutar el Backend
```bash
cd backend
python app.py
```

### Ejecutar el Frontend
```bash
cd frontend
npm start
```

## Niveles de Dificultad

El proyecto está diseñado con tres niveles de dificultad:
- 🟢 **Básico**: Visualización simple de asteroides
- 🟡 **Intermedio**: Simulación básica de impactos
- 🔴 **Avanzado**: Análisis completo de riesgos y mitigación

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Equipo

**Equipo 42** - Participantes del Hackathón NASA

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## Agradecimientos

- NASA por proporcionar los datasets de asteroides
- USGS por los datos geológicos
- Comunidad de código abierto por las herramientas utilizadas

---

*Desarrollado para el NASA Space Apps Challenge 2025*