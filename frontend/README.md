# Meteor Madness - Frontend

Interfaz de usuario React para la visualización interactiva de asteroides y simulaciones.

## Estructura

```
frontend/
├── public/             # Archivos públicos
├── src/
│   ├── components/     # Componentes React
│   ├── pages/          # Páginas principales
│   ├── services/       # Servicios API
│   ├── utils/          # Utilidades
│   └── App.js          # Componente principal
├── package.json
└── README.md
```

## Componentes Principales

- `AsteroidViewer` - Visualización 3D de asteroides
- `SimulationPanel` - Panel de control de simulación
- `RiskAnalysis` - Análisis de riesgos visualizado
- `DataDashboard` - Dashboard de datos de NASA

## Instalación

```bash
npm install
npm start
```

## Tecnologías

- React.js
- Three.js (3D)
- Material-UI
- Axios