"""
Integración con APIs de la NASA
Servicio para obtener datos reales de asteroides cercanos a la Tierra
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import json
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NASAApiService:
    """Servicio para interactuar con las APIs de la NASA"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializar el servicio de NASA API
        
        Args:
            api_key: Clave API de NASA (opcional, usa DEMO_KEY por defecto)
        """
        self.api_key = api_key or "DEMO_KEY"
        self.base_urls = {
            "neo": "https://api.nasa.gov/neo/rest/v1",
            "sbdb": "https://ssd-api.jpl.nasa.gov/sbdb.api",
            "cad": "https://ssd-api.jpl.nasa.gov/cad.api"
        }
        
        # Configurar sesión HTTP
        self.session = requests.Session()
        self.session.params = {"api_key": self.api_key}
        
    def get_neo_feed(self, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """
        Obtener feed de objetos cercanos a la Tierra (NEO)
        
        Args:
            start_date: Fecha de inicio en formato YYYY-MM-DD
            end_date: Fecha final en formato YYYY-MM-DD
            
        Returns:
            Dict con datos de asteroides cercanos
        """
        
        # Si no se proporcionan fechas, usar los últimos 7 días
        if not start_date:
            start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
            
        url = f"{self.base_urls['neo']}/feed"
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "detailed": "true"
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al obtener NEO feed: {e}")
            return {}
    
    def get_asteroid_details(self, asteroid_id: str) -> Dict[str, Any]:
        """
        Obtener detalles específicos de un asteroide
        
        Args:
            asteroid_id: ID del asteroide (ej: "3542519")
            
        Returns:
            Dict con detalles del asteroide
        """
        url = f"{self.base_urls['neo']}/neo/{asteroid_id}"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al obtener detalles del asteroide {asteroid_id}: {e}")
            return {}
    
    def get_close_approach_data(self, date_min: str = None, date_max: str = None, 
                               dist_max: str = "0.2") -> List[Dict[str, Any]]:
        """
        Obtener datos de aproximaciones cercanas usando JPL CAD API
        
        Args:
            date_min: Fecha mínima (YYYY-MM-DD)
            date_max: Fecha máxima (YYYY-MM-DD)
            dist_max: Distancia máxima en AU (por defecto 0.2 AU)
            
        Returns:
            Lista de objetos con datos de aproximación
        """
        
        url = self.base_urls["cad"]
        params = {
            "dist-max": dist_max,
            "date-min": date_min or "2024-01-01",
            "date-max": date_max or "2026-01-01",
            "sort": "date"
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Convertir a formato más usable
            if "data" in data and "fields" in data:
                fields = data["fields"]
                objects = []
                for row in data["data"]:
                    obj = dict(zip(fields, row))
                    objects.append(obj)
                return objects
            
            return []
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al obtener datos CAD: {e}")
            return []
    
    def get_small_body_data(self, designation: str) -> Dict[str, Any]:
        """
        Obtener datos detallados de un cuerpo pequeño usando JPL SBDB
        
        Args:
            designation: Designación del objeto (ej: "2025 RR")
            
        Returns:
            Dict con datos físicos y orbitales
        """
        
        url = self.base_urls["sbdb"]
        params = {
            "sstr": designation,
            "full-prec": "true"
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al obtener datos SBDB para {designation}: {e}")
            return {}
    
    def parse_neo_data(self, neo_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Parsear datos NEO a formato estándar
        
        Args:
            neo_data: Datos raw de la API NEO
            
        Returns:
            Lista de asteroides en formato estándar
        """
        
        asteroids = []
        
        if "near_earth_objects" not in neo_data:
            return asteroids
        
        for date, objects in neo_data["near_earth_objects"].items():
            for obj in objects:
                try:
                    # Extraer datos básicos
                    asteroid = {
                        "id": obj.get("id"),
                        "name": obj.get("name", "").replace("(", "").replace(")", ""),
                        "neo_reference_id": obj.get("neo_reference_id"),
                        "absolute_magnitude": obj.get("absolute_magnitude_h"),
                        "is_potentially_hazardous": obj.get("is_potentially_hazardous_asteroid", False)
                    }
                    
                    # Diámetro estimado
                    diameter_data = obj.get("estimated_diameter", {})
                    if "kilometers" in diameter_data:
                        diameter = diameter_data["kilometers"]
                        asteroid["diameter_km_min"] = diameter.get("estimated_diameter_min", 0)
                        asteroid["diameter_km_max"] = diameter.get("estimated_diameter_max", 0)
                        asteroid["diameter_km_avg"] = (
                            asteroid["diameter_km_min"] + asteroid["diameter_km_max"]
                        ) / 2
                    
                    # Datos de aproximación cercana
                    close_approaches = obj.get("close_approach_data", [])
                    if close_approaches:
                        closest = min(close_approaches, 
                                    key=lambda x: float(x["miss_distance"]["astronomical"]))
                        
                        asteroid["close_approach_date"] = closest.get("close_approach_date")
                        asteroid["velocity_kms"] = float(
                            closest["relative_velocity"]["kilometers_per_second"]
                        )
                        asteroid["distance_au"] = float(closest["miss_distance"]["astronomical"])
                        asteroid["distance_km"] = float(closest["miss_distance"]["kilometers"])
                    
                    # Calcular nivel de riesgo
                    asteroid["risk_level"] = self._calculate_risk_level(asteroid)
                    
                    asteroids.append(asteroid)
                    
                except Exception as e:
                    logger.warning(f"Error al parsear objeto NEO: {e}")
                    continue
        
        return asteroids
    
    def _calculate_risk_level(self, asteroid: Dict[str, Any]) -> str:
        """
        Calcular nivel de riesgo basado en características del asteroide
        
        Args:
            asteroid: Datos del asteroide
            
        Returns:
            "HIGH", "MEDIUM", o "LOW"
        """
        
        score = 0
        
        # Factor tamaño
        diameter = asteroid.get("diameter_km_avg", 0)
        if diameter > 1:
            score += 3
        elif diameter > 0.5:
            score += 2
        elif diameter > 0.1:
            score += 1
        
        # Factor velocidad
        velocity = asteroid.get("velocity_kms", 0)
        if velocity > 20:
            score += 3
        elif velocity > 15:
            score += 2
        elif velocity > 10:
            score += 1
        
        # Factor distancia
        distance_au = asteroid.get("distance_au", float('inf'))
        if distance_au < 0.05:  # < 0.05 AU
            score += 3
        elif distance_au < 0.1:   # < 0.1 AU
            score += 2
        elif distance_au < 0.2:   # < 0.2 AU
            score += 1
        
        # Asteroide potencialmente peligroso
        if asteroid.get("is_potentially_hazardous", False):
            score += 2
        
        # Clasificar riesgo
        if score >= 7:
            return "HIGH"
        elif score >= 4:
            return "MEDIUM"
        else:
            return "LOW"
    
    def get_potentially_hazardous_asteroids(self, page: int = 0, size: int = 20) -> Dict[str, Any]:
        """
        Obtener lista de asteroides potencialmente peligrosos
        
        Args:
            page: Página de resultados
            size: Tamaño de página
            
        Returns:
            Dict con asteroides peligrosos
        """
        
        url = f"{self.base_urls['neo']}/neo/browse"
        params = {
            "page": page,
            "size": size
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al obtener asteroides peligrosos: {e}")
            return {}

class AsteroidDataProcessor:
    """Procesador de datos de asteroides para el sistema"""
    
    def __init__(self, nasa_service: NASAApiService):
        self.nasa_service = nasa_service
    
    def get_current_threats(self) -> List[Dict[str, Any]]:
        """
        Obtener amenazas actuales y próximas
        
        Returns:
            Lista de asteroides amenazantes
        """
        
        # Obtener datos de los próximos 30 días
        end_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        neo_data = self.nasa_service.get_neo_feed(end_date=end_date)
        
        # Parsear y filtrar amenazas
        asteroids = self.nasa_service.parse_neo_data(neo_data)
        
        # Filtrar solo amenazas significativas
        threats = [
            asteroid for asteroid in asteroids
            if asteroid.get("risk_level") in ["HIGH", "MEDIUM"] or
               asteroid.get("is_potentially_hazardous", False)
        ]
        
        # Ordenar por nivel de riesgo y proximidad
        threats.sort(key=lambda x: (
            {"HIGH": 3, "MEDIUM": 2, "LOW": 1}.get(x.get("risk_level", "LOW"), 1),
            -x.get("distance_au", float('inf'))
        ), reverse=True)
        
        return threats
    
    def enrich_asteroid_data(self, asteroid: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enriquecer datos del asteroide con información adicional
        
        Args:
            asteroid: Datos básicos del asteroide
            
        Returns:
            Asteroide con datos enriquecidos
        """
        
        # Obtener datos detallados si tenemos ID
        if asteroid.get("neo_reference_id"):
            detailed_data = self.nasa_service.get_asteroid_details(
                asteroid["neo_reference_id"]
            )
            
            if detailed_data:
                # Agregar datos orbitales
                orbital_data = detailed_data.get("orbital_data", {})
                asteroid["orbital_period"] = orbital_data.get("orbital_period")
                asteroid["minimum_orbit_intersection"] = orbital_data.get("minimum_orbit_intersection")
                asteroid["jupiter_tisserand_invariant"] = orbital_data.get("jupiter_tisserand_invariant")
                
                # Agregar más aproximaciones cercanas
                asteroid["close_approach_data"] = detailed_data.get("close_approach_data", [])
        
        return asteroid

# Función de conveniencia
def get_nasa_asteroids(api_key: str = None, days_ahead: int = 30) -> List[Dict[str, Any]]:
    """
    Función conveniente para obtener datos de asteroides de NASA
    
    Args:
        api_key: Clave API de NASA (opcional)
        days_ahead: Días hacia adelante para buscar (por defecto 30)
        
    Returns:
        Lista de asteroides procesados
    """
    
    nasa_service = NASAApiService(api_key)
    processor = AsteroidDataProcessor(nasa_service)
    
    return processor.get_current_threats()