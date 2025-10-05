"""
Script de debugging para analizar el flujo completo de datos en simulación
"""

print("🔍 ANÁLISIS COMPLETO DEL FLUJO DE SIMULACIÓN")
print("=" * 60)

print("\n📱 FRONTEND -> BACKEND:")
print("1. Frontend envía impactLocation: { lat: X, lon: Y }")
print("2. Backend recibe simulation_request.impact_location")
print("3. Backend extrae: impact_lat = impact_location.get('lat', 0)")
print("4. Backend llama: demographic_service.estimate_casualties(lat, lon, crater, energy)")

print("\n🔍 PROBLEMA IDENTIFICADO:")
print("El servicio demográfico ESTÁ recibiendo las coordenadas correctas,")
print("pero siempre devuelve resultados similares porque:")

print("\n❌ ISSUE #1: Detección de océano defectuosa")
print("   La función _is_ocean() usa rangos muy amplios que clasifican")
print("   muchas áreas terrestres como océano")

print("\n❌ ISSUE #2: Clasificación de región muy básica") 
print("   Solo tiene 6 ciudades principales en major_cities")
print("   Si no está cerca de esas 6, siempre clasifica como 'rural_sparse'")

print("\n❌ ISSUE #3: Cálculo de víctimas por área circular")
print("   Usa π × radio² × densidad fija")
print("   No considera variaciones reales de población en el área")

print("\n❌ ISSUE #4: Datos económicos fijos por tipo")
print("   Mismo multiplier económico para toda una región")
print("   No considera diferencias dentro de la región")

print("\n🎯 EJEMPLOS PROBLEMÁTICOS:")

# Simular coordenadas específicas
test_locations = [
    {"name": "Tokyo Centro", "lat": 35.6762, "lon": 139.6503, "expected": "urban_major"},
    {"name": "Océano Pacífico", "lat": 0, "lon": -150, "expected": "ocean"},
    {"name": "Nueva York", "lat": 40.7128, "lon": -74.0060, "expected": "urban_major"},
    {"name": "Sahara", "lat": 23.8, "lon": 11.0, "expected": "desert"},
    {"name": "Amazonas", "lat": -3.0, "lon": -60.0, "expected": "forest"},
]

print("\nProbando clasificación de regiones:")
for loc in test_locations:
    lat, lon = loc["lat"], loc["lon"]
    
    # Simular detección de océano
    is_ocean = False
    if -60 < lat < 60 and ((120 < lon < 180) or (-180 < lon < -80)):
        is_ocean = True
    elif -60 < lat < 70 and -80 < lon < 20:
        is_ocean = True
    elif -60 < lat < 30 and 20 < lon < 120:
        is_ocean = True
    
    if is_ocean:
        classified = "ocean"
        density = 0
    else:
        # Simular distancia a ciudad más cercana (simplificado)
        major_cities = {
            "tokyo": {"lat": 35.6762, "lon": 139.6503, "population": 37400000},
            "new_york": {"lat": 40.7128, "lon": -74.0060, "population": 18804000},
        }
        
        min_distance = float('inf')
        nearest_city = None
        for city_name, city_data in major_cities.items():
            # Cálculo simplificado de distancia
            distance = ((lat - city_data["lat"])**2 + (lon - city_data["lon"])**2)**0.5 * 111
            if distance < min_distance:
                min_distance = distance
                nearest_city = {"name": city_name, "distance": distance, "population": city_data["population"]}
        
        if nearest_city and min_distance < 25 and nearest_city["population"] > 20000000:
            classified = "urban_major"
            density = 10000
        elif nearest_city and min_distance < 200:
            classified = "suburban"
            density = 500
        else:
            classified = "rural_sparse"
            density = 25
    
    # Simular cálculo de víctimas para crater de 1km
    crater_diameter = 1.0  # km
    immediate_radius = crater_diameter / 2
    area = 3.14159 * (immediate_radius ** 2)
    population = area * density
    casualties = int(population * 0.95)
    
    print(f"   {loc['name']:15} -> {classified:12} (density: {density:5}/km²) -> {casualties:6} víctimas")
    if classified != loc['expected']:
        print(f"      ⚠️  ESPERADO: {loc['expected']}")

print("\n🚨 CONCLUSIÓN:")
print("El sistema demográfico tiene varios problemas de lógica que causan:")
print("1. Detección incorrecta de océanos vs tierra")
print("2. Clasificación muy básica de regiones") 
print("3. Densidades poblacionales fijas y poco realistas")
print("4. Mismo resultado para ubicaciones muy diferentes")

print("\n💡 SOLUCIONES RECOMENDADAS:")
print("1. Mejorar detección de océanos con datos geográficos reales")
print("2. Expandir base de datos de ciudades principales")
print("3. Usar gradientes de densidad poblacional")
print("4. Implementar interpolación entre diferentes tipos de terreno")
print("5. Agregar más factores geográficos (costa, montaña, etc.)")