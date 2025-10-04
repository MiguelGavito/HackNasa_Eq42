# Archivos de Datos

Este directorio contiene datasets y archivos de datos utilizados por la aplicación.

## Estructura

```
data/
├── asteroids/          # Datos de asteroides de NASA
├── models/             # Modelos entrenados y parámetros
├── cache/              # Cache de datos de APIs
└── samples/            # Datos de ejemplo para desarrollo
```

## Fuentes de Datos

### NASA APIs
- **Near Earth Object Web Service (NeoWs)**: Datos de objetos cercanos a la Tierra
- **Small-Body Database (SBDB)**: Información detallada de cuerpos pequeños
- **Close Approach Data (CAD)**: Datos de aproximaciones cercanas

### USGS Data
- **Earthquake Data**: Para modelar efectos sísmicos
- **Geographic Data**: Información geológica y topográfica

## Formato de Datos

Los datos se almacenan principalmente en formato JSON para facilitar la integración con el frontend y backend.

### Ejemplo de Estructura de Asteroide

```json
{
  "id": "2025-IMPACT",
  "name": "Impactador-2025",
  "diameter": 1.2,
  "velocity": 18.5,
  "distance_from_earth": 7500000,
  "risk_level": "HIGH",
  "impact_probability": 0.15,
  "orbital_data": {
    "period": 365.25,
    "eccentricity": 0.1
  }
}
```