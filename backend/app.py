from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import numpy as np
from datetime import datetime
import json

app = FastAPI(title="Meteor Madness API", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de datos
class Asteroid(BaseModel):
    id: str
    name: str
    diameter: float  # km
    velocity: float  # km/s
    distance_from_earth: float  # km
    risk_level: str
    impact_probability: float

class SimulationRequest(BaseModel):
    asteroid_id: str
    impact_location: dict  # {"lat": float, "lon": float}
    impact_angle: float
    impact_velocity: float
    # Campos opcionales para asteroides personalizados
    asteroid_diameter: Optional[float] = None
    asteroid_composition: Optional[str] = None
    asteroid_density: Optional[float] = None

class SimulationResult(BaseModel):
    crater_diameter: float
    energy_released: float  # megatons TNT
    affected_area: float  # km²
    casualties_estimate: int
    economic_damage: float  # USD

# Datos de ejemplo (normalmente vendría de NASA APIs)
sample_asteroids = [
    {
        "id": "2025-IMPACT",
        "name": "Impactador-2025",
        "diameter": 1.2,
        "velocity": 18.5,
        "distance_from_earth": 7500000,
        "risk_level": "HIGH",
        "impact_probability": 0.15
    },
    {
        "id": "2023-BU",
        "name": "Apophis-like",
        "diameter": 0.34,
        "velocity": 12.8,
        "distance_from_earth": 15000000,
        "risk_level": "MEDIUM",
        "impact_probability": 0.003
    }
]

@app.get("/")
async def root():
    return {"message": "Meteor Madness API - NASA Hackathon 2025"}

@app.get("/api/asteroids", response_model=List[Asteroid])
async def get_asteroids():
    """Obtener lista de asteroides conocidos"""
    return sample_asteroids

@app.get("/api/asteroids/{asteroid_id}", response_model=Asteroid)
async def get_asteroid(asteroid_id: str):
    """Obtener información de un asteroide específico"""
    asteroid = next((a for a in sample_asteroids if a["id"] == asteroid_id), None)
    if not asteroid:
        raise HTTPException(status_code=404, detail="Asteroid not found")
    return asteroid

@app.post("/api/simulation", response_model=SimulationResult)
async def run_simulation(simulation_request: SimulationRequest):
    """Ejecutar simulación de impacto de asteroide"""
    
    # Verificar si es un asteroide personalizado (del Asteroid Launcher)
    if simulation_request.asteroid_id == "custom-asteroid":
        # Usar datos personalizados del request
        diameter = getattr(simulation_request, 'asteroid_diameter', 1.0)
        velocity = simulation_request.impact_velocity
        composition = getattr(simulation_request, 'asteroid_composition', 'rocky')
        density = getattr(simulation_request, 'asteroid_density', 2500)
    else:
        # Obtener datos del asteroide predefinido
        asteroid = next((a for a in sample_asteroids if a["id"] == simulation_request.asteroid_id), None)
        if not asteroid:
            raise HTTPException(status_code=404, detail="Asteroid not found")
        
        diameter = asteroid["diameter"]
        velocity = simulation_request.impact_velocity
        composition = "rocky"
        density = 2500
    
    # Energía cinética: E = 0.5 * m * v²
    # Masa estimada basada en densidad promedio de asteroides (2.5 g/cm³)
    volume = (4/3) * np.pi * (diameter/2)**3  # km³
    mass = volume * 2.5e12  # kg (densidad 2.5 g/cm³)
    energy_joules = 0.5 * mass * (velocity * 1000)**2  # Joules
    energy_megatons = energy_joules / 4.184e15  # Conversión a megatones TNT
    
    # Diámetro del cráter (fórmula empírica)
    crater_diameter = 1.8 * (diameter * 1000) * (velocity / 12)**0.78  # metros
    crater_diameter_km = crater_diameter / 1000
    
    # Área afectada (aproximación circular)
    affected_area = np.pi * (crater_diameter_km * 10)**2  # Área extendida
    
    # Estimación de víctimas (basada en densidad poblacional promedio)
    population_density = 50  # personas por km²
    casualties_estimate = int(affected_area * population_density * 0.7)  # 70% de afectación
    
    # Daño económico (estimación simplificada)
    economic_damage = affected_area * 1e9  # $1B por km² afectado
    
    return SimulationResult(
        crater_diameter=crater_diameter_km,
        energy_released=energy_megatons,
        affected_area=affected_area,
        casualties_estimate=casualties_estimate,
        economic_damage=economic_damage
    )

@app.get("/api/risk-analysis/{asteroid_id}")
async def get_risk_analysis(asteroid_id: str):
    """Obtener análisis de riesgos detallado"""
    asteroid = next((a for a in sample_asteroids if a["id"] == asteroid_id), None)
    if not asteroid:
        raise HTTPException(status_code=404, detail="Asteroid not found")
    
    # Calcular factores de riesgo
    size_factor = min(asteroid["diameter"] / 10, 1.0)  # Normalizado a 10km max
    velocity_factor = min(asteroid["velocity"] / 30, 1.0)  # Normalizado a 30km/s max
    distance_factor = max(0, 1 - (asteroid["distance_from_earth"] / 50000000))  # 50M km threshold
    
    overall_risk = (size_factor + velocity_factor + distance_factor) / 3
    
    return {
        "asteroid_id": asteroid_id,
        "overall_risk_score": overall_risk,
        "risk_factors": {
            "size": size_factor,
            "velocity": velocity_factor,
            "proximity": distance_factor
        },
        "mitigation_urgency": "HIGH" if overall_risk > 0.7 else "MEDIUM" if overall_risk > 0.4 else "LOW",
        "estimated_detection_time": "6 months" if distance_factor > 0.8 else "2 years",
        "recommended_actions": [
            "Continuous monitoring",
            "Trajectory refinement",
            "Mission planning" if overall_risk > 0.5 else "Observation only"
        ]
    }

@app.get("/api/mitigation-strategies/{asteroid_id}")
async def get_mitigation_strategies(asteroid_id: str):
    """Obtener estrategias de mitigación disponibles"""
    asteroid = next((a for a in sample_asteroids if a["id"] == asteroid_id), None)
    if not asteroid:
        raise HTTPException(status_code=404, detail="Asteroid not found")
    
    strategies = []
    
    # Deflección cinética
    if asteroid["diameter"] < 5:
        strategies.append({
            "name": "Kinetic Impactor",
            "description": "Misión de impacto para cambiar la trayectoria",
            "success_probability": 0.85,
            "cost_estimate": 500e6,  # $500M
            "preparation_time": "3-5 years",
            "effectiveness": "High for small asteroids"
        })
    
    # Tractor gravitacional
    if asteroid["distance_from_earth"] > 10000000:
        strategies.append({
            "name": "Gravity Tractor",
            "description": "Nave espacial que usa gravedad para desviar asteroide",
            "success_probability": 0.75,
            "cost_estimate": 2e9,  # $2B
            "preparation_time": "10-15 years",
            "effectiveness": "Medium, requires long lead time"
        })
    
    # Evacuación
    strategies.append({
        "name": "Evacuation",
        "description": "Evacuación de áreas de impacto potencial",
        "success_probability": 0.95,
        "cost_estimate": 10e9,  # $10B
        "preparation_time": "1-2 years",
        "effectiveness": "High for saving lives, zero for infrastructure"
    })
    
    return {
        "asteroid_id": asteroid_id,
        "available_strategies": strategies,
        "recommended_strategy": strategies[0]["name"] if strategies else "Monitoring",
        "decision_timeline": "Immediate action required" if asteroid["risk_level"] == "HIGH" else "Plan within 2 years"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)