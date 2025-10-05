import React, { useState, useEffect } from 'react';
import { Container, Grid, Box, Typography, Fab } from '@mui/material';
import { Refresh as RefreshIcon } from '@mui/icons-material';
import AsteroidViewer3D from './AsteroidViewer3D';
import AsteroidControls from './AsteroidControls';
import ImpactResults from './ImpactResults';
import * as api from '../../services/api';

const AsteroidLauncher = () => {
  const [asteroidData, setAsteroidData] = useState({
    diameter: 1.0,
    velocity: 20.0,
    angle: 45,
    composition: 'rocky',
    density: 2500
  });
  
  const [impactLocation, setImpactLocation] = useState(null);
  const [simulationResults, setSimulationResults] = useState(null);
  const [isSimulating, setIsSimulating] = useState(false);
  const [showImpactEffect, setShowImpactEffect] = useState(false);

  const handleAsteroidChange = (newData) => {
    setAsteroidData(newData);
    // Limpiar resultados anteriores cuando cambian los parámetros
    setSimulationResults(null);
    setShowImpactEffect(false);
  };

  const handleLocationSelect = (location) => {
    setImpactLocation(location);
    // Limpiar resultados anteriores cuando cambia la ubicación
    setSimulationResults(null);
    setShowImpactEffect(false);
  };

  const handleLaunch = async () => {
    if (!impactLocation) return;

    setIsSimulating(true);
    setShowImpactEffect(false);
    setSimulationResults(null);

    try {
      // Preparar datos para la simulación
      const simulationData = {
        asteroid_id: 'custom-asteroid',
        impact_location: impactLocation,
        impact_angle: asteroidData.angle,
        impact_velocity: asteroidData.velocity,
        asteroid_diameter: asteroidData.diameter,
        asteroid_composition: asteroidData.composition,
        asteroid_density: asteroidData.density
      };

      // Esperar un poco para el efecto visual
      setTimeout(() => {
        setShowImpactEffect(true);
      }, 2000);

      // Ejecutar simulación
      const results = await api.runSimulation(simulationData);
      
      // Mostrar resultados después del efecto visual
      setTimeout(() => {
        setSimulationResults(results);
      }, 3000);

    } catch (error) {
      console.error('Error en la simulación:', error);
      // En caso de error, usar cálculos locales básicos
      const fallbackResults = calculateFallbackResults();
      setTimeout(() => {
        setSimulationResults(fallbackResults);
        setShowImpactEffect(true);
      }, 2000);
    } finally {
      setTimeout(() => {
        setIsSimulating(false);
      }, 4000);
    }
  };

  const calculateFallbackResults = () => {
    // Cálculos básicos locales como backup
    const radius = asteroidData.diameter / 2;
    const volume = (4/3) * Math.PI * Math.pow(radius * 1000, 3); // m³
    const mass = volume * asteroidData.density; // kg
    const energy = 0.5 * mass * Math.pow(asteroidData.velocity * 1000, 2); // Joules
    const energyMT = energy / (4.184e15); // Megatons TNT
    
    const craterDiameter = Math.pow(energyMT / 1000, 0.25) * asteroidData.diameter * 20;
    const affectedArea = Math.PI * Math.pow(craterDiameter * 10, 2);
    const casualties = Math.floor(affectedArea * 50 * 0.3); // Estimación básica
    const economicDamage = affectedArea * 1e8;
    
    return {
      crater_diameter: craterDiameter,
      energy_released: energyMT,
      affected_area: affectedArea,
      casualties_estimate: casualties,
      economic_damage: economicDamage
    };
  };

  const handleReset = () => {
    setImpactLocation(null);
    setSimulationResults(null);
    setShowImpactEffect(false);
    setIsSimulating(false);
    setAsteroidData({
      diameter: 1.0,
      velocity: 20.0,
      angle: 45,
      composition: 'rocky',
      density: 2500
    });
  };

  return (
    <Container maxWidth="xl" sx={{ py: 2 }}>
      {/* Header */}
      <Box textAlign="center" mb={3}>
        <Typography variant="h3" component="h1" gutterBottom sx={{ color: '#ff4444', fontWeight: 'bold' }}>
          Asteroid Launcher
        </Typography>
        <Typography variant="h6" color="text.secondary" paragraph>
          Simula impactos de asteroides y descubre su poder destructivo
        </Typography>
      </Box>

      <Grid container spacing={3}>
        {/* Visualización 3D */}
        <Grid item xs={12} lg={8}>
          <Box sx={{ position: 'relative' }}>
            <AsteroidViewer3D
              asteroidData={asteroidData}
              impactLocation={impactLocation}
              simulationResults={simulationResults}
              onLocationSelect={handleLocationSelect}
              isSimulating={isSimulating}
              showImpactEffect={showImpactEffect}
            />
            
            {/* Botón de Reset */}
            <Fab
              color="secondary"
              size="small"
              onClick={handleReset}
              sx={{
                position: 'absolute',
                top: 16,
                right: 16,
                bgcolor: '#666',
                '&:hover': { bgcolor: '#888' }
              }}
            >
              <RefreshIcon />
            </Fab>
          </Box>
        </Grid>

        {/* Controles */}
        <Grid item xs={12} lg={4}>
          <AsteroidControls
            asteroidData={asteroidData}
            onAsteroidChange={handleAsteroidChange}
            onLaunch={handleLaunch}
            impactLocation={impactLocation}
            isSimulating={isSimulating}
          />
        </Grid>

        {/* Resultados */}
        <Grid item xs={12}>
          <ImpactResults
            results={simulationResults}
            asteroidData={asteroidData}
            impactLocation={impactLocation}
          />
        </Grid>
      </Grid>

      {/* Información adicional */}
      <Box sx={{ mt: 4, p: 3, bgcolor: 'rgba(26, 26, 46, 0.5)', borderRadius: 2 }}>
        <Typography variant="h6" gutterBottom sx={{ color: '#00ff88' }}>
          ℹ️ Cómo usar el Asteroid Launcher
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} md={3}>
            <Typography variant="body2">
              <strong>1. Configura el asteroide:</strong> Ajusta tamaño, velocidad, ángulo y composición
            </Typography>
          </Grid>
          <Grid item xs={12} md={3}>
            <Typography variant="body2">
              <strong>2. Selecciona el objetivo:</strong> Haz clic en la Tierra para elegir el punto de impacto
            </Typography>
          </Grid>
          <Grid item xs={12} md={3}>
            <Typography variant="body2">
              <strong>3. Lanza el asteroide:</strong> Presiona el botón de lanzar para iniciar la simulación
            </Typography>
          </Grid>
          <Grid item xs={12} md={3}>
            <Typography variant="body2">
              <strong>4. Observa los resultados:</strong> Analiza el daño causado y los efectos del impacto
            </Typography>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default AsteroidLauncher;