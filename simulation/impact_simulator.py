"""
Motor de Simulación de Impactos de Asteroides
Desarrollado para el NASA Hackathon 2025 - Equipo 42
"""

import numpy as np
from dataclasses import dataclass
from typing import Tuple, Dict, Any
import math

@dataclass
class AsteroidProperties:
    """Propiedades físicas de un asteroide"""
    diameter: float  # km
    density: float   # kg/m³ (default: 2500 para asteroides rocosos)
    velocity: float  # km/s
    angle: float     # grados (ángulo de impacto)
    composition: str # "rocky", "metallic", "icy"

@dataclass
class ImpactLocation:
    """Ubicación del impacto"""
    latitude: float
    longitude: float
    terrain_type: str  # "ocean", "land", "urban", "desert"
    elevation: float   # metros sobre el nivel del mar

@dataclass
class ImpactResult:
    """Resultados de la simulación de impacto"""
    crater_diameter: float      # km
    crater_depth: float         # km
    energy_released: float      # megatones TNT
    seismic_magnitude: float    # Escala Richter
    affected_area: float        # km²
    casualties_estimate: int
    economic_damage: float      # USD
    atmospheric_effects: Dict[str, Any]
    tsunami_risk: bool
    
class ImpactSimulator:
    """Simulador principal de impactos de asteroides"""
    
    def __init__(self):
        # Constantes físicas
        self.EARTH_GRAVITY = 9.81  # m/s²
        self.TNT_ENERGY = 4.184e9  # Julios por tonelada de TNT
        self.EARTH_RADIUS = 6371   # km
        
        # Densidades típicas (kg/m³)
        self.DENSITIES = {
            "rocky": 2500,
            "metallic": 7800,
            "icy": 900
        }
        
        # Factores de población por tipo de terreno (personas/km²)
        self.POPULATION_DENSITY = {
            "ocean": 0,
            "land": 50,
            "urban": 1000,
            "desert": 1,
            "forest": 10
        }
    
    def calculate_mass(self, asteroid: AsteroidProperties) -> float:
        """Calcula la masa del asteroide"""
        radius_m = (asteroid.diameter * 1000) / 2  # convertir a metros
        volume_m3 = (4/3) * math.pi * (radius_m ** 3)
        
        if asteroid.density:
            density = asteroid.density
        else:
            density = self.DENSITIES.get(asteroid.composition, 2500)
        
        return volume_m3 * density  # kg
    
    def calculate_kinetic_energy(self, asteroid: AsteroidProperties) -> float:
        """Calcula la energía cinética del impacto"""
        mass_kg = self.calculate_mass(asteroid)
        velocity_ms = asteroid.velocity * 1000  # convertir a m/s
        
        # Considerar el ángulo de impacto
        angle_factor = math.sin(math.radians(asteroid.angle))
        effective_velocity = velocity_ms * angle_factor
        
        energy_joules = 0.5 * mass_kg * (effective_velocity ** 2)
        return energy_joules
    
    def calculate_crater_dimensions(self, energy_joules: float, asteroid: AsteroidProperties) -> Tuple[float, float]:
        """Calcula las dimensiones del cráter usando ecuaciones empíricas"""
        
        # Convertir energía a megatones TNT
        energy_mt = energy_joules / (self.TNT_ENERGY * 1e6)
        
        # Fórmula empírica para diámetro del cráter (Schmidt & Housen, 1987)
        # D = 1.8 * (E/ρg)^0.22 * (ρp/ρt)^0.33
        
        gravity = self.EARTH_GRAVITY
        projectile_density = self.DENSITIES.get(asteroid.composition, 2500)
        target_density = 2500  # densidad promedio de la corteza terrestre
        
        # Simplificación de la fórmula
        diameter_m = 1.8 * ((energy_joules / (target_density * gravity)) ** 0.22) * \
                    ((projectile_density / target_density) ** 0.33)
        
        diameter_km = diameter_m / 1000
        
        # La profundidad típica es ~1/10 del diámetro
        depth_km = diameter_km * 0.1
        
        return diameter_km, depth_km
    
    def calculate_seismic_effects(self, energy_joules: float) -> float:
        """Calcula la magnitud sísmica del impacto"""
        # Relación empírica entre energía y magnitud sísmica
        # M = (2/3) * log10(E) - 6.0 (donde E está en Julios)
        
        if energy_joules > 0:
            magnitude = (2/3) * math.log10(energy_joules) - 6.0
            return max(0, magnitude)  # No permitir magnitudes negativas
        return 0
    
    def calculate_affected_area(self, crater_diameter_km: float, energy_mt: float) -> float:
        """Calcula el área total afectada por el impacto"""
        
        # Área del cráter
        crater_area = math.pi * (crater_diameter_km / 2) ** 2
        
        # Área de destrucción extendida (aproximación)
        # Basada en la energía liberada y efectos de onda expansiva
        destruction_radius = crater_diameter_km * (1 + math.log10(max(1, energy_mt)))
        destruction_area = math.pi * (destruction_radius / 2) ** 2
        
        return destruction_area
    
    def estimate_casualties(self, affected_area_km2: float, location: ImpactLocation) -> int:
        """Estima el número de víctimas"""
        
        population_density = self.POPULATION_DENSITY.get(location.terrain_type, 50)
        
        # Población total en el área afectada
        total_population = affected_area_km2 * population_density
        
        # Factor de mortalidad (varía según el tipo de impacto)
        if location.terrain_type == "ocean":
            mortality_rate = 0.1  # Principalmente por tsunami
        elif location.terrain_type == "urban":
            mortality_rate = 0.3  # Alta densidad, más víctimas
        else:
            mortality_rate = 0.2  # Promedio para otros terrenos
        
        return int(total_population * mortality_rate)
    
    def estimate_economic_damage(self, affected_area_km2: float, location: ImpactLocation) -> float:
        """Estima el daño económico en USD"""
        
        # Valor económico por km² según el tipo de terreno
        economic_values = {
            "ocean": 1e6,      # $1M por km² (principalmente pesca, transporte)
            "land": 1e8,       # $100M por km² (agricultura, infraestructura rural)
            "urban": 1e10,     # $10B por km² (infraestructura urbana)
            "desert": 1e5,     # $100K por km² (valor mínimo)
            "forest": 1e7      # $10M por km² (recursos naturales)
        }
        
        value_per_km2 = economic_values.get(location.terrain_type, 1e8)
        return affected_area_km2 * value_per_km2
    
    def check_tsunami_risk(self, location: ImpactLocation, crater_diameter_km: float) -> bool:
        """Evalúa el riesgo de tsunami"""
        
        # Solo océanos pueden generar tsunamis
        if location.terrain_type != "ocean":
            return False
        
        # Cráteres de más de 1 km en océano pueden generar tsunamis significativos
        return crater_diameter_km > 1.0
    
    def calculate_atmospheric_effects(self, energy_mt: float, asteroid: AsteroidProperties) -> Dict[str, Any]:
        """Calcula efectos atmosféricos del impacto"""
        
        effects = {
            "dust_cloud_height": 0,      # km
            "dust_cloud_duration": 0,    # días
            "global_cooling": 0,         # grados Celsius
            "ozone_depletion": 0         # porcentaje
        }
        
        # Solo impactos grandes tienen efectos atmosféricos significativos
        if energy_mt > 100:  # Más de 100 megatones
            effects["dust_cloud_height"] = min(50, energy_mt / 1000 * 10)  # km
            effects["dust_cloud_duration"] = min(365, energy_mt / 100)     # días
            effects["global_cooling"] = min(5, energy_mt / 10000)          # °C
            effects["ozone_depletion"] = min(10, energy_mt / 1000)         # %
        
        return effects
    
    def simulate_impact(self, asteroid: AsteroidProperties, location: ImpactLocation) -> ImpactResult:
        """Ejecuta la simulación completa del impacto"""
        
        # Cálculos principales
        energy_joules = self.calculate_kinetic_energy(asteroid)
        energy_mt = energy_joules / (self.TNT_ENERGY * 1e6)  # Convertir a megatones
        
        crater_diameter, crater_depth = self.calculate_crater_dimensions(energy_joules, asteroid)
        seismic_magnitude = self.calculate_seismic_effects(energy_joules)
        affected_area = self.calculate_affected_area(crater_diameter, energy_mt)
        
        casualties = self.estimate_casualties(affected_area, location)
        economic_damage = self.estimate_economic_damage(affected_area, location)
        
        tsunami_risk = self.check_tsunami_risk(location, crater_diameter)
        atmospheric_effects = self.calculate_atmospheric_effects(energy_mt, asteroid)
        
        return ImpactResult(
            crater_diameter=crater_diameter,
            crater_depth=crater_depth,
            energy_released=energy_mt,
            seismic_magnitude=seismic_magnitude,
            affected_area=affected_area,
            casualties_estimate=casualties,
            economic_damage=economic_damage,
            atmospheric_effects=atmospheric_effects,
            tsunami_risk=tsunami_risk
        )

# Función de conveniencia para uso rápido
def quick_simulation(diameter_km: float, velocity_kms: float, 
                    lat: float, lon: float, terrain: str = "land") -> ImpactResult:
    """
    Función rápida para simular un impacto con parámetros básicos
    
    Args:
        diameter_km: Diámetro del asteroide en km
        velocity_kms: Velocidad de impacto en km/s
        lat: Latitud del impacto
        lon: Longitud del impacto
        terrain: Tipo de terreno ("ocean", "land", "urban", "desert")
    
    Returns:
        ImpactResult: Resultados de la simulación
    """
    
    asteroid = AsteroidProperties(
        diameter=diameter_km,
        density=2500,  # Asteroide rocoso típico
        velocity=velocity_kms,
        angle=45,      # Ángulo típico
        composition="rocky"
    )
    
    location = ImpactLocation(
        latitude=lat,
        longitude=lon,
        terrain_type=terrain,
        elevation=0
    )
    
    simulator = ImpactSimulator()
    return simulator.simulate_impact(asteroid, location)