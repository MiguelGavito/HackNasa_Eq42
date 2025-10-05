#!/usr/bin/env python3
"""
Test simple para verificar que la API de demografía funciona
"""

import sys
sys.path.append('.')
from services.demographic_service import DemographicService
import logging

# Activar logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def test_api_direct():
    demo_service = DemographicService()
    
    print("=" * 60)
    print("TEST DIRECTO DE API DEMOGRÁFICA")
    print("=" * 60)
    
    # Test 1: NYC
    print("\n1. TESTANDO NYC (40.7128, -74.0060)")
    nyc_data = demo_service.calculate_population_density(40.7128, -74.0060)
    print(f"Densidad NYC: {nyc_data['density_per_km2']} personas/km²")
    print(f"Tipo región: {nyc_data['region_type']}")
    print(f"Fuente datos: {nyc_data.get('data_source', 'no_source')}")
    print(f"País: {nyc_data.get('country', 'unknown')}")
    if 'location_info' in nyc_data:
        print(f"Info ubicación: {nyc_data['location_info']}")
    
    # Test 2: Área Rural (Dakota del Norte)
    print("\n2. TESTANDO ÁREA RURAL (45.0, -100.0)")
    rural_data = demo_service.calculate_population_density(45.0, -100.0)
    print(f"Densidad Rural: {rural_data['density_per_km2']} personas/km²")
    print(f"Tipo región: {rural_data['region_type']}")
    print(f"Fuente datos: {rural_data.get('data_source', 'no_source')}")
    print(f"País: {rural_data.get('country', 'unknown')}")
    if 'location_info' in rural_data:
        print(f"Info ubicación: {rural_data['location_info']}")
    
    # Test 3: Océano
    print("\n3. TESTANDO OCÉANO (30.0, -60.0)")
    ocean_data = demo_service.calculate_population_density(30.0, -60.0)
    print(f"Densidad Océano: {ocean_data['density_per_km2']} personas/km²")
    print(f"Tipo región: {ocean_data['region_type']}")
    print(f"Fuente datos: {ocean_data.get('data_source', 'no_source')}")
    
    print("\n" + "=" * 60)
    print("RESUMEN:")
    print(f"NYC: {nyc_data['density_per_km2']} p/km² - {nyc_data.get('data_source', 'unknown')}")
    print(f"Rural: {rural_data['density_per_km2']} p/km² - {rural_data.get('data_source', 'unknown')}")
    print(f"Océano: {ocean_data['density_per_km2']} p/km² - {ocean_data.get('data_source', 'unknown')}")
    print("=" * 60)

if __name__ == "__main__":
    test_api_direct()