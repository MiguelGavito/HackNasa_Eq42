# 🚀 Asteroid Launcher - Guía de Inicio Rápido

## Instalación Rápida

### 1. Instalar Dependencias

```bash
# Backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Frontend (nueva terminal)
cd frontend
npm install
```

### 2. Ejecutar la Aplicación

```bash
# Terminal 1: Backend
cd backend
venv\Scripts\activate
python app.py

# Terminal 2: Frontend
cd frontend
npm start
```

### 3. Acceder al Asteroid Launcher

1. Abrir http://localhost:3000
2. Navegar a "🚀 Launcher" en el menú
3. ¡Comenzar a destruir planetas!

## Cómo Usar el Asteroid Launcher

### Paso 1: Configurar el Asteroide
- **Diámetro**: Desde 0.01 km (piedra) hasta 15 km (extinción masiva)
- **Velocidad**: 11-72 km/s (velocidad cósmica realista)
- **Ángulo**: 15°-90° (afecta el patrón de destrucción)
- **Composición**: Rocoso, Metálico o Helado

### Paso 2: Seleccionar Objetivo
- Rotar la Tierra 3D con el mouse
- Hacer zoom con la rueda del mouse
- Hacer clic en cualquier punto de la superficie

### Paso 3: Lanzar y Observar
- Presionar "🚀 Lanzar Asteroide"
- Ver la animación del impacto
- Analizar los resultados destructivos

## Ejemplos Preconfigurados

### 🏠 **Tunguska (1908)**
- Diámetro: 60m
- Destrucción: Bosque de 2,000 km²
- Resultado: Daño regional

### 🌆 **Chelyabinsk (2013)**
- Diámetro: 20m
- Destrucción: Ventanas rotas en ciudad
- Resultado: Daño local

### 🦕 **Chicxulub (Dinosaurios)**
- Diámetro: 10 km
- Destrucción: Extinción masiva
- Resultado: Fin de una era

### ☄️ **Apophis (Hipotético)**
- Diámetro: 340m
- Destrucción: Devastación regional
- Resultado: Crisis global

## Interpretando los Resultados

### 🔥 **Energía Liberada**
- Medida en Megatones TNT
- 1 MT = 67 veces la bomba de Hiroshima
- >100,000 MT = Extinción masiva

### 🕳️ **Diámetro del Cráter**
- Depende del tamaño y velocidad
- Cráteres grandes son visibles desde el espacio
- Referencia: Cráter de Arizona = 1.2 km

### 📍 **Área Afectada**
- Incluye destrucción directa e indirecta
- Ondas sísmicas, incendios, tsunami
- Comparado con países/estados

### 👥 **Víctimas Estimadas**
- Basado en densidad poblacional
- Océanos: Principalmente tsunamis
- Ciudades: Máxima devastación

## Efectos Especiales por Tamaño

### 🪨 **Pequeño (< 100m)**
- Explosión atmosférica
- Daño local por onda expansiva
- Comparable a arma nuclear

### 🗿 **Mediano (100m - 1km)**
- Cráter de impacto
- Destrucción regional
- Efectos sísmicos significativos

### 🏔️ **Grande (1-10km)**
- Devastación continental
- Cambio climático temporal
- Extinción de especies locales

### 🌍 **Masivo (>10km)**
- Extinción masiva global
- Invierno nuclear
- Colapso de ecosistemas

## Tips y Trucos

### 🎯 **Maximizar Destrucción**
- Asteroide grande + alta velocidad
- Ángulo de 45° para máximo alcance
- Impacto en área densamente poblada

### 🌊 **Generar Tsunamis**
- Impactar en océanos profundos
- Asteroides >1km de diámetro
- Costas pobladas para máximo efecto

### 🔬 **Experimentos Científicos**
- Comparar composiciones diferentes
- Probar ángulos de impacto
- Analizar efectos de velocidad

### 🏙️ **Objetivos Interesantes**
- Nueva York: Máxima densidad urbana
- Océano Pacífico: Tsunamis masivos
- Himalaya: Efectos geológicos únicos
- Sahara: Mínima población, máximo cráter

## Datos Científicos Reales

### 📊 **Frecuencia de Impactos**
- >1km: Cada 500,000 años
- >10km: Cada 50-100 millones de años
- Pequeños: Diariamente (se queman en atmósfera)

### 🛡️ **Sistemas de Defensa Actuales**
- Detección: Telescopios espaciales y terrestres
- Alerta temprana: 10-50 años para grandes asteroides
- Deflección: Misiones kinéticas (en desarrollo)

### 🎯 **Probabilidades Reales**
- Apophis 2029: 0% de impacto
- Asteroides desconocidos: Mayor amenaza
- Impactos pequeños: Muy frecuentes

## Personalización Avanzada

### 🔧 **Modificar Parámetros**
- Editar `AsteroidControls.js` para nuevos rangos
- Ajustar cálculos en `impact_simulator.py`
- Personalizar efectos visuales en `AsteroidViewer3D.js`

### 🎨 **Texturas Personalizadas**
- Agregar texturas en `public/textures/`
- Soporta mapas de altura y normales
- Ver `textures/README.md` para detalles

¡Diviértete destruyendo mundos de manera científicamente precisa! 🌍💥