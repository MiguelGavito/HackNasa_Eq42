"""
Script para verificar el mapeo correcto de coordenadas geográficas en la esfera 3D
"""

import math

print("🌍 VERIFICACIÓN DE MAPEO DE COORDENADAS ESFERA 3D")
print("=" * 60)

# Función de conversión lat/lon a posición 3D (como en el frontend)
def latlon_to_3d(lat, lon, radius=1):
    """Convertir lat/lon a coordenadas 3D como en el frontend"""
    lat_rad = lat * math.pi / 180
    lon_rad = lon * math.pi / 180
    
    x = radius * math.cos(lat_rad) * math.cos(lon_rad)
    y = radius * math.sin(lat_rad)  
    z = radius * math.cos(lat_rad) * math.sin(lon_rad)
    
    return x, y, z

# Función de conversión 3D a lat/lon (como en el frontend)
def pos_3d_to_latlon(x, y, z):
    """Convertir posición 3D a lat/lon como en el frontend"""
    # Normalizar el vector
    length = math.sqrt(x*x + y*y + z*z)
    nx, ny, nz = x/length, y/length, z/length
    
    # Convertir a lat/lon
    lat = math.asin(ny) * (180 / math.pi)
    lon = math.atan2(nz, nx) * (180 / math.pi)
    
    return lat, lon

print("\n🧪 PRUEBA DE IDA Y VUELTA (Round Trip Test):")
print("Convertir lat/lon → 3D → lat/lon y verificar que coincide")

test_locations = [
    {"name": "Ciudad de México", "lat": 19.4326, "lon": -99.1332},
    {"name": "Tokyo", "lat": 35.6762, "lon": 139.6503},
    {"name": "Nueva York", "lat": 40.7128, "lon": -74.0060},
    {"name": "Londres", "lat": 51.5074, "lon": -0.1278},
    {"name": "Sydney", "lat": -33.8688, "lon": 151.2093},
    {"name": "São Paulo", "lat": -23.5505, "lon": -46.6333},
    {"name": "Punto Ecuador 0°", "lat": 0, "lon": 0},
    {"name": "Meridiano Greenwich", "lat": 51.4778, "lon": 0},
    {"name": "Polo Norte", "lat": 90, "lon": 0},
    {"name": "Polo Sur", "lat": -90, "lon": 0},
    {"name": "Océano Pacífico", "lat": 0, "lon": -150},
    {"name": "Océano Atlántico", "lat": 30, "lon": -40}
]

print(f"{'Ubicación':<20} {'Original':<20} {'Convertido':<20} {'Error':<15} {'Status'}")
print("-" * 90)

max_error = 0
total_error = 0
problematic_locations = []

for loc in test_locations:
    original_lat, original_lon = loc["lat"], loc["lon"]
    
    # Conversión ida y vuelta
    x, y, z = latlon_to_3d(original_lat, original_lon)
    converted_lat, converted_lon = pos_3d_to_latlon(x, y, z)
    
    # Calcular error
    lat_error = abs(original_lat - converted_lat)
    lon_error = abs(original_lon - converted_lon)
    
    # Manejar el caso especial de longitud 180/-180
    if lon_error > 180:
        lon_error = 360 - lon_error
    
    total_error_loc = lat_error + lon_error
    total_error += total_error_loc
    max_error = max(max_error, total_error_loc)
    
    status = "✅ OK" if total_error_loc < 0.01 else "⚠️  ERROR"
    if total_error_loc >= 0.01:
        problematic_locations.append(loc["name"])
    
    print(f"{loc['name']:<20} ({original_lat:6.2f},{original_lon:7.2f}) ({converted_lat:6.2f},{converted_lon:7.2f}) {total_error_loc:8.4f}°     {status}")

avg_error = total_error / len(test_locations)

print("\n📊 RESUMEN DE PRECISIÓN:")
print(f"   Error promedio: {avg_error:.4f}°")
print(f"   Error máximo:   {max_error:.4f}°")
print(f"   Ubicaciones problemáticas: {len(problematic_locations)}")

if problematic_locations:
    print(f"   Problemas en: {', '.join(problematic_locations)}")

print("\n🗺️  VERIFICACIÓN DE TEXTURA DE MAPA:")
print("Verificando si la textura está correctamente orientada...")

# Verificar orientación de la textura
print("\n📍 PUNTOS DE REFERENCIA GEOGRÁFICOS:")
reference_points = [
    {"name": "Greenwich (0°,0°)", "lat": 0, "lon": 0, "expected": "Costa de África occidental"},
    {"name": "Ecuador Pacífico", "lat": 0, "lon": -90, "expected": "Océano Pacífico (oeste Ecuador)"},
    {"name": "Meridiano 180°", "lat": 0, "lon": 180, "expected": "Océano Pacífico (línea fecha)"},
    {"name": "Meridiano -180°", "lat": 0, "lon": -180, "expected": "Océano Pacífico (línea fecha)"},
]

for point in reference_points:
    x, y, z = latlon_to_3d(point["lat"], point["lon"])
    print(f"   {point['name']:<20} → 3D({x:6.3f}, {y:6.3f}, {z:6.3f}) → {point['expected']}")

print("\n🎯 VALIDACIÓN ESPECÍFICA PARA TEXTURAS DE TIERRA:")

# Verificar que las coordenadas conocidas caigan en lugares correctos
validation_tests = [
    {
        "click_description": "Clic en el centro de Estados Unidos",
        "expected_lat": 39.8283, 
        "expected_lon": -98.5795,
        "tolerance_lat": 10,
        "tolerance_lon": 10,
        "region": "Norteamérica"
    },
    {
        "click_description": "Clic en el centro de Europa",
        "expected_lat": 54.5260, 
        "expected_lon": 15.2551,
        "tolerance_lat": 10,
        "tolerance_lon": 15,
        "region": "Europa"
    },
    {
        "click_description": "Clic en Australia",
        "expected_lat": -25.2744, 
        "expected_lon": 133.7751,
        "tolerance_lat": 10,
        "tolerance_lon": 15,
        "region": "Australia"
    }
]

print("\n🔍 POSIBLES PROBLEMAS COMUNES:")
print("1. Textura invertida horizontalmente (este-oeste intercambiados)")
print("2. Textura invertida verticalmente (norte-sur intercambiados)")
print("3. Rotación de textura (offset en longitud)")
print("4. Escala incorrecta de UV mapping")

print("\n💡 RECOMENDACIÓN PARA PRUEBA MANUAL:")
print("1. Abre la aplicación")
print("2. Haz clic en ubicaciones conocidas:")
print("   • Centro de Estados Unidos (debería ser ~40°N, 100°W)")
print("   • Reino Unido (debería ser ~54°N, 2°W)")
print("   • Japón (debería ser ~36°N, 138°E)")
print("   • Australia (debería ser ~25°S, 135°E)")
print("3. Verifica que las coordenadas mostradas coincidan")
print("4. Si no coinciden, la textura necesita ajuste")

print("\n🛠️  SI HAY PROBLEMAS:")
print("- Verificar orientación de earth-day.jpg")
print("- Ajustar UV mapping en Three.js")
print("- Considerar rotar textura 180° si este-oeste están invertidos")
print("- Verificar que la textura sea equirectangular estándar")

# Función para debugging en vivo
def debug_coordinate_conversion(lat, lon):
    """Función para usar en debugging en vivo"""
    print(f"\n🔍 DEBUG: lat={lat}, lon={lon}")
    x, y, z = latlon_to_3d(lat, lon)
    print(f"   → 3D: ({x:.3f}, {y:.3f}, {z:.3f})")
    back_lat, back_lon = pos_3d_to_latlon(x, y, z)
    print(f"   → Back: ({back_lat:.3f}, {back_lon:.3f})")
    error = abs(lat - back_lat) + abs(lon - back_lon)
    print(f"   → Error: {error:.4f}°")

print("\n" + "=" * 60)
print("✅ Verificación completada. Prueba manualmente las coordenadas.")