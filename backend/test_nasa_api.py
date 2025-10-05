#!/usr/bin/env python3
"""
Script de prueba para verificar que el .env y NASA API funcionan correctamente
"""

import os
from dotenv import load_dotenv
from services.nasa_api import NASAApiService

def test_nasa_api():
    print("🚀 Probando NASA API...")
    
    # Cargar variables de entorno
    load_dotenv()
    api_key = os.getenv('NASA_API_KEY')
    
    if not api_key:
        print("❌ ERROR: NASA_API_KEY no encontrada en .env")
        return False
    
    print(f"✅ API Key encontrada: {api_key[:10]}...")
    
    # Inicializar servicio
    try:
        nasa_service = NASAApiService()
        print("✅ Servicio NASA inicializado correctamente")
    except Exception as e:
        print(f"❌ Error inicializando servicio: {e}")
        return False
    
    # Probar obtener datos NEO
    try:
        print("🌍 Obteniendo datos de asteroides cercanos...")
        neo_data = nasa_service.get_neo_feed()
        
        if neo_data:
            print(f"✅ Datos obtenidos: {len(neo_data)} asteroides encontrados")
            
            # Mostrar algunos datos del primer asteroide
            if len(neo_data) > 0:
                first_asteroid = neo_data[0]
                print(f"   📡 Primer asteroide:")
                print(f"      • ID: {first_asteroid['id']}")
                print(f"      • Nombre: {first_asteroid['name']}")
                print(f"      • Diámetro máx: {first_asteroid['estimated_diameter_km_max']:.3f} km")
                print(f"      • Velocidad: {first_asteroid['relative_velocity_km_s']:.2f} km/s")
                print(f"      • Distancia: {first_asteroid['miss_distance_km']:,.0f} km")
                print(f"      • Peligroso: {'Sí' if first_asteroid['is_potentially_hazardous_asteroid'] else 'No'}")
            
            return True
        else:
            print("❌ No se obtuvieron datos")
            return False
            
    except Exception as e:
        print(f"❌ Error obteniendo datos NEO: {e}")
        return False

if __name__ == "__main__":
    success = test_nasa_api()
    
    if success:
        print("\n🎉 ¡Prueba exitosa! Tu .env está configurado correctamente")
        print("📝 Ahora puedes reiniciar tu backend con: python app.py")
    else:
        print("\n⚠️  Hay problemas con la configuración")
        print("💡 Verifica:")
        print("   1. Que tu archivo .env existe en la carpeta backend/")
        print("   2. Que contiene: NASA_API_KEY=tu_clave_aqui")
        print("   3. Que tu clave API de NASA es válida")