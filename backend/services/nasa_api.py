"""
Integración con APIs de la NASA
Servicio para obtener datos reales de asteroides cercanos a la Tierra
"""

import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import json
import logging
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NASAApiService:
    """Servicio para interactuar con las APIs de la NASA"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializar el servicio de NASA API
        
        Args:
            api_key: Clave API de NASA (opcional, carga desde .env)
        """
        self.api_key = api_key or os.getenv('NASA_API_KEY', 'DEMO_KEY')
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
    
    def get_processed_asteroids(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Obtener asteroides procesados y limitados para la aplicación
        
        Args:
            limit: Número máximo de asteroides a devolver
            
        Returns:
            Lista de asteroides procesados y listos para usar
        """
        try:
            # Obtener datos RAW de NASA (últimos 7 días)
            raw_data = self.get_neo_feed()
            
            # Procesar asteroides recientes
            processed_asteroids = []
            if raw_data and 'near_earth_objects' in raw_data:
                neo_objects = raw_data['near_earth_objects']
                
                # Iterar por todas las fechas y asteroides
                for date_key, asteroids_list in neo_objects.items():
                    for asteroid in asteroids_list:
                        try:
                            processed_asteroid = self._process_asteroid_data(asteroid)
                            if processed_asteroid:
                                processed_asteroids.append(processed_asteroid)
                        except Exception as e:
                            logger.warning(f"Error procesando asteroide {asteroid.get('id', 'unknown')}: {e}")
                            continue
            
            # Agregar algunos asteroides históricos peligrosos conocidos para demo
            historical_dangerous = self._get_historical_dangerous_asteroids()
            processed_asteroids.extend(historical_dangerous)
            
            # Remover duplicados por ID
            seen_ids = set()
            unique_asteroids = []
            for asteroid in processed_asteroids:
                if asteroid['id'] not in seen_ids:
                    seen_ids.add(asteroid['id'])
                    unique_asteroids.append(asteroid)
            
            # Ordenar: primero peligrosos, luego por tamaño
            unique_asteroids.sort(key=lambda x: (
                -int(x.get('is_potentially_hazardous_asteroid', False)),
                -x.get('estimated_diameter_km_max', 0)
            ))
            
            total_found = len(unique_asteroids)
            result = unique_asteroids[:limit]
            
            logger.info(f"Procesados {len(result)} asteroides de {total_found} únicos encontrados")
            return result
            
        except Exception as e:
            logger.error(f"Error procesando asteroides: {e}")
            return []
    
    def _get_historical_dangerous_asteroids(self) -> List[Dict[str, Any]]:
        """
        Obtener asteroides históricos peligrosos conocidos para la demostración
        
        Returns:
            Lista de asteroides históricos con datos realistas
        """
        return [
            {
                'id': '99942',
                'name': '99942 Apophis',
                'estimated_diameter_km_min': 0.325,
                'estimated_diameter_km_max': 0.375,
                'relative_velocity_km_s': 7.42,
                'miss_distance_km': 31000,
                'is_potentially_hazardous_asteroid': True,
                'close_approach_date': '2029-04-13',
                'nasa_jpl_url': 'https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html#/?sstr=99942',
                'absolute_magnitude_h': 19.7
            },
            {
                'id': '101955',
                'name': '101955 Bennu',
                'estimated_diameter_km_min': 0.492,
                'estimated_diameter_km_max': 0.565,
                'relative_velocity_km_s': 11.16,
                'miss_distance_km': 480000,
                'is_potentially_hazardous_asteroid': True,
                'close_approach_date': '2182-09-25',
                'nasa_jpl_url': 'https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html#/?sstr=101955',
                'absolute_magnitude_h': 20.9
            },
            {
                'id': '1036',
                'name': '1036 Ganymed',
                'estimated_diameter_km_min': 31.7,
                'estimated_diameter_km_max': 35.1,
                'relative_velocity_km_s': 13.63,
                'miss_distance_km': 56000000,
                'is_potentially_hazardous_asteroid': True,
                'close_approach_date': '2024-10-13',
                'nasa_jpl_url': 'https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html#/?sstr=1036',
                'absolute_magnitude_h': 9.45
            },
            {
                'id': '4179',
                'name': '4179 Toutatis',
                'estimated_diameter_km_min': 2.5,
                'estimated_diameter_km_max': 5.4,
                'relative_velocity_km_s': 11.02,
                'miss_distance_km': 18000000,
                'is_potentially_hazardous_asteroid': True,
                'close_approach_date': '2004-09-29',
                'nasa_jpl_url': 'https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html#/?sstr=4179',
                'absolute_magnitude_h': 15.3
            },
            {
                'id': '2022_AP7',
                'name': '2022 AP7',
                'estimated_diameter_km_min': 1.1,
                'estimated_diameter_km_max': 2.3,
                'relative_velocity_km_s': 8.15,
                'miss_distance_km': 4200000,
                'is_potentially_hazardous_asteroid': True,
                'close_approach_date': '2022-01-07',
                'nasa_jpl_url': 'https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html#/?sstr=2022_AP7',
                'absolute_magnitude_h': 15.6
            }
        ]
    
    def _process_asteroid_data(self, asteroid: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Procesar datos de un asteroide individual
        
        Args:
            asteroid: Datos RAW del asteroide desde NASA API
            
        Returns:
            Datos procesados del asteroide o None si hay error
        """
        try:
            # Obtener datos de aproximación más cercana
            close_approach = asteroid.get('close_approach_data', [{}])[0]
            
            # Extraer diámetros
            diameter_data = asteroid.get('estimated_diameter', {}).get('kilometers', {})
            diameter_min = diameter_data.get('estimated_diameter_min', 0)
            diameter_max = diameter_data.get('estimated_diameter_max', 0)
            
            # Extraer velocidad y distancia
            velocity_kmh = float(close_approach.get('relative_velocity', {}).get('kilometers_per_hour', 0))
            velocity_kms = velocity_kmh / 3600  # Convertir a km/s
            
            distance_km = float(close_approach.get('miss_distance', {}).get('kilometers', 0))
            
            return {
                'id': asteroid.get('id', ''),
                'name': asteroid.get('name', '').replace('(', '').replace(')', ''),
                'estimated_diameter_km_min': round(diameter_min, 3),
                'estimated_diameter_km_max': round(diameter_max, 3),
                'relative_velocity_km_s': round(velocity_kms, 2),
                'miss_distance_km': round(distance_km, 0),
                'is_potentially_hazardous_asteroid': asteroid.get('is_potentially_hazardous_asteroid', False),
                'close_approach_date': close_approach.get('close_approach_date', ''),
                'nasa_jpl_url': asteroid.get('nasa_jpl_url', ''),
                'absolute_magnitude_h': asteroid.get('absolute_magnitude_h', 0)
            }
            
        except Exception as e:
            logger.warning(f"Error procesando datos del asteroide: {e}")
            return None
    
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