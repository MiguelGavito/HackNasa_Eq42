#!/usr/bin/env python3
"""
Script de debugging detallado para NASA API
"""

import os
import requests
from dotenv import load_dotenv

def debug_step_by_step():
    print("🔍 DIAGNÓSTICO PASO A PASO - NASA API")
    print("=" * 50)
    
    # PASO 1: Verificar .env
    print("\n📋 PASO 1: Verificando archivo .env")
    load_dotenv()
    
    if os.path.exists('.env'):
        print("✅ Archivo .env encontrado")
        with open('.env', 'r') as f:
            content = f.read()
            if 'NASA_API_KEY' in content:
                print("✅ NASA_API_KEY encontrada en .env")
            else:
                print("❌ NASA_API_KEY NO encontrada en .env")
                return False
    else:
        print("❌ Archivo .env NO encontrado")
        return False
    
    # PASO 2: Verificar variable de entorno
    print("\n🔑 PASO 2: Verificando variable de entorno")
    api_key = os.getenv('NASA_API_KEY')
    
    if api_key:
        print(f"✅ NASA_API_KEY cargada: {api_key[:10]}...{api_key[-5:]}")
        if api_key == 'DEMO_KEY':
            print("⚠️  Usando DEMO_KEY (limitado a 30 requests/hora)")
        else:
            print("✅ Usando API key personalizada")
    else:
        print("❌ NASA_API_KEY no se pudo cargar")
        return False
    
    # PASO 3: Probar conexión directa a NASA API
    print("\n🌐 PASO 3: Probando conexión directa a NASA API")
    
    # URL para probar Neo Feed
    url = f"https://api.nasa.gov/neo/rest/v1/feed?api_key={api_key}"
    
    try:
        print(f"📡 Haciendo request a: {url[:80]}...")
        response = requests.get(url, timeout=10)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📏 Content Length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            print("✅ Conexión exitosa!")
            
            try:
                data = response.json()
                print(f"📋 Estructura de respuesta:")
                print(f"   • Keys: {list(data.keys())}")
                
                if 'near_earth_objects' in data:
                    neo_objects = data['near_earth_objects']
                    total_asteroids = sum(len(asteroids) for asteroids in neo_objects.values())
                    print(f"   • Total asteroides: {total_asteroids}")
                    print("✅ Datos válidos recibidos")
                    return True
                else:
                    print("❌ Estructura de datos inesperada")
                    print(f"Datos recibidos: {str(data)[:200]}...")
                    return False
                    
            except Exception as json_error:
                print(f"❌ Error parseando JSON: {json_error}")
                print(f"Contenido: {response.text[:200]}...")
                return False
                
        elif response.status_code == 403:
            print("❌ Error 403: API key inválida o expirada")
            print("💡 Verifica tu API key en https://api.nasa.gov/")
            return False
            
        elif response.status_code == 429:
            print("❌ Error 429: Límite de requests excedido")
            print("💡 Espera un momento o usa tu propia API key")
            return False
            
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            print(f"Mensaje: {response.text[:200]}...")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout: La API tardó demasiado en responder")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión: No se puede conectar a NASA API")
        print("💡 Verifica tu conexión a internet")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {type(e).__name__}: {e}")
        return False

def test_our_service():
    print("\n🔧 PASO 4: Probando nuestro servicio NASA")
    
    try:
        from services.nasa_api import NASAApiService
        nasa_service = NASAApiService()
        
        print("✅ Servicio importado correctamente")
        print(f"🔑 API Key en servicio: {nasa_service.api_key[:10]}...{nasa_service.api_key[-5:]}")
        
        # Probar método get_neo_feed
        print("📡 Llamando get_neo_feed()...")
        result = nasa_service.get_neo_feed()
        
        print(f"📊 Tipo de resultado: {type(result)}")
        print(f"📏 Contenido: {str(result)[:200]}...")
        
        if isinstance(result, list):
            print(f"✅ Lista con {len(result)} elementos")
            if len(result) > 0:
                print(f"📋 Primer elemento: {result[0]}")
            return True
        else:
            print(f"❌ Resultado no es una lista: {result}")
            return False
            
    except ImportError as e:
        print(f"❌ Error importando servicio: {e}")
        return False
    except Exception as e:
        print(f"❌ Error en servicio: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO DIAGNÓSTICO COMPLETO")
    
    step1 = debug_step_by_step()
    if step1:
        step2 = test_our_service()
        
        if step1 and step2:
            print("\n🎉 ¡TODO FUNCIONA CORRECTAMENTE!")
            print("📝 Puedes reiniciar tu backend con: python app.py")
        else:
            print("\n⚠️  Hay problemas en nuestro servicio")
    else:
        print("\n⚠️  Hay problemas básicos de configuración")
    
    print("\n" + "=" * 50)
    print("📋 RESUMEN DE DIAGNÓSTICO COMPLETADO")