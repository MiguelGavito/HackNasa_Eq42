import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  TextField,
  Button,
  Box,
  Alert,
  CircularProgress,
  Slider,
  FormControl,
  InputLabel,
  Select,
  MenuItem
} from '@mui/material';
import { useSearchParams } from 'react-router-dom';
import * as api from '../services/api';

const SimulationPage = () => {
  const [searchParams] = useSearchParams();
  const [asteroids, setAsteroids] = useState([]);
  const [selectedAsteroid, setSelectedAsteroid] = useState('');
  const [simulationParams, setSimulationParams] = useState({
    impact_location: { lat: 40.7589, lon: -73.9851 }, // NYC por defecto
    impact_angle: 45,
    impact_velocity: 18.5
  });
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchAsteroids = async () => {
      try {
        const data = await api.getAsteroids();
        setAsteroids(data);
        
        // Si hay un asteroide en la URL, seleccionarlo
        const asteroidFromUrl = searchParams.get('asteroid');
        if (asteroidFromUrl && data.find(a => a.id === asteroidFromUrl)) {
          setSelectedAsteroid(asteroidFromUrl);
        } else if (data.length > 0) {
          setSelectedAsteroid(data[0].id);
        }
      } catch (error) {
        setError('Error al cargar asteroides');
        console.error(error);
      }
    };

    fetchAsteroids();
  }, [searchParams]);

  const handleSimulation = async () => {
    if (!selectedAsteroid) {
      setError('Por favor selecciona un asteroide');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      const simulationData = {
        asteroid_id: selectedAsteroid,
        ...simulationParams
      };
      
      const result = await api.runSimulation(simulationData);
      setResults(result);
    } catch (error) {
      setError('Error al ejecutar la simulación');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const formatNumber = (num) => {
    if (num >= 1e9) return (num / 1e9).toFixed(2) + 'B';
    if (num >= 1e6) return (num / 1e6).toFixed(2) + 'M';
    if (num >= 1e3) return (num / 1e3).toFixed(2) + 'K';
    return num.toFixed(2);
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h3" component="h1" gutterBottom sx={{ color: '#00ff88', textAlign: 'center' }}>
        🎯 Simulación de Impacto
      </Typography>
      
      <Grid container spacing={4}>
        {/* Panel de Controles */}
        <Grid item xs={12} md={6}>
          <Card sx={{ bgcolor: 'rgba(26, 26, 46, 0.95)', border: '1px solid #00ff88' }}>
            <CardContent>
              <Typography variant="h5" component="h2" gutterBottom sx={{ color: '#00ff88' }}>
                Parámetros de Simulación
              </Typography>

              {/* Selección de Asteroide */}
              <FormControl fullWidth margin="normal">
                <InputLabel>Asteroide</InputLabel>
                <Select
                  value={selectedAsteroid}
                  label="Asteroide"
                  onChange={(e) => setSelectedAsteroid(e.target.value)}
                >
                  {asteroids.map((asteroid) => (
                    <MenuItem key={asteroid.id} value={asteroid.id}>
                      {asteroid.name} ({asteroid.diameter} km)
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>

              {/* Ubicación de Impacto */}
              <Typography variant="h6" sx={{ mt: 3, mb: 2 }}>
                Ubicación de Impacto
              </Typography>
              
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <TextField
                    fullWidth
                    label="Latitud"
                    type="number"
                    value={simulationParams.impact_location.lat}
                    onChange={(e) => setSimulationParams({
                      ...simulationParams,
                      impact_location: {
                        ...simulationParams.impact_location,
                        lat: parseFloat(e.target.value)
                      }
                    })}
                    inputProps={{ step: 0.1, min: -90, max: 90 }}
                  />
                </Grid>
                <Grid item xs={6}>
                  <TextField
                    fullWidth
                    label="Longitud"
                    type="number"
                    value={simulationParams.impact_location.lon}
                    onChange={(e) => setSimulationParams({
                      ...simulationParams,
                      impact_location: {
                        ...simulationParams.impact_location,
                        lon: parseFloat(e.target.value)
                      }
                    })}
                    inputProps={{ step: 0.1, min: -180, max: 180 }}
                  />
                </Grid>
              </Grid>

              {/* Ángulo de Impacto */}
              <Box sx={{ mt: 3 }}>
                <Typography gutterBottom>
                  Ángulo de Impacto: {simulationParams.impact_angle}°
                </Typography>
                <Slider
                  value={simulationParams.impact_angle}
                  onChange={(e, value) => setSimulationParams({
                    ...simulationParams,
                    impact_angle: value
                  })}
                  min={15}
                  max={90}
                  step={5}
                  marks
                  valueLabelDisplay="auto"
                  sx={{ color: '#00ff88' }}
                />
              </Box>

              {/* Velocidad de Impacto */}
              <Box sx={{ mt: 3 }}>
                <Typography gutterBottom>
                  Velocidad de Impacto: {simulationParams.impact_velocity} km/s
                </Typography>
                <Slider
                  value={simulationParams.impact_velocity}
                  onChange={(e, value) => setSimulationParams({
                    ...simulationParams,
                    impact_velocity: value
                  })}
                  min={11}
                  max={30}
                  step={0.5}
                  marks
                  valueLabelDisplay="auto"
                  sx={{ color: '#ff6b35' }}
                />
              </Box>

              {/* Botón de Simulación */}
              <Box sx={{ mt: 4, textAlign: 'center' }}>
                <Button
                  variant="contained"
                  size="large"
                  onClick={handleSimulation}
                  disabled={loading || !selectedAsteroid}
                  sx={{ 
                    bgcolor: '#00ff88', 
                    '&:hover': { bgcolor: '#00cc70' },
                    minWidth: 200
                  }}
                >
                  {loading ? <CircularProgress size={24} /> : 'Ejecutar Simulación'}
                </Button>
              </Box>

              {error && (
                <Alert severity="error" sx={{ mt: 2 }}>
                  {error}
                </Alert>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Panel de Resultados */}
        <Grid item xs={12} md={6}>
          <Card sx={{ bgcolor: 'rgba(26, 26, 46, 0.95)', border: '1px solid #ff6b35' }}>
            <CardContent>
              <Typography variant="h5" component="h2" gutterBottom sx={{ color: '#ff6b35' }}>
                Resultados de la Simulación
              </Typography>

              {!results && !loading && (
                <Box sx={{ textAlign: 'center', py: 4 }}>
                  <Typography variant="body1" color="text.secondary">
                    Configura los parámetros y ejecuta la simulación para ver los resultados
                  </Typography>
                </Box>
              )}

              {loading && (
                <Box sx={{ textAlign: 'center', py: 4 }}>
                  <CircularProgress sx={{ color: '#ff6b35' }} />
                  <Typography variant="body1" sx={{ mt: 2 }}>
                    Calculando impacto...
                  </Typography>
                </Box>
              )}

              {results && (
                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <Card sx={{ bgcolor: 'rgba(0, 255, 136, 0.1)', border: '1px solid rgba(0, 255, 136, 0.3)' }}>
                      <CardContent sx={{ textAlign: 'center', py: 2 }}>
                        <Typography variant="h4" sx={{ color: '#00ff88', fontWeight: 'bold' }}>
                          {results.crater_diameter.toFixed(2)}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Diámetro del Cráter (km)
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>

                  <Grid item xs={6}>
                    <Card sx={{ bgcolor: 'rgba(255, 107, 53, 0.1)', border: '1px solid rgba(255, 107, 53, 0.3)' }}>
                      <CardContent sx={{ textAlign: 'center', py: 2 }}>
                        <Typography variant="h4" sx={{ color: '#ff6b35', fontWeight: 'bold' }}>
                          {results.energy_released.toFixed(1)}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Energía (Megatones TNT)
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>

                  <Grid item xs={6}>
                    <Card sx={{ bgcolor: 'rgba(255, 170, 0, 0.1)', border: '1px solid rgba(255, 170, 0, 0.3)' }}>
                      <CardContent sx={{ textAlign: 'center', py: 2 }}>
                        <Typography variant="h4" sx={{ color: '#ffaa00', fontWeight: 'bold' }}>
                          {formatNumber(results.affected_area)}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Área Afectada (km²)
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>

                  <Grid item xs={6}>
                    <Card sx={{ bgcolor: 'rgba(255, 68, 68, 0.1)', border: '1px solid rgba(255, 68, 68, 0.3)' }}>
                      <CardContent sx={{ textAlign: 'center', py: 2 }}>
                        <Typography variant="h4" sx={{ color: '#ff4444', fontWeight: 'bold' }}>
                          {formatNumber(results.casualties_estimate)}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Víctimas Estimadas
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>

                  <Grid item xs={12}>
                    <Card sx={{ bgcolor: 'rgba(138, 43, 226, 0.1)', border: '1px solid rgba(138, 43, 226, 0.3)' }}>
                      <CardContent sx={{ textAlign: 'center', py: 2 }}>
                        <Typography variant="h4" sx={{ color: '#8a2be2', fontWeight: 'bold' }}>
                          ${formatNumber(results.economic_damage)}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Daño Económico Estimado
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                </Grid>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Información del Asteroide Seleccionado */}
      {selectedAsteroid && asteroids.length > 0 && (
        <Box sx={{ mt: 4 }}>
          <Card sx={{ bgcolor: 'rgba(26, 26, 46, 0.95)', border: '1px solid #ffaa00' }}>
            <CardContent>
              <Typography variant="h5" component="h2" gutterBottom sx={{ color: '#ffaa00' }}>
                Información del Asteroide
              </Typography>
              
              {(() => {
                const asteroid = asteroids.find(a => a.id === selectedAsteroid);
                if (!asteroid) return null;
                
                return (
                  <Grid container spacing={3}>
                    <Grid item xs={12} md={3}>
                      <Typography variant="body1">
                        <strong>Nombre:</strong> {asteroid.name}
                      </Typography>
                    </Grid>
                    <Grid item xs={12} md={3}>
                      <Typography variant="body1">
                        <strong>Diámetro:</strong> {asteroid.diameter} km
                      </Typography>
                    </Grid>
                    <Grid item xs={12} md={3}>
                      <Typography variant="body1">
                        <strong>Velocidad:</strong> {asteroid.velocity} km/s
                      </Typography>
                    </Grid>
                    <Grid item xs={12} md={3}>
                      <Typography variant="body1">
                        <strong>Nivel de Riesgo:</strong> {asteroid.risk_level}
                      </Typography>
                    </Grid>
                  </Grid>
                );
              })()}
            </CardContent>
          </Card>
        </Box>
      )}
    </Container>
  );
};

export default SimulationPage;