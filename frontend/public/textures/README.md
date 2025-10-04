# Texturas para el Modelo 3D de la Tierra

Esta carpeta debe contener las texturas necesarias para el modelo 3D de la Tierra en el Asteroid Launcher.

## Archivos Requeridos

### 1. earth-day.jpg
- **Descripción**: Textura principal de la Tierra (día)
- **Resolución recomendada**: 2048x1024 o 4096x2048
- **Fuente**: NASA Blue Marble o similar
- **URL de ejemplo**: https://www.nasa.gov/sites/default/files/thumbnails/image/blue_marble_2012_-_blue_marble_next_generation.jpg

### 2. earth-normal.jpg
- **Descripción**: Mapa de normales para dar relieve a la superficie
- **Resolución**: Igual que earth-day.jpg
- **Uso**: Crear efectos de profundidad en montañas y océanos

### 3. earth-specular.jpg
- **Descripción**: Mapa especular para reflejos (océanos brillantes, tierra opaca)
- **Resolución**: Igual que earth-day.jpg
- **Uso**: Los océanos aparecen en blanco, la tierra en negro

## Cómo Obtener las Texturas

### Opción 1: Texturas Gratuitas de NASA
```
1. Visitar: https://www.nasa.gov/multimedia/imagegallery/
2. Buscar "Blue Marble" o "Earth texture"
3. Descargar imagen de alta resolución
4. Renombrar como earth-day.jpg
```

### Opción 2: Texturas de Desarrollo (Básicas)
Para desarrollo rápido, puedes usar colores sólidos temporalmente:
- earth-day.jpg: Imagen de la Tierra básica
- earth-normal.jpg: Gris neutro (RGB: 128,128,255)
- earth-specular.jpg: Negro para tierra, blanco para océanos

### Opción 3: Texturas de Stock (Recomendado)
- **Sitios**: textures.com, freepik.com, unsplash.com
- **Términos de búsqueda**: "earth texture", "planet texture", "world map"
- **Licencia**: Verificar que sean libres para uso

## Instalación

1. Descargar las texturas
2. Renombrarlas según los nombres requeridos
3. Colocarlas en esta carpeta (`public/textures/`)
4. El componente AsteroidViewer3D las cargará automáticamente

## Texturas Alternativas (Fallback)

Si no tienes las texturas, el componente mostrará la Tierra como una esfera azul básica.

## Optimización

- **Formato**: JPG para texturas (menor tamaño)
- **Resolución**: Balance entre calidad y performance
  - Desarrollo: 1024x512
  - Producción: 2048x1024 o superior
- **Compresión**: Usar herramientas como tinypng.com para reducir tamaño

## Créditos

Recuerda dar crédito apropiado según la fuente de las texturas:
- NASA: Dominio público, no requiere crédito pero es recomendado
- Stock photos: Verificar licencia específica