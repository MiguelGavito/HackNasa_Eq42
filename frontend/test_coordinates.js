// Test de coordenadas - Verificar que México aparezca en el lugar correcto
// México está aproximadamente en: 25°N, 100°W

console.log("=== TEST DE COORDENADAS MÉXICO ===");

// Coordenadas reales de México
const mexico_lat = 25.0;
const mexico_lon = -100.0;

console.log(`México real: ${mexico_lat}°N, ${mexico_lon}°W`);

// Conversión lat/lon a 3D (como en getImpactPosition)
const lat_rad = (mexico_lat * Math.PI) / 180;
const lon_rad = (mexico_lon * Math.PI) / 180;
const radius = 1.0;

const x = radius * Math.cos(lat_rad) * Math.cos(lon_rad);
const y = radius * Math.sin(lat_rad);
const z = radius * Math.cos(lat_rad) * Math.sin(lon_rad);

console.log(`3D calculado: x=${x.toFixed(4)}, y=${y.toFixed(4)}, z=${z.toFixed(4)}`);

// Conversión inversa 3D a lat/lon (como en el click handler)
const lat_back = Math.asin(y) * (180 / Math.PI);
const lon_back = Math.atan2(z, x) * (180 / Math.PI);

console.log(`Conversión inversa: ${lat_back.toFixed(2)}°N, ${lon_back.toFixed(2)}°W`);

// Verificar que coincidan
const lat_error = Math.abs(mexico_lat - lat_back);
const lon_error = Math.abs(mexico_lon - lon_back);

console.log(`Error latitud: ${lat_error.toFixed(4)}°`);
console.log(`Error longitud: ${lon_error.toFixed(4)}°`);

if (lat_error < 0.01 && lon_error < 0.01) {
    console.log("✅ CONVERSIÓN CORRECTA - Las fórmulas son consistentes");
} else {
    console.log("❌ ERROR EN CONVERSIÓN - Las fórmulas no coinciden");
}

// Test de dirección este/oeste
console.log("\n=== TEST DIRECCIÓN ESTE/OESTE ===");

// Punto al este de México
const mexico_este_lon = -95.0; // 5° al este
const lon_este_rad = (mexico_este_lon * Math.PI) / 180;
const x_este = radius * Math.cos(lat_rad) * Math.cos(lon_este_rad);
const z_este = radius * Math.cos(lat_rad) * Math.sin(lon_este_rad);
const lon_este_back = Math.atan2(z_este, x_este) * (180 / Math.PI);

console.log(`5° al ESTE de México: ${mexico_este_lon}° → ${lon_este_back.toFixed(2)}°`);

// Punto al oeste de México
const mexico_oeste_lon = -105.0; // 5° al oeste
const lon_oeste_rad = (mexico_oeste_lon * Math.PI) / 180;
const x_oeste = radius * Math.cos(lat_rad) * Math.cos(lon_oeste_rad);
const z_oeste = radius * Math.cos(lat_rad) * Math.sin(lon_oeste_rad);
const lon_oeste_back = Math.atan2(z_oeste, x_oeste) * (180 / Math.PI);

console.log(`5° al OESTE de México: ${mexico_oeste_lon}° → ${lon_oeste_back.toFixed(2)}°`);

if (lon_este_back > lon_oeste_back) {
    console.log("✅ DIRECCIÓN CORRECTA - Este > Oeste");
} else {
    console.log("❌ DIRECCIÓN INCORRECTA - Este < Oeste");
}