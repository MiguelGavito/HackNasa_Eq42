# Meteor Madness - Backend

API REST para el sistema de simulación de impactos de asteroides.

## Estructura

```
backend/
├── app.py              # Aplicación principal FastAPI
├── models/             # Modelos de datos
├── routes/             # Endpoints de la API
├── services/           # Lógica de negocio
├── utils/              # Utilidades
└── requirements.txt    # Dependencias Python
```

## Endpoints Principales

- `/api/asteroids` - Obtener lista de asteroides
- `/api/simulation` - Ejecutar simulación de impacto
- `/api/risk-analysis` - Análisis de riesgos
- `/api/mitigation` - Estrategias de mitigación

## Instalación

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```