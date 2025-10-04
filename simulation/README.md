# Motor de Simulación de Impactos

Este módulo contiene los algoritmos y modelos físicos para simular impactos de asteroides.

## Estructura

```
simulation/
├── __init__.py
├── impact_simulator.py    # Simulador principal de impactos
├── physics_models.py      # Modelos físicos y ecuaciones
├── crater_calculator.py   # Cálculo de cráteres
├── damage_assessment.py   # Evaluación de daños
└── visualization.py       # Generación de gráficos
```

## Modelos Implementados

### Física de Impactos
- Energía cinética de asteroides
- Formación de cráteres
- Ondas sísmicas
- Efectos atmosféricos

### Evaluación de Daños
- Estimación de víctimas
- Daño a infraestructura
- Impacto económico
- Efectos ambientales

## Uso

```python
from simulation.impact_simulator import ImpactSimulator

simulator = ImpactSimulator()
result = simulator.simulate_impact(
    diameter=1.2,  # km
    velocity=18.5,  # km/s
    angle=45,      # grados
    location=(40.7589, -73.9851)  # NYC
)
```