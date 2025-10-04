# Documentación Técnica

Documentación detallada del proyecto Meteor Madness.

## Contenido

- [Arquitectura del Sistema](architecture.md)
- [API Reference](api-reference.md)
- [Guía de Instalación](installation-guide.md)
- [Desarrollo](development-guide.md)
- [Deployment](deployment-guide.md)

## Arquitectura General

### Frontend (React)
- **Tecnologías**: React.js, Material-UI, Three.js
- **Responsabilidades**: UI/UX, visualización 3D, dashboards interactivos

### Backend (FastAPI)
- **Tecnologías**: Python, FastAPI, NumPy, Pandas
- **Responsabilidades**: API REST, integración con NASA, simulaciones

### Motor de Simulación (Python)
- **Tecnologías**: SciPy, NumPy, Astropy
- **Responsabilidades**: Cálculos físicos, modelado de impactos

## APIs Utilizadas

### NASA APIs
1. **Near Earth Object Web Service (NeoWs)**
   - URL: `https://api.nasa.gov/neo/rest/v1`
   - Propósito: Datos de asteroides cercanos

2. **Small-Body Database (SBDB)**
   - URL: `https://ssd-api.jpl.nasa.gov/sbdb.api`
   - Propósito: Datos físicos y orbitales detallados

3. **Close Approach Data (CAD)**
   - URL: `https://ssd-api.jpl.nasa.gov/cad.api`
   - Propósito: Datos de aproximaciones cercanas

## Flujo de Datos

```
NASA APIs → Backend (FastAPI) → Frontend (React) → Usuario
    ↓
Simulación Engine → Resultados → Visualización
```

## Modelos de Datos

### Asteroide
```python
{
    "id": str,
    "name": str,
    "diameter": float,
    "velocity": float,
    "distance_from_earth": float,
    "risk_level": str,
    "impact_probability": float
}
```

### Resultado de Simulación
```python
{
    "crater_diameter": float,
    "energy_released": float,
    "affected_area": float,
    "casualties_estimate": int,
    "economic_damage": float
}
```