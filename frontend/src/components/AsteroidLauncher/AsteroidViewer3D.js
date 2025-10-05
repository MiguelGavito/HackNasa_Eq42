import React, { useRef, useState, useEffect } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { 
  Sphere, 
  OrbitControls, 
  Stars, 
  Text,
  useTexture,
  Ring,
  Cylinder
} from '@react-three/drei';
import * as THREE from 'three';

// Componente de la Tierra
const Earth = ({ impactLocation, showImpact, impactIntensity, onEarthClick }) => {
  const earthRef = useRef();
  const impactRef = useRef();
  
  // Usar solo la textura de día de la Tierra
  const earthTexture = useTexture('/textures/earth-day.jpg');

  useFrame((state) => {
    /*
    if (earthRef.current) {
      earthRef.current.rotation.y += 0.002;
    }
      */

    // Animación del impacto
    if (showImpact && impactRef.current) {
      const time = state.clock.getElapsedTime();
      const intensity = Math.sin(time * 10) * impactIntensity;
      impactRef.current.scale.setScalar(1 + intensity * 0.1);
    }
  });

  // Convertir coordenadas lat/lon a posición 3D en la esfera
  const getImpactPosition = () => {
    if (!impactLocation) return [0, 0, 1];
    
    const lat = (impactLocation.lat * Math.PI) / 180;
    const lon = (impactLocation.lon * Math.PI) / 180;
    const radius = 1.01; // Ligeramente fuera de la superficie
    
    const x = radius * Math.cos(lat) * Math.cos(lon);
    const y = radius * Math.sin(lat);
    const z = radius * Math.cos(lat) * Math.sin(lon);
    
    return [x, y, z];
  };



  const calculateRingRotation = () => {
    if (!impactLocation) return [-Math.PI / 2, 0, 0];
  
    const lat = (impactLocation.lat * Math.PI) / 180;
    const lon = (impactLocation.lon * Math.PI) / 180;
    
    // Crear vector normal hacia el centro de la Tierra
    const normal = new THREE.Vector3(
      Math.cos(lat) * Math.cos(lon),
      Math.sin(lat),
      Math.cos(lat) * Math.sin(lon)
    );
    
    // Calcular rotación para que el anillo sea perpendicular al vector normal
    const euler = new THREE.Euler();
    const quaternion = new THREE.Quaternion();
    
    // Orientar el anillo para que mire hacia el centro
    quaternion.setFromUnitVectors(new THREE.Vector3(0, 0, 1), normal);
    euler.setFromQuaternion(quaternion);
    
    return [euler.x, euler.y, euler.z];
  }

  const impactPos = getImpactPosition();

  return (
    <group>
      {/* Tierra */}
      <Sphere 
        ref={earthRef} 
        args={[1, 64, 64]} 
        position={[0, 0, 0]}
        rotation={[0,Math.PI / 1, 0]}
        onClick={onEarthClick}
      >
        <meshPhongMaterial 
          map={earthTexture}
          shininess={100}
        />
      </Sphere>
      
      {/* Atmósfera */}
      <Sphere args={[1.02, 32, 32]} position={[0, 0, 0]}>
        <meshPhongMaterial 
          color="#87CEEB" 
          transparent 
          opacity={0.1}
          side={THREE.BackSide}
        />
      </Sphere>

      {/* Marcador de impacto */}
      {impactLocation && (
        <group position={impactPos}>
          <Ring 
            ref={impactRef}
            args={[0.02, 0.04, 16]}
            rotation={calculateRingRotation()}
          >
            <meshBasicMaterial 
              color={showImpact ? "#ff4444" : "#ffaa00"} 
              transparent
              opacity={showImpact ? 0.8 : 0.6}
            />
          </Ring>
          
          {/* Punto de impacto */}
          <Sphere args={[0.01, 8, 8]}>
            <meshBasicMaterial color="#ff0000" />
          </Sphere>
        </group>
      )}

      {/* Efecto de explosión */}
      {showImpact && impactLocation && (
        <group position={impactPos}>
          {[...Array(8)].map((_, i) => (
            <Sphere key={i} args={[0.005, 8, 8]} position={[
              (Math.random() - 0.5) * 0.1,
              (Math.random() - 0.5) * 0.1,
              (Math.random() - 0.5) * 0.1
            ]}>
              <meshBasicMaterial 
                color={`hsl(${Math.random() * 60}, 100%, 50%)`}
                transparent
                opacity={0.7}
              />
            </Sphere>
          ))}
        </group>
      )}
    </group>
  );
};

// Componente del Asteroide
const Asteroid = ({ 
  size, 
  velocity, 
  angle, 
  position, 
  isLaunched, 
  targetPosition,
  onImpact 
}) => {
  const asteroidRef = useRef();
  const [currentPosition, setCurrentPosition] = useState(position);
  const [hasImpacted, setHasImpacted] = useState(false);

  useFrame((state, delta) => {
    if (!isLaunched || hasImpacted || !asteroidRef.current) return;

    const currentPos = new THREE.Vector3(...currentPosition);
    const targetPos = new THREE.Vector3(...targetPosition);
    
    // Calcular trayectoria que evite atravesar la Tierra
    const earthCenter = new THREE.Vector3(0, 0, 0);
    const currentDistance = currentPos.length();
    
    // Si está muy cerca de la Tierra, usar trayectoria tangencial
    let direction;
    if (currentDistance < 2.5) {
      // Trayectoria directa cuando está cerca
      direction = new THREE.Vector3().subVectors(targetPos, currentPos).normalize();
    } else {
      // Trayectoria curva que evite pasar por el centro de la Tierra
      const toTarget = new THREE.Vector3().subVectors(targetPos, currentPos);
      const toEarth = new THREE.Vector3().subVectors(earthCenter, currentPos);
      
      // Si la trayectoria directa pasaría muy cerca del centro, ajustarla
      const directPath = toTarget.clone().normalize();
      const earthDirection = toEarth.clone().normalize();
      const dotProduct = directPath.dot(earthDirection);
      
      if (dotProduct > 0.3) { // Si va hacia el centro de la Tierra
        // Crear trayectoria tangencial
        const perpendicular = new THREE.Vector3().crossVectors(directPath, new THREE.Vector3(0, 1, 0));
        if (perpendicular.length() < 0.1) {
          perpendicular.crossVectors(directPath, new THREE.Vector3(1, 0, 0));
        }
        perpendicular.normalize();
        
        // Mezclar dirección directa con perpendicular para evitar la Tierra
        direction = directPath.multiplyScalar(0.7).add(perpendicular.multiplyScalar(0.3)).normalize();
      } else {
        direction = directPath;
      }
    }

    // Mover asteroide con velocidad variable según distancia
    const distanceToTarget = currentPos.distanceTo(targetPos);
    const speedMultiplier = Math.max(0.3, Math.min(1.0, distanceToTarget / 3));
    const speed = velocity * delta * 0.15 * speedMultiplier;
    
    const newPos = currentPos.add(direction.multiplyScalar(speed));
    
    setCurrentPosition([newPos.x, newPos.y, newPos.z]);
    asteroidRef.current.position.copy(newPos);
    
    // Rotación del asteroide
    asteroidRef.current.rotation.x += delta * 2;
    asteroidRef.current.rotation.y += delta * 1.5;

    // Verificar impacto (distancia a la superficie de la Tierra)
    const distanceToEarthSurface = newPos.length() - 1.0; // Restar radio de la Tierra
    if (distanceToEarthSurface <= 0.05) { // Impacto a 50m de la superficie
      setHasImpacted(true);
      onImpact();
    }
  });

  if (!isLaunched) return null;

  return (
    <group>
      <Sphere 
        ref={asteroidRef} 
        args={[size * 0.01, 16, 16]} 
        position={currentPosition}
      >
        <meshStandardMaterial 
          color="#8B4513" 
          roughness={0.8}
          metalness={0.2}
        />
      </Sphere>
      
      {/* Estela del asteroide */}
      {!hasImpacted && (
        <Cylinder 
          args={[0.002, 0.005, velocity * 0.02, 8]}
          position={[
            currentPosition[0] - 0.1,
            currentPosition[1] - 0.1, 
            currentPosition[2] - 0.1
          ]}
        >
          <meshBasicMaterial 
            color="#ff6600" 
            transparent 
            opacity={0.6}
          />
        </Cylinder>
      )}
    </group>
  );
};

// Componente de información de impacto
const ImpactInfo = ({ results, position }) => {
  if (!results) return null;

  return (
    <group position={position}>
      <Text
        fontSize={0.05}
        color="#ff4444"
        anchorX="center"
        anchorY="middle"
        position={[0, 0.2, 0]}
      >
        ¡IMPACTO!
      </Text>
      <Text
        fontSize={0.03}
        color="#ffffff"
        anchorX="center"
        anchorY="middle"
        position={[0, 0.1, 0]}
      >
        {`Cráter: ${results.crater_diameter?.toFixed(2)} km`}
      </Text>
      <Text
        fontSize={0.03}
        color="#ffffff"
        anchorX="center"
        anchorY="middle"
        position={[0, 0.05, 0]}
      >
        {`Energía: ${results.energy_released?.toFixed(1)} MT`}
      </Text>
    </group>
  );
};

// Componente principal del viewer 3D
const AsteroidViewer3D = ({ 
  asteroidData, 
  impactLocation, 
  simulationResults,
  onLocationSelect,
  isSimulating,
  showImpactEffect
}) => {
  const [cameraPosition, setCameraPosition] = useState([3, 1, 3]);
  const [asteroidLaunched, setAsteroidLaunched] = useState(false);

  const asteroidStartPosition = [4, 2, 4];
  
  const getTargetPosition = () => {
    if (!impactLocation) return [1, 0, 0];
    
    const lat = (impactLocation.lat * Math.PI) / 180;
    const lon = (impactLocation.lon * Math.PI) / 180;
    
    const x = Math.cos(lat) * Math.cos(lon);
    const y = Math.sin(lat);
    const z = Math.cos(lat) * Math.sin(lon);
    
    return [x, y, z];
  };

  const handleImpact = () => {
    console.log('¡Impacto detectado!');
  };

  const [lastClickTime, setLastClickTime] = useState(0);
  const [clickCount, setClickCount] = useState(0);

  const handleCanvasClick = (event) => {
    if (!onLocationSelect) return;
    
    const currentTime = Date.now();
    const timeDiff = currentTime - lastClickTime;
    
    if (timeDiff < 500 && clickCount === 1) {
      // DOBLE CLICK DETECTADO
      // Usar intersections del evento React Three Fiber
      if (event.intersections && event.intersections.length > 0) {
        const intersection = event.intersections[0];
        const worldPosition = intersection.point;
        
        // Normalizar a la superficie de la esfera (radio = 1)
        const normalizedPosition = worldPosition.clone().normalize();
        
        // Convertir posición 3D a lat/lon
        const lat = Math.asin(normalizedPosition.y) * (180 / Math.PI);
        const lon = Math.atan2(normalizedPosition.z, normalizedPosition.x) * (180 / Math.PI);
        
        onLocationSelect({ lat, lon });
      }
      setClickCount(0);
    } else {
      setClickCount(1);
      setLastClickTime(currentTime);
      setTimeout(() => setClickCount(0), 500);
    }
  };
  /*
  const handleCanvasClick = (event) => {
    if (!onLocationSelect) return;
  
    const currentTime = Date.now();
    const timeDiff = currentTime - lastClickTime;
  
    if (timeDiff < 500 && clickCount === 1) {
      // DOBLE CLICK DETECTADO
      const mouse = new THREE.Vector2();
      mouse.x = (event.point.x / window.innerWidth) * 2 - 1;
      mouse.y = -(event.point.y / window.innerHeight) * 2 + 1;
      
      // Crear raycaster manualmente
      const raycaster = new THREE.Raycaster();
      raycaster.setFromCamera(mouse, event.camera);
      
      // Intersección con la esfera de la Tierra
      const sphere = new THREE.Sphere(new THREE.Vector3(0, 0, 0), 1);
      const intersectionPoint = new THREE.Vector3();
      
      if (raycaster.ray.intersectSphere(sphere, intersectionPoint)) {
        const lat = Math.asin(intersectionPoint.y) * (180 / Math.PI);
        const lon = Math.atan2(intersectionPoint.z, intersectionPoint.x) * (180 / Math.PI);
        onLocationSelect({ lat, lon });
      }
      
    setClickCount(0);
    } else {
      setClickCount(1);
      setLastClickTime(currentTime);
      setTimeout(() => setClickCount(0), 500);
    }
  };
  */

  /*
  // Click handler para la Tierra
  const EarthClickHandler = () => {
    const { camera, raycaster } = useThree();

    
    
    const handleClick = (event) => {
      if (!onLocationSelect) return;

      const currentTime = Date.now();
      const timeDiff = currentTime - lastClickTime;

      // Solo ejecutar seleccion si es doble click (< 500ms)
      if (timeDiff < 500 && clickCount === 1){
          
        // Convertir coordenadas del click a posición 3D
        const rect = event.target.getBoundingClientRect();
        const mouse = new THREE.Vector2();
        mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
        
        raycaster.setFromCamera(mouse, camera);
        
        // Intersección con la esfera de la Tierra
        const sphere = new THREE.Sphere(new THREE.Vector3(0, 0, 0), 1);
        const intersectionPoint = new THREE.Vector3();
        
        if (raycaster.ray.intersectSphere(sphere, intersectionPoint)) {
          // Convertir posición 3D a lat/lon
          const lat = Math.asin(intersectionPoint.y) * (180 / Math.PI);
          const lon = Math.atan2(intersectionPoint.z, intersectionPoint.x) * (180 / Math.PI);
          
          onLocationSelect({ lat, lon });
        } 
        setClickCount(0); // Reset
      } else {
        // Primer click
        setClickCount(1);
        setLastClickTime(currentTime);
        setTimeout(() => setClickCount(0), 500); // Auto-reset
      }
      
    };

    useEffect(() => {
      const canvas = document.querySelector('canvas');
      if (canvas) {
        canvas.addEventListener('click', handleClick);
        return () => canvas.removeEventListener('click', handleClick);
      }
    }, [lastClickTime, clickCount]);

    return null;
  };
  */

  useEffect(() => {
    if (isSimulating && !asteroidLaunched) {
      setAsteroidLaunched(true);
      setTimeout(() => setAsteroidLaunched(false), 5000); // Reset después de 5 segundos
    }
  }, [isSimulating]);

  return (
    <div style={{ width: '100%', height: '500px', background: '#000011' }}>
      <Canvas 
        camera={{ position: cameraPosition, fov: 60 }}
        onPointerDown={handleCanvasClick}
      >
        {/* Iluminación */}
        <ambientLight intensity={0.3} />
        <directionalLight 
          position={[5, 5, 5]} 
          intensity={1} 
          castShadow 
        />
        <pointLight 
          position={[-5, -5, -5]} 
          intensity={0.5} 
          color="#4488ff" 
        />

        {/* Estrellas de fondo */}
        <Stars 
          radius={100} 
          depth={50} 
          count={5000} 
          factor={4} 
          saturation={0} 
        />

        {/* Controles de órbita */}
        <OrbitControls 
          enablePan={true}
          enableZoom={true}
          enableRotate={true}
          minDistance={1.5}
          maxDistance={10}
        />

        {/* La Tierra */}
        <Earth 
          impactLocation={impactLocation}
          showImpact={showImpactEffect}
          impactIntensity={simulationResults ? 1 : 0}
          onEarthClick={handleCanvasClick}
        />

        {/* Asteroide */}
        {asteroidData && (
          <Asteroid
            size={asteroidData.diameter || 1}
            velocity={asteroidData.velocity || 20}
            angle={45}
            position={asteroidStartPosition}
            isLaunched={asteroidLaunched}
            targetPosition={getTargetPosition()}
            onImpact={handleImpact}
          />
        )}

        {/* Información de impacto */}
        {simulationResults && showImpactEffect && (
          <ImpactInfo 
            results={simulationResults}
            position={getTargetPosition().map(coord => coord * 1.3)}
          />
        )}

        
        
      </Canvas>

      {/* UI overlay */}
      <div style={{
        position: 'absolute',
        top: '10px',
        left: '10px',
        color: 'white',
        background: 'rgba(0,0,0,0.7)',
        padding: '10px',
        borderRadius: '5px',
        fontSize: '14px'
      }}>
        <div>🌍 Haz clic en la Tierra para seleccionar ubicación de impacto</div>
        <div>🖱️ Arrastra para rotar • Scroll para zoom</div>
        {impactLocation && (
          <div>
            📍 Impacto: {impactLocation.lat.toFixed(2)}°, {impactLocation.lon.toFixed(2)}°
          </div>
        )}
      </div>
    </div>
  );
};

export default AsteroidViewer3D;