#!/usr/bin/env python3
"""
Script de prueba para verificar los cálculos de víctimas corregidos
"""

import sys
sys.path.append('.')
from services.demographic_service import DemographicService
import math
import logging

# Activar logging para ver los debug messages
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def test_casualties():
    demo_service = DemographicService()
    
    print("=" * 60)
    print("PRUEBA DE CÁLCULOS DE VÍCTIMAS CORREGIDOS")
    print("=" * 60)
    
    # Test 1: Meteorito muy pequeño (50 metros)
    print("\n1. METEORITO MUY PEQUEÑO (50 metros)")
    diameter_km = 0.05
    velocity = 15.0
    crater_diameter_km = 1.8 * diameter_km * (velocity / 12)**0.78
    
    volume = (4/3) * math.pi * (diameter_km/2)**3
    mass = volume * 2.5e12
    energy_joules = 0.5 * mass * (velocity * 1000)**2
    energy_megatons = energy_joules / 4.184e15
    
    print(f"Diámetro meteorito: {diameter_km} km ({diameter_km*1000} metros)")
    print(f"Velocidad: {velocity} km/s")
    print(f"Cráter calculado: {crater_diameter_km:.4f} km ({crater_diameter_km*1000:.1f} metros)")
    print(f"Energía: {energy_megatons:.4f} megatones")
    
    # Test en NYC
    casualties = demo_service.estimate_casualties(40.7128, -74.0060, crater_diameter_km, energy_megatons)
    print(f"  -> NYC: {casualties.get('total_casualties', 0):,} víctimas")
    
    # Test en área rural
    casualties = demo_service.estimate_casualties(45.0, -100.0, crater_diameter_km, energy_megatons)
    print(f"  -> Rural: {casualties.get('total_casualties', 0):,} víctimas")
    
    # Test 2: Meteorito pequeño (100 metros)
    print("\n2. METEORITO PEQUEÑO (100 metros)")
    diameter_km = 0.1
    velocity = 20.0
    crater_diameter_km = 1.8 * diameter_km * (velocity / 12)**0.78
    
    volume = (4/3) * math.pi * (diameter_km/2)**3
    mass = volume * 2.5e12
    energy_joules = 0.5 * mass * (velocity * 1000)**2
    energy_megatons = energy_joules / 4.184e15
    
    print(f"Diámetro meteorito: {diameter_km} km ({diameter_km*1000} metros)")
    print(f"Velocidad: {velocity} km/s")
    print(f"Cráter calculado: {crater_diameter_km:.4f} km ({crater_diameter_km*1000:.1f} metros)")
    print(f"Energía: {energy_megatons:.4f} megatones")
    
    # Test en NYC
    casualties = demo_service.estimate_casualties(40.7128, -74.0060, crater_diameter_km, energy_megatons)
    print(f"  -> NYC: {casualties.get('total_casualties', 0):,} víctimas")
    
    # Test en área rural
    casualties = demo_service.estimate_casualties(45.0, -100.0, crater_diameter_km, energy_megatons)
    print(f"  -> Rural: {casualties.get('total_casualties', 0):,} víctimas")
    
    # Test 3: Meteorito mediano (500 metros)
    print("\n3. METEORITO MEDIANO (500 metros)")
    diameter_km = 0.5
    velocity = 25.0
    crater_diameter_km = 1.8 * diameter_km * (velocity / 12)**0.78
    
    volume = (4/3) * math.pi * (diameter_km/2)**3
    mass = volume * 2.5e12
    energy_joules = 0.5 * mass * (velocity * 1000)**2
    energy_megatons = energy_joules / 4.184e15
    
    print(f"Diámetro meteorito: {diameter_km} km ({diameter_km*1000} metros)")
    print(f"Velocidad: {velocity} km/s")
    print(f"Cráter calculado: {crater_diameter_km:.4f} km ({crater_diameter_km*1000:.1f} metros)")
    print(f"Energía: {energy_megatons:.2f} megatones")
    
    # Test en NYC
    casualties = demo_service.estimate_casualties(40.7128, -74.0060, crater_diameter_km, energy_megatons)
    print(f"  -> NYC: {casualties.get('total_casualties', 0):,} víctimas")
    
    # Test en área rural
    casualties = demo_service.estimate_casualties(45.0, -100.0, crater_diameter_km, energy_megatons)
    print(f"  -> Rural: {casualties.get('total_casualties', 0):,} víctimas")
    
    # Test 4: Meteorito grande (1 km)
    print("\n4. METEORITO GRANDE (1 km)")
    diameter_km = 1.0
    velocity = 30.0
    crater_diameter_km = 1.8 * diameter_km * (velocity / 12)**0.78
    
    volume = (4/3) * math.pi * (diameter_km/2)**3
    mass = volume * 2.5e12
    energy_joules = 0.5 * mass * (velocity * 1000)**2
    energy_megatons = energy_joules / 4.184e15
    
    print(f"Diámetro meteorito: {diameter_km} km ({diameter_km*1000} metros)")
    print(f"Velocidad: {velocity} km/s")
    print(f"Cráter calculado: {crater_diameter_km:.4f} km ({crater_diameter_km*1000:.1f} metros)")
    print(f"Energía: {energy_megatons:.2f} megatones")
    
    # Test en NYC
    casualties = demo_service.estimate_casualties(40.7128, -74.0060, crater_diameter_km, energy_megatons)
    print(f"  -> NYC: {casualties.get('total_casualties', 0):,} víctimas")
    
    # Test en área rural
    casualties = demo_service.estimate_casualties(45.0, -100.0, crater_diameter_km, energy_megatons)
    print(f"  -> Rural: {casualties.get('total_casualties', 0):,} víctimas")
    
    print("\n" + "=" * 60)
    print("REFERENCIAS REALES:")
    print("- Meteor Crater (Arizona): 50m meteorito → 1.2km cráter")
    print("- Chelyabinsk (2013): 20m meteorito → explosión aérea, ~1,500 heridos")
    print("- Tunguska (1908): ~60m meteorito → 2,000 km² devastados")
    print("=" * 60)

if __name__ == "__main__":
    test_casualties()