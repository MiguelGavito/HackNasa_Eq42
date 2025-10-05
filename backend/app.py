from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import numpy as np
from datetime import datetime
import json
from services.nasa_api import NASAApiService
from services.demographic_service import DemographicService

app = FastAPI(title="Meteor Madness API", version="1.0.0")

# Inicializar servicios
nasa_service = NASAApiService()
demographic_service = DemographicService()

# Función helper para buscar asteroides
def find_asteroid_by_id(asteroid_id: str):
    """Buscar asteroide por ID en datos NASA y samples"""
    try:
        # Buscar primero en datos de NASA
        nasa_asteroids = nasa_service.get_processed_asteroids(limit=50)
        nasa_asteroid = next((a for a in nasa_asteroids if a["id"] == asteroid_id), None)
        
        if nasa_asteroid:
            # Convertir formato NASA a formato estándar
            return {
                "id": nasa_asteroid["id"],
                "name": nasa_asteroid["name"],
                "diameter": nasa_asteroid["estimated_diameter_km_max"],
                "velocity": nasa_asteroid["relative_velocity_km_s"],
                "distance_from_earth": nasa_asteroid["miss_distance_km"],
                "risk_level": "High" if nasa_asteroid["is_potentially_hazardous_asteroid"] else "Low",
                "impact_probability": 0.001 if nasa_asteroid["is_potentially_hazardous_asteroid"] else 0.0001,
                "source": "nasa"
            }
        else:
            # Buscar en samples como fallback
            sample_asteroid = next((a for a in sample_asteroids if a["id"] == asteroid_id), None)
            if sample_asteroid:
                sample_asteroid["source"] = "sample"
                return sample_asteroid
            else:
                return None
    except Exception as e:
        print(f"Error buscando asteroide {asteroid_id}: {e}")
        # Fallback final a samples
        sample_asteroid = next((a for a in sample_asteroids if a["id"] == asteroid_id), None)
        if sample_asteroid:
            sample_asteroid["source"] = "sample"
            return sample_asteroid
        return None

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

@app.get("/api/coordinate-test/{lat}/{lon}")
async def test_coordinate_mapping(lat: float, lon: float):
    """Verificar mapeo de coordenadas y clasificación geográfica"""
    import math
    
    # Función de conversión como en el frontend
    def latlon_to_3d(lat_deg, lon_deg, radius=1):
        lat_rad = lat_deg * math.pi / 180
        lon_rad = lon_deg * math.pi / 180
        
        x = radius * math.cos(lat_rad) * math.cos(lon_rad)
        y = radius * math.sin(lat_rad)
        z = radius * math.cos(lat_rad) * math.sin(lon_rad)
        
        return x, y, z
    
    def pos_3d_to_latlon(x, y, z):
        length = math.sqrt(x*x + y*y + z*z)
        nx, ny, nz = x/length, y/length, z/length
        
        lat = math.asin(ny) * (180 / math.pi)
        lon = math.atan2(nz, nx) * (180 / math.pi)
        
        return lat, lon
    
    try:
        # Test round-trip conversion
        x, y, z = latlon_to_3d(lat, lon)
        back_lat, back_lon = pos_3d_to_latlon(x, y, z)
        
        conversion_error = abs(lat - back_lat) + abs(lon - back_lon)
        
        # Obtener info demográfica
        demo_info = demographic_service.calculate_population_density(lat, lon)
        
        # Determinar región geográfica esperada
        expected_region = "Unknown"
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            if abs(lat) > 80:
                expected_region = "Polar"
            elif -60 < lat < 60 and ((120 < lon < 180) or (-180 < lon < -80)):
                expected_region = "Pacific Ocean"
            elif -60 < lat < 70 and -80 < lon < 20:
                expected_region = "Atlantic Ocean"  
            elif -60 < lat < 30 and 20 < lon < 120:
                expected_region = "Indian Ocean"
            elif 25 < lat < 50 and -130 < lon < -65:
                expected_region = "North America"
            elif 35 < lat < 70 and -10 < lon < 40:
                expected_region = "Europe"
            elif -35 < lat < 35 and 70 < lon < 140:
                expected_region = "Asia"
            elif -40 < lat < -10 and 110 < lon < 160:
                expected_region = "Australia"
            elif -55 < lat < 15 and -80 < lon < -35:
                expected_region = "South America"
            elif -35 < lat < 35 and -20 < lon < 55:
                expected_region = "Africa"
        
        return {
            "status": "success",
            "input_coordinates": {"lat": lat, "lon": lon},
            "conversion_test": {
                "3d_position": {"x": round(x, 4), "y": round(y, 4), "z": round(z, 4)},
                "back_to_latlon": {"lat": round(back_lat, 4), "lon": round(back_lon, 4)},
                "conversion_error_degrees": round(conversion_error, 6),
                "conversion_accurate": conversion_error < 0.01
            },
            "geographic_analysis": {
                "expected_region": expected_region,
                "detected_region_type": demo_info.get("region_type", "unknown"),
                "is_ocean_expected": "Ocean" in expected_region,
                "is_ocean_detected": demo_info.get("region_type") == "ocean",
                "ocean_detection_correct": ("Ocean" in expected_region) == (demo_info.get("region_type") == "ocean")
            },
            "demographic_data": demo_info,
            "coordinates_validation": {
                "latitude_valid": -90 <= lat <= 90,
                "longitude_valid": -180 <= lon <= 180,
                "within_earth_bounds": True
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "coordinates": {"lat": lat, "lon": lon}
        }

@app.get("/api/demographic-info/{lat}/{lon}")
async def get_demographic_info(lat: float, lon: float):
    """Obtener información demográfica para coordenadas específicas"""
    try:
        demo_info = demographic_service.calculate_population_density(lat, lon)
        return {
            "status": "success",
            "coordinates": {"lat": lat, "lon": lon},
            "demographic_data": demo_info
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@app.get("/api/test-nasa")
async def test_nasa_connection():
    """Endpoint de prueba para verificar conexión con NASA API"""
    try:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('NASA_API_KEY', 'DEMO_KEY')
        
        # Probar nuestro servicio optimizado
        processed_asteroids = nasa_service.get_processed_asteroids(limit=3)
        
        return {
            "status": "success",
            "api_key_loaded": api_key[:10] + "..." if api_key != 'DEMO_KEY' else 'DEMO_KEY',
            "processed_asteroids_count": len(processed_asteroids),
            "sample_asteroid": processed_asteroids[0] if processed_asteroids else None,
            "message": "NASA API funcionando correctamente con datos procesados"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_type": type(e).__name__,
            "error_message": str(e)
        }

@app.get("/api/asteroids", response_model=List[Asteroid])
async def get_asteroids():
    """Obtener lista de asteroides conocidos desde NASA API (optimizado)"""
    try:
        # Obtener datos procesados y limitados de NASA
        processed_asteroids = nasa_service.get_processed_asteroids(limit=15)
        
        if not processed_asteroids:
            print("No se obtuvieron asteroides procesados, usando datos de muestra")
            return sample_asteroids
        
        # Convertir a formato de nuestra API
        asteroids = []
        for neo in processed_asteroids:
            asteroids.append({
                "id": neo['id'],
                "name": neo['name'],
                "diameter": neo['estimated_diameter_km_max'],
                "velocity": neo['relative_velocity_km_s'],
                "distance_from_earth": neo['miss_distance_km'],
                "risk_level": "High" if neo['is_potentially_hazardous_asteroid'] else "Low",
                "impact_probability": 0.001 if neo['is_potentially_hazardous_asteroid'] else 0.0001
            })
        
        print(f"✅ Devolviendo {len(asteroids)} asteroides reales de NASA")
        return asteroids
        
    except Exception as e:
        # Si hay error con NASA API, usar datos de muestra como fallback
        print(f"❌ Error conectando con NASA API: {e}")
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
        # Buscar asteroide primero en datos reales de NASA
        try:
            nasa_asteroids = nasa_service.get_processed_asteroids(limit=50)
            asteroid = next((a for a in nasa_asteroids if a["id"] == simulation_request.asteroid_id), None)
            
            if asteroid:
                diameter = asteroid["estimated_diameter_km_max"]
                velocity = simulation_request.impact_velocity
                composition = "rocky"
                density = 2500
            else:
                # Si no se encuentra en NASA, buscar en sample_asteroids como fallback
                sample_asteroid = next((a for a in sample_asteroids if a["id"] == simulation_request.asteroid_id), None)
                if not sample_asteroid:
                    raise HTTPException(status_code=404, detail=f"Asteroid {simulation_request.asteroid_id} not found in NASA data or samples")
                
                diameter = sample_asteroid["diameter"]
                velocity = simulation_request.impact_velocity
                composition = "rocky"
                density = 2500
                
        except Exception as e:
            print(f"Error buscando asteroide en NASA API: {e}")
            # Fallback a sample_asteroids
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
    
    # Diámetro del cráter (fórmula empírica corregida)
    # Fórmula basada en estudios reales: D_crater ≈ D_asteroid * factor_velocidad
    crater_diameter_km = 1.8 * diameter * (velocity / 12)**0.78  # km directamente
    
    # Obtener coordenadas del impacto
    impact_lat = simulation_request.impact_location.get("lat", 0)
    impact_lon = simulation_request.impact_location.get("lon", 0)
    
    # Calcular víctimas usando servicio demográfico
    casualty_analysis = demographic_service.estimate_casualties(
        lat=impact_lat,
        lon=impact_lon,
        crater_diameter_km=crater_diameter_km,
        energy_megatons=energy_megatons
    )
    
    casualties_estimate = casualty_analysis.get("total_casualties", 0)
    affected_area = casualty_analysis.get("casualties_by_zone", {}).get("moderate_damage_zone", {}).get("radius_km", crater_diameter_km * 3) ** 2 * np.pi
    
    # Daño económico basado en tipo de región
    region_type = casualty_analysis.get("region_info", {}).get("region_type", "unknown")
    economic_multiplier = {
        "urban_major": 10e9,    # $10B por km² en ciudades principales
        "urban_large": 5e9,     # $5B por km² en ciudades grandes
        "urban_medium": 2e9,    # $2B por km² en ciudades medianas
        "suburban": 1e9,        # $1B por km² en suburbios
        "rural_populated": 0.5e9,  # $500M por km² en rural poblado
        "rural_sparse": 0.1e9,     # $100M por km² en rural disperso
        "ocean": 0.05e9,        # $50M por km² en océano (principalmente navíos)
        "unknown": 1e9          # Default
    }.get(region_type, 1e9)
    
    economic_damage = affected_area * economic_multiplier
    
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
    asteroid = find_asteroid_by_id(asteroid_id)
    if not asteroid:
        raise HTTPException(status_code=404, detail=f"Asteroid {asteroid_id} not found in NASA or sample data")
    
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
    asteroid = find_asteroid_by_id(asteroid_id)
    if not asteroid:
        raise HTTPException(status_code=404, detail=f"Asteroid {asteroid_id} not found in NASA or sample data")
    
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