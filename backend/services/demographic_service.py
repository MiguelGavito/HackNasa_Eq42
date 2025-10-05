"""
Servicio de cálculo demográfico para estimación de víctimas por impacto de asteroide
Utiliza datos de población mundial por coordenadas geográficas
"""

import math
import requests
from typing import Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)

class DemographicService:
    """Servicio para calcular densidad poblacional y estimar víctimas"""
    
    def __init__(self):
        """Inicializar servicio demográfico"""
        # APIs disponibles para datos demográficos
        self.population_apis = {
            "worldpop": "https://api.worldpop.org",  # WorldPop - datos de población global
            "geonames": "http://api.geonames.org",   # GeoNames - datos geográficos
            "rest_countries": "https://restcountries.com/v3.1"  # Datos de países
        }
        
        # Densidades poblacionales estimadas por región (personas/km²)
        self.regional_density_estimates = {
            # Ciudades principales (muy alta densidad)
            "urban_major": 10000,      # Nueva York, Tokio, Mumbai, etc.
            "urban_large": 5000,       # Ciudades grandes
            "urban_medium": 2500,      # Ciudades medianas
            "urban_small": 1000,       # Ciudades pequeñas
            
            # Áreas rurales
            "suburban": 500,           # Suburbios
            "rural_populated": 100,    # Rural poblado
            "rural_sparse": 25,        # Rural disperso
            
            # Áreas especiales
            "agricultural": 150,       # Zonas agrícolas
            "coastal": 300,           # Zonas costeras
            "mountain": 10,           # Montañas
            "desert": 1,              # Desiertos
            "ocean": 0,               # Océanos
            "arctic": 0.1             # Ártico/Antártico
        }
        
        # Coordenadas de ciudades principales del mundo
        self.major_cities = {
            # Asia
            "tokyo": {"lat": 35.6762, "lon": 139.6503, "population": 37400000, "density": 15000},
            "delhi": {"lat": 28.7041, "lon": 77.1025, "population": 30290000, "density": 11000},
            "shanghai": {"lat": 31.2304, "lon": 121.4737, "population": 27058000, "density": 7700},
            "dhaka": {"lat": 23.8103, "lon": 90.4125, "population": 21005000, "density": 23000},
            "mumbai": {"lat": 19.0760, "lon": 72.8777, "population": 20411000, "density": 32000},
            "beijing": {"lat": 39.9042, "lon": 116.4074, "population": 20035000, "density": 1300},
            
            # América
            "new_york": {"lat": 40.7128, "lon": -74.0060, "population": 18804000, "density": 11000},
            "mexico_city": {"lat": 19.4326, "lon": -99.1332, "population": 21782000, "density": 9600},
            "sao_paulo": {"lat": -23.5505, "lon": -46.6333, "population": 22043000, "density": 8000},
            "los_angeles": {"lat": 34.0522, "lon": -118.2437, "population": 12458000, "density": 3200},
            
            # Europa
            "london": {"lat": 51.5074, "lon": -0.1278, "population": 9304000, "density": 5700},
            "paris": {"lat": 48.8566, "lon": 2.3522, "population": 11017000, "density": 8900},
            "moscow": {"lat": 55.7558, "lon": 37.6176, "population": 12506000, "density": 5000},
            
            # África
            "cairo": {"lat": 30.0444, "lon": 31.2357, "population": 20484000, "density": 15000},
            "lagos": {"lat": 6.5244, "lon": 3.3792, "population": 14368000, "density": 18000},
            
            # Oceanía
            "sydney": {"lat": -33.8688, "lon": 151.2093, "population": 5312000, "density": 2100}
        }
    
    def calculate_population_density(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Calcular densidad poblacional estimada para coordenadas específicas
        Usa APIs reales cuando es posible, fallback a estimaciones locales
        
        Args:
            lat: Latitud
            lon: Longitud
            
        Returns:
            Dict con información demográfica
        """
        try:
            # Determinar si está en océano
            if self._is_ocean(lat, lon):
                return {
                    "density_per_km2": 0,
                    "region_type": "ocean",
                    "nearest_major_city": None,
                    "estimated_population_50km": 0,
                    "country": "Ocean",
                    "data_source": "local_estimation"
                }
            
            # Intentar obtener datos reales primero
            real_data = self._get_real_demographic_data(lat, lon)
            if real_data:
                return real_data
            
            # Fallback a estimaciones locales
            logger.info(f"Usando estimaciones locales para {lat}, {lon}")
            
            # Buscar ciudad principal más cercana
            nearest_city = self._find_nearest_major_city(lat, lon)
            
            # Determinar tipo de región basado en proximidad a ciudades
            region_info = self._classify_region(lat, lon, nearest_city)
            
            # Calcular población estimada en radio de 50km
            population_50km = self._estimate_population_in_radius(lat, lon, 50, region_info["density"])
            
            return {
                "density_per_km2": region_info["density"],
                "region_type": region_info["type"],
                "nearest_major_city": nearest_city,
                "estimated_population_50km": population_50km,
                "country": self._estimate_country(lat, lon),
                "coordinates": {"lat": lat, "lon": lon},
                "data_source": "local_estimation"
            }
            
        except Exception as e:
            logger.error(f"Error calculando densidad poblacional: {e}")
            # Retornar estimación básica
            return {
                "density_per_km2": 50,  # Densidad promedio mundial
                "region_type": "unknown",
                "nearest_major_city": None,
                "estimated_population_50km": 392000,  # π × 50² × 50
                "country": "Unknown"
            }
    
    def estimate_casualties(self, lat: float, lon: float, crater_diameter_km: float, 
                          energy_megatons: float) -> Dict[str, Any]:
        """
        Estimar víctimas basado en ubicación del impacto
        
        Args:
            lat: Latitud del impacto
            lon: Longitud del impacto
            crater_diameter_km: Diámetro del cráter en km
            energy_megatons: Energía liberada en megatones TNT
            
        Returns:
            Dict con estimaciones de víctimas
        """
        try:
            # Verificar tamaño mínimo para impacto significativo
            if crater_diameter_km < 0.01:
                return {
                    "total_casualties": 0,
                    "total_affected_population": 0,
                    "note": "Impacto demasiado pequeño para causar víctimas significativas"
                }
            
            # Obtener información demográfica
            demo_info = self.calculate_population_density(lat, lon)
            
            # Calcular zonas de impacto (radios más realistas)
            immediate_radius = crater_diameter_km / 2  # Radio de destrucción total
            severe_damage_radius = crater_diameter_km * 2  # Daño severo  
            moderate_damage_radius = crater_diameter_km * 4  # Daño moderado
            
            # DEBUG: Mostrar qué densidad estamos usando
            density = demo_info["density_per_km2"]
            logger.info(f"DEBUG - Ubicación: {lat},{lon} | Densidad: {density} p/km² | Tipo: {demo_info.get('region_type', 'unknown')} | Fuente: {demo_info.get('data_source', 'unknown')}")
            
            # Calcular población en cada zona
            immediate_pop = self._estimate_population_in_radius(lat, lon, immediate_radius, density)
            severe_pop = self._estimate_population_in_radius(lat, lon, severe_damage_radius, density)
            moderate_pop = self._estimate_population_in_radius(lat, lon, moderate_damage_radius, density)
            
            # Factor de escalado basado en energía (impactos pequeños son menos letales)
            energy_factor = min(1.0, max(0.1, energy_megatons / 100.0))
            
            # DEBUG: Mostrar cálculos intermedios
            logger.info(f"DEBUG - Radios: inmediato={immediate_radius:.2f}km, severo={severe_damage_radius:.2f}km, moderado={moderate_damage_radius:.2f}km")
            logger.info(f"DEBUG - Poblaciones: inmediata={immediate_pop:.0f}, severa={severe_pop:.0f}, moderada={moderate_pop:.0f}")
            logger.info(f"DEBUG - Factor energía: {energy_factor:.3f} (de {energy_megatons:.2f} MT)")
            
            # Calcular letalidad basada en distancia real del impacto
            immediate_casualties = self._calculate_casualties_by_distance(
                lat, lon, immediate_radius, immediate_pop, 0.85, energy_factor
            )
            severe_casualties = self._calculate_casualties_by_distance(
                lat, lon, severe_damage_radius, severe_pop - immediate_pop, 0.45, energy_factor
            )
            moderate_casualties = self._calculate_casualties_by_distance(
                lat, lon, moderate_damage_radius, moderate_pop - severe_pop, 0.08, energy_factor
            )
            
            total_casualties = immediate_casualties + severe_casualties + moderate_casualties
            total_affected = int(moderate_pop)
            
            # Factores adicionales por tipo de región
            if demo_info["region_type"] == "ocean":
                # Impacto oceánico: tsunamis
                tsunami_casualties = self._estimate_tsunami_casualties(lat, lon, energy_megatons)
                total_casualties += tsunami_casualties
            
            return {
                "total_casualties": total_casualties,
                "total_affected_population": total_affected,
                "casualties_by_zone": {
                    "immediate_zone": {
                        "radius_km": immediate_radius,
                        "population": int(immediate_pop),
                        "casualties": immediate_casualties,
                        "mortality_rate": 0.95
                    },
                    "severe_damage_zone": {
                        "radius_km": severe_damage_radius,
                        "population": int(severe_pop - immediate_pop),
                        "casualties": severe_casualties,
                        "mortality_rate": 0.60
                    },
                    "moderate_damage_zone": {
                        "radius_km": moderate_damage_radius,
                        "population": int(moderate_pop - severe_pop),
                        "casualties": moderate_casualties,
                        "mortality_rate": 0.15
                    }
                },
                "region_info": demo_info,
                "additional_effects": {
                    "tsunami_risk": demo_info["region_type"] == "ocean",
                    "wildfire_risk": demo_info["region_type"] in ["rural_populated", "agricultural"],
                    "infrastructure_damage": demo_info["region_type"] in ["urban_major", "urban_large"]
                }
            }
            
        except Exception as e:
            logger.error(f"Error estimando víctimas: {e}")
            return {
                "total_casualties": int(crater_diameter_km ** 2 * 1000),  # Estimación básica
                "error": str(e)
            }
    
    def _is_ocean(self, lat: float, lon: float) -> bool:
        """Determinar si las coordenadas están en océano usando áreas continentales conocidas"""
        
        # Definir continentes principales con rangos corregidos y más precisos
        
        # América del Norte (incluyendo Groenlandia, Alaska, Centroamérica)
        if 10 < lat < 85 and -180 < lon < -50:
            return False
            
        # América del Sur (incluyendo islas del Caribe)
        if -60 < lat < 15 and -90 < lon < -30:
            return False
            
        # Europa (incluyendo Islandia, Reino Unido, Escandinavia)
        if 35 < lat < 75 and -30 < lon < 60:
            return False
            
        # África (incluyendo Madagascar y islas cercanas)  
        if -40 < lat < 40 and -25 < lon < 60:
            return False
            
        # Asia (incluyendo Rusia, China, India, Indonesia, Japón)
        if -15 < lat < 85 and 25 < lon < 180:
            return False
            
        # Australia/Oceanía (incluyendo Nueva Zelanda y islas del Pacífico)
        if -55 < lat < -5 and 110 < lon < 180:
            return False
            
        # Antártida
        if lat < -60:
            return False
            
        # Si no está en ningún continente, es océano
        return True
    
    def _find_nearest_major_city(self, lat: float, lon: float) -> Dict[str, Any]:
        """Encontrar la ciudad principal más cercana"""
        min_distance = float('inf')
        nearest_city = None
        
        for city_name, city_data in self.major_cities.items():
            distance = self._calculate_distance(lat, lon, city_data["lat"], city_data["lon"])
            if distance < min_distance:
                min_distance = distance
                nearest_city = {
                    "name": city_name,
                    "distance_km": distance,
                    "population": city_data["population"],
                    "density": city_data["density"]
                }
        
        return nearest_city
    
    def _classify_region(self, lat: float, lon: float, nearest_city: Dict) -> Dict[str, Any]:
        """Clasificar tipo de región basado en proximidad a ciudades"""
        if not nearest_city:
            return {"type": "rural_sparse", "density": self.regional_density_estimates["rural_sparse"]}
        
        distance = nearest_city["distance_km"]
        city_population = nearest_city["population"]
        
        # Clasificación basada en distancia y tamaño de ciudad
        if distance < 25 and city_population > 20000000:
            return {"type": "urban_major", "density": self.regional_density_estimates["urban_major"]}
        elif distance < 50 and city_population > 10000000:
            return {"type": "urban_large", "density": self.regional_density_estimates["urban_large"]}
        elif distance < 100 and city_population > 5000000:
            return {"type": "urban_medium", "density": self.regional_density_estimates["urban_medium"]}
        elif distance < 200 and city_population > 1000000:
            return {"type": "suburban", "density": self.regional_density_estimates["suburban"]}
        elif distance < 500:
            return {"type": "rural_populated", "density": self.regional_density_estimates["rural_populated"]}
        else:
            return {"type": "rural_sparse", "density": self.regional_density_estimates["rural_sparse"]}
    
    def _estimate_population_in_radius(self, lat: float, lon: float, radius_km: float, density: float) -> float:
        """Estimar población en un radio específico usando áreas graduales"""
        # Área básica circular
        area_km2 = math.pi * (radius_km ** 2)
        base_population = area_km2 * density
        
        # Factor de corrección por distribución no uniforme
        # En ciudades reales, la densidad no es uniforme - más densa en el centro
        if density > 10000:  # Ciudades muy densas
            distribution_factor = 0.7  # 70% de la densidad teórica
        elif density > 1000:  # Ciudades medianas
            distribution_factor = 0.8  # 80% de la densidad teórica
        else:  # Áreas rurales
            distribution_factor = 0.9  # 90% de la densidad teórica (más uniforme)
            
        return base_population * distribution_factor
    
    def _estimate_tsunami_casualties(self, lat: float, lon: float, energy_megatons: float) -> int:
        """Estimar víctimas adicionales por tsunami (impactos oceánicos)"""
        if energy_megatons < 50:
            return 0  # Sin tsunamis significativos
        elif energy_megatons < 500:
            return int(energy_megatons * 100)  # 100 víctimas por megatón
        elif energy_megatons < 2000:
            return int(energy_megatons * 150)  # Tsunami regional
        else:
            return int(energy_megatons * 200)  # Máximo 200 víctimas por megatón
    
    def _estimate_country(self, lat: float, lon: float) -> str:
        """Estimación simplificada de país basada en coordenadas"""
        # Simplificado - en producción usaríamos una API real
        if 24 < lat < 49 and -125 < lon < -66:
            return "United States"
        elif 35 < lat < 71 and -10 < lon < 40:
            return "Europe"
        elif -35 < lat < 35 and 70 < lon < 140:
            return "Asia"
        elif -35 < lat < 37 and -20 < lon < 55:
            return "Africa"
        elif -55 < lat < -10 and -75 < lon < -35:
            return "South America"
        else:
            return "Other"
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calcular distancia entre dos puntos en km usando fórmula haversine"""
        R = 6371  # Radio de la Tierra en km
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat / 2) ** 2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    def _calculate_casualties_by_distance(self, impact_lat: float, impact_lon: float, 
                                        radius_km: float, population: float, 
                                        base_mortality: float, energy_factor: float) -> int:
        """
        Calcular víctimas basado en distancia real del impacto con letalidad degradada
        
        Args:
            impact_lat: Latitud del impacto
            impact_lon: Longitud del impacto  
            radius_km: Radio de la zona de daño
            population: Población en la zona
            base_mortality: Tasa de mortalidad base para la zona
            energy_factor: Factor de escalado por energía
            
        Returns:
            Número de víctimas estimadas
        """
        if population <= 0:
            return 0
            
        # Simular distribución de población dentro del radio
        # En lugar de asumir mortalidad uniforme, usar degradación por distancia
        
        total_casualties = 0
        
        # Dividir el área en anillos concéntricos para simular distancia variable
        num_rings = max(3, int(radius_km))  # Mínimo 3 anillos, más para áreas grandes
        
        for ring in range(num_rings):
            ring_inner_radius = (ring / num_rings) * radius_km
            ring_outer_radius = ((ring + 1) / num_rings) * radius_km
            
            # Population in this ring (proportional to area)
            ring_area = math.pi * (ring_outer_radius**2 - ring_inner_radius**2)
            total_area = math.pi * radius_km**2
            ring_population = population * (ring_area / total_area)
            
            # Letalidad degradada por distancia
            avg_distance = (ring_inner_radius + ring_outer_radius) / 2
            distance_factor = max(0.1, 1 - (avg_distance / radius_km) * 0.5)  # Reduce 50% en el borde
            
            # Mortalidad final para este anillo
            ring_mortality = base_mortality * distance_factor * energy_factor
            ring_casualties = int(ring_population * ring_mortality)
            
            total_casualties += ring_casualties
            
        return total_casualties
    
    def _get_real_demographic_data(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Obtener datos demográficos reales usando Nominatim API (OpenStreetMap)
        
        Args:
            lat: Latitud
            lon: Longitud
            
        Returns:
            Dict con datos reales o None si falla
        """
        try:
            # Usar Nominatim directamente - es gratuito y confiable
            nominatim_data = self._query_nominatim_api(lat, lon)
            if nominatim_data:
                return nominatim_data
                
        except Exception as e:
            logger.warning(f"Error obteniendo datos reales para {lat}, {lon}: {e}")
        
        return None
    
    def _query_geonames_api(self, lat: float, lon: float) -> Dict[str, Any]:
        """Consultar GeoNames API para obtener datos de población"""
        try:
            # Nota: Necesitas registrarte en geonames.org para obtener un username
            # Por ahora usamos datos de demostración
            url = f"http://api.geonames.org/findNearbyPlaceName"
            params = {
                "lat": lat,
                "lng": lon,
                "username": "demo",  # Cambiar por tu username real
                "maxRows": 5,
                "radius": 50,
                "style": "full"
            }
            
            # GeoNames necesita registro, saltamos por ahora
            pass
            
        except Exception as e:
            logger.error(f"Error consultando GeoNames: {e}")
        
        return None
    
    def _query_nominatim_api(self, lat: float, lon: float) -> Dict[str, Any]:
        """Consultar Nominatim (OpenStreetMap) para información geográfica"""
        try:
            url = "https://nominatim.openstreetmap.org/reverse"
            params = {
                "format": "json",
                "lat": lat,
                "lon": lon,
                "zoom": 10,
                "addressdetails": 1
            }
            headers = {
                "User-Agent": "MeteorMadness-HackNASA/1.0"
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return self._process_nominatim_response(data, lat, lon)
                
        except Exception as e:
            logger.error(f"Error consultando Nominatim: {e}")
        
        return None
    
    def _process_nominatim_response(self, data: dict, lat: float, lon: float) -> Dict[str, Any]:
        """Procesar respuesta de Nominatim para extraer datos demográficos"""
        try:
            display_name = data.get("display_name", "")
            address = data.get("address", {})
            
            # Determinar tipo de área basado en la respuesta
            place_type = data.get("type", "unknown")
            osm_type = data.get("osm_type", "unknown")
            
            # Clasificar densidad basada en tipo de lugar
            density = self._estimate_density_from_osm_data(address, place_type)
            region_type = self._classify_region_from_address(address)
            
            # Estimar país
            country = address.get("country", "Unknown")
            
            # Calcular población estimada
            population_50km = self._estimate_population_in_radius(lat, lon, 50, density)
            
            return {
                "density_per_km2": density,
                "region_type": region_type,
                "nearest_major_city": {
                    "name": address.get("city", address.get("town", address.get("village", "Unknown"))),
                    "distance_km": 0,  # Estimado
                    "population": "unknown"
                },
                "estimated_population_50km": population_50km,
                "country": country,
                "coordinates": {"lat": lat, "lon": lon},
                "data_source": "nominatim_osm",
                "location_info": {
                    "display_name": display_name,
                    "place_type": place_type,
                    "osm_type": osm_type
                }
            }
            
        except Exception as e:
            logger.error(f"Error procesando respuesta Nominatim: {e}")
            return None
    
    def _estimate_density_from_osm_data(self, address: dict, place_type: str) -> float:
        """Estimar densidad poblacional basada en datos de OpenStreetMap con precisión mejorada"""
        
        # Obtener nombre de ciudad/estado/país para clasificación precisa
        city = address.get("city", "").lower()
        state = address.get("state", "").lower()
        country = address.get("country", "").lower()
        
        # Megaciudades específicas (densidad muy alta)
        megacities = {
            "new york": 28000, "manhattan": 74000, "brooklyn": 15000,
            "tokyo": 15000, "mumbai": 32000, "delhi": 29000,
            "shanghai": 7700, "london": 5700, "paris": 8900,
            "mexico city": 9600, "são paulo": 8000, "cairo": 15000,
            "lagos": 18000, "dhaka": 23000, "beijing": 1300,
            "los angeles": 3200, "chicago": 4600, "houston": 1400
        }
        
        for mega_city, density in megacities.items():
            if mega_city in city:
                return density
        
        # Clasificación por tipo de lugar y contexto
        if place_type in ["city", "town"]:
            # Ciudades por país/región
            if country in ["united states", "usa"]:
                if "new york" in state or "california" in state:
                    return 2500  # Estados densamente poblados
                else:
                    return 800   # Ciudades americanas típicas
            elif country in ["japan", "south korea", "singapore"]:
                return 8000      # Países asiáticos densos
            elif country in ["india", "bangladesh", "china"]:
                return 12000     # Países súper poblados
            elif country in ["germany", "netherlands", "belgium"]:
                return 3500      # Europa densa
            else:
                return 1500      # Ciudades promedio mundial
                
        elif place_type in ["village", "hamlet"]:
            if country in ["india", "bangladesh", "china"]:
                return 500       # Pueblos asiáticos densos
            else:
                return 50        # Pueblos típicos
                
        elif place_type in ["suburb", "neighbourhood"]:
            if country in ["united states", "canada", "australia"]:
                return 800       # Suburbios occidentales
            else:
                return 1200      # Suburbios internacionales
                
        elif place_type in ["industrial", "commercial"]:
            return 300           # Zonas industriales (menos gente vive ahí)
            
        elif place_type in ["farmland", "forest", "natural", "water"]:
            return 2             # Zonas naturales/rurales
            
        else:
            # Default basado en país
            if country in ["monaco", "singapore", "hong kong"]:
                return 20000     # Países/ciudades-estado muy densos
            elif country in ["bangladesh", "south korea", "taiwan"]:
                return 1200      # Países densos
            elif country in ["india", "china", "japan", "philippines"]:
                return 400       # Países poblados
            elif country in ["united states", "canada", "australia"]:
                return 35        # Países con mucho espacio
            else:
                return 150       # Promedio mundial
    
    def _classify_region_from_address(self, address: dict) -> str:
        """Clasificar tipo de región basado en dirección de OSM"""
        
        if address.get("city") or address.get("town"):
            population_indicators = address.get("city", address.get("town", "")).lower()
            if any(city in population_indicators for city in ["new york", "tokyo", "london", "paris", "mumbai", "beijing"]):
                return "urban_major"
            elif address.get("city"):
                return "urban_large"
            else:
                return "urban_medium"
        elif address.get("village") or address.get("hamlet"):
            return "rural_populated"
        elif address.get("suburb"):
            return "suburban"
        else:
            return "rural_sparse"