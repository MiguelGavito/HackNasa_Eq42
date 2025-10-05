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
  MenuItem,
} from '@mui/material';
import { useSearchParams } from 'react-router-dom';
import * as api from '../services/api';

// --- Importar Iconos de Material UI ---
import PublicIcon from '@mui/icons-material/Public'; // Para Ubicación
import SpeedIcon from '@mui/icons-material/Speed'; // Para Velocidad
import GpsFixedIcon from '@mui/icons-material/GpsFixed'; // Para Impacto
import LayersIcon from '@mui/icons-material/Layers'; // Para Cráter
import FlashOnIcon from '@mui/icons-material/FlashOn'; // Para Energía
import CropFreeIcon from '@mui/icons-material/CropFree'; // Para Área Afectada
import GroupIcon from '@mui/icons-material/Group'; // Para Víctimas
import AttachMoneyIcon from '@mui/icons-material/AttachMoney'; // Para Daño Económico
import InfoIcon from '@mui/icons-material/Info'; // Para Detalles del Asteroide

// --- Paleta Base (Monocromática) ---
const PRIMARY_BG = '#1e2a4a'; 
const CARD_BG = '#253457';
const PURE_WHITE = '#ffffff';
const TEXT_COLOR = '#e8e8e8'; 
const BORDER_COLOR = 'rgba(255, 255, 255, 0.1)';

// --- Paleta Temática para Resultados ---
const RESULT_BLUE = '#87CEEB';      // Diámetro (Físico)
const RESULT_ORANGE = '#FFB74D';    // Energía (Poder)
const RESULT_PURPLE = '#BB86FC';    // Área (Escala)
const RESULT_YELLOW = '#FFF176';    // Víctimas (Riesgo/Cautela)
const RESULT_GREEN = '#A5D6A7';     // Daño Económico (Finanzas)


// Componente de Estilo para los TextField
const DarkTextField = (props) => (
  <TextField
    {...props}
    sx={{
      '& .MuiInputBase-root': {
        color: TEXT_COLOR,
        backgroundColor: 'rgba(0, 0, 0, 0.2)',
        borderRadius: '8px',
      },
      '& .MuiOutlinedInput-root': {
        '& fieldset': {
          borderColor: BORDER_COLOR,
        },
        '&:hover fieldset': {
          borderColor: PURE_WHITE,
        },
        '&.Mui-focused fieldset': {
          borderColor: PURE_WHITE,
        },
      },
      '& .MuiInputLabel-root': {
        color: TEXT_COLOR,
        '&.Mui-focused': {
          color: PURE_WHITE,
        },
      },
    }}
  />
);

const DarkSelect = (props) => (
    <Select
        {...props}
        sx={{
            color: TEXT_COLOR,
            backgroundColor: 'rgba(0, 0, 0, 0.2)',
            borderRadius: '8px',
            '& .MuiOutlinedInput-notchedOutline': {
                borderColor: BORDER_COLOR,
            },
            '&:hover .MuiOutlinedInput-notchedOutline': {
                borderColor: PURE_WHITE,
            },
            '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                borderColor: PURE_WHITE,
            },
            '& .MuiSvgIcon-root': {
                color: TEXT_COLOR,
            }
        }}
        MenuProps={{
            PaperProps: {
                sx: {
                    bgcolor: CARD_BG,
                    color: TEXT_COLOR,
                }
            }
        }}
    >
        {props.children}
    </Select>
);

const SimulationPage = () => {
  const [searchParams] = useSearchParams();
  const [asteroids, setAsteroids] = useState([]);
  const [selectedAsteroid, setSelectedAsteroid] = useState('');
  const [simulationParams, setSimulationParams] = useState({
    impact_location: { lat: 40.7589, lon: -73.9851 },
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
  
  // Estilo base de los Sliders con animación y hover/active
  const sliderStyle = {
    transition: 'color 0.3s ease-in-out', 
    '& .MuiSlider-thumb': {
        transition: 'background-color 0.3s ease-in-out, box-shadow 0.3s ease-in-out',
        '&:hover, &.Mui-focusVisible': {
            boxShadow: '0px 0px 0px 8px rgba(255, 255, 255, 0.16)',
        },
        '&.Mui-active': {
            boxShadow: '0px 0px 0px 14px rgba(255, 255, 255, 0.16)',
        },
    },
    '& .MuiSlider-track': {
        transition: 'background-color 0.3s ease-in-out',
    },
  };

  return (
    // 1. Fondo con Gradiente Radial
    <Container maxWidth="lg" sx={{ 
        py: 4, 
        bgcolor: PRIMARY_BG, 
        backgroundImage: `radial-gradient(circle at 50% 10%, ${PRIMARY_BG}, #111a2f)`, // Gradiente
        minHeight: '100vh',
        color: TEXT_COLOR // Asegurar que el texto general sea legible
    }}>
      <Typography variant="h3" component="h1" gutterBottom sx={{ color: PURE_WHITE, textAlign: 'center', fontWeight: 'Bold', letterSpacing: '2px' }}>
        Simulación de Impacto
      </Typography>
      
      <Grid container spacing={4}>
        {/* Panel de Controles */}
        <Grid item xs={12} md={6}>
          <Card sx={{ 
            bgcolor: CARD_BG, 
            border: `1px solid ${BORDER_COLOR}`, 
            borderRadius: '16px', 
            boxShadow: '0 4px 20px rgba(0, 0, 0, 0.4)',
          }}>
            <CardContent>
              <Typography variant="h5" component="h2" gutterBottom sx={{ color: PURE_WHITE, borderBottom: `2px solid ${BORDER_COLOR}`, pb: 1, mb: 3 }}>
                Parámetros de Simulación
              </Typography>

              {/* Selección de Asteroide */}
              <FormControl fullWidth margin="normal">
                <InputLabel sx={{fontSize: '1rem', color: TEXT_COLOR }}>Asteroide</InputLabel>
                <DarkSelect
                  value={selectedAsteroid}
                  label="Asteroide"
                  onChange={(e) => setSelectedAsteroid(e.target.value)}
                >
                  {asteroids.map((asteroid) => (
                    <MenuItem key={asteroid.id} value={asteroid.id}>
                      {asteroid.name} ({asteroid.diameter} km)
                    </MenuItem>
                  ))}
                </DarkSelect>
              </FormControl>

              {/* Ubicación de Impacto */}
              <Typography variant="h6" sx={{ mt: 3, mb: 2, color: TEXT_COLOR }}>
                <PublicIcon sx={{ fontSize: 20, verticalAlign: 'middle', mr: 1 }} />
                Ubicación de Impacto
              </Typography>
              
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <DarkTextField
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
                  <DarkTextField
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
              <Box sx={{ mt: 3, color: TEXT_COLOR }}>
                <Typography gutterBottom>
                  <GpsFixedIcon sx={{ fontSize: 20, verticalAlign: 'middle', mr: 1 }} />
                  Ángulo de Impacto: **{simulationParams.impact_angle}°**
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
                  sx={{ 
                    ...sliderStyle, 
                    color: PURE_WHITE 
                  }}
                />
              </Box>

              {/* Velocidad de Impacto */}
              <Box sx={{ mt: 3, color: TEXT_COLOR }}>
                <Typography gutterBottom>
                  <SpeedIcon sx={{ fontSize: 20, verticalAlign: 'middle', mr: 1 }} />
                  Velocidad de Impacto: **{simulationParams.impact_velocity} km/s**
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
                  sx={{ 
                    ...sliderStyle, 
                    color: TEXT_COLOR 
                  }}
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
                    bgcolor: PURE_WHITE,
                    color: PRIMARY_BG,
                    fontWeight: 'bold',
                    borderRadius: '50px',
                    padding: '10px 30px',
                    transition: 'all 0.3s ease',
                    '&:hover': { 
                        bgcolor: TEXT_COLOR,
                        transform: 'scale(1.02)',
                        // 3. Efecto de Sombra (Glow)
                        boxShadow: '0 0 15px rgba(255, 255, 255, 0.4)', 
                    },
                     '&:active': { // Animación al presionar
                        transform: 'scale(0.98)',
                        boxShadow: '0 0 10px rgba(255, 255, 255, 0.3)',
                    },
                    minWidth: 200
                  }}
                >
                  {loading ? <CircularProgress size={24} sx={{ color: PRIMARY_BG }} /> : 'Ejecutar Simulación'}
                </Button>
              </Box>

              {error && (
                <Alert severity="error" sx={{ mt: 2, bgcolor: 'rgba(255, 255, 255, 0.1)', color: PURE_WHITE }}>
                  {error}
                </Alert>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Panel de Resultados */}
        <Grid item xs={12} md={6}>
          <Card sx={{ 
            bgcolor: CARD_BG, 
            border: `1px solid ${PURE_WHITE}`,
            borderRadius: '16px',
            boxShadow: '0 4px 20px rgba(0, 0, 0, 0.4)',
          }}>
            <CardContent>
              <Typography variant="h5" component="h2" gutterBottom sx={{ color: PURE_WHITE, borderBottom: `2px solid ${PURE_WHITE}`, pb: 1, mb: 3 }}>
                Resultados de la Simulación
              </Typography>

              {!results && !loading && (
                <Box sx={{ textAlign: 'center', py: 4, color: TEXT_COLOR }}>
                  <Typography variant="body1" color="inherit">
                    Configura los parámetros y pulsa 'Ejecutar Simulación' para ver el impacto.
                  </Typography>
                </Box>
              )}

              {loading && (
                <Box sx={{ textAlign: 'center', py: 4, color: PURE_WHITE }}>
                  <CircularProgress color="inherit" />
                  <Typography variant="body1" sx={{ mt: 2, color: TEXT_COLOR }}>
                    Calculando impacto...
                  </Typography>
                </Box>
              )}

              {results && (
                <Grid container spacing={2}>
                  {/* Diámetro del Cráter - Azul */}
                  <Grid item xs={6}>
                    <Card sx={{ bgcolor: 'rgba(135, 206, 235, 0.1)', border: `1px solid ${RESULT_BLUE}` }}>
                      <CardContent sx={{ textAlign: 'center', py: 2 }}>
                        <Typography variant="h4" sx={{ color: RESULT_BLUE, fontWeight: 'bold' }}>
                          {results.crater_diameter.toFixed(2)}
                        </Typography>
                        <Typography variant="body2" sx={{ color: TEXT_COLOR }}>
                          <LayersIcon sx={{ fontSize: 16, verticalAlign: 'middle', mr: 0.5, color: RESULT_BLUE }} />
                          Diámetro del Cráter (km)
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>

                  {/* Energía Liberada - Naranja */}
                  <Grid item xs={6}>
                    <Card sx={{ bgcolor: 'rgba(255, 183, 77, 0.1)', border: `1px solid ${RESULT_ORANGE}` }}>
                      <CardContent sx={{ textAlign: 'center', py: 2 }}>
                        <Typography variant="h4" sx={{ color: RESULT_ORANGE, fontWeight: 'bold' }}>
                          {results.energy_released.toFixed(1)}
                        </Typography>
                        <Typography variant="body2" sx={{ color: TEXT_COLOR }}>
                          <FlashOnIcon sx={{ fontSize: 16, verticalAlign: 'middle', mr: 0.5, color: RESULT_ORANGE }} />
                          Energía (Megatones TNT)
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>

                  {/* Área Afectada - Púrpura */}
                  <Grid item xs={6}>
                    <Card sx={{ bgcolor: 'rgba(187, 134, 252, 0.1)', border: `1px solid ${RESULT_PURPLE}` }}>
                      <CardContent sx={{ textAlign: 'center', py: 2 }}>
                        <Typography variant="h4" sx={{ color: RESULT_PURPLE, fontWeight: 'bold' }}>
                          {formatNumber(results.affected_area)}
                        </Typography>
                        <Typography variant="body2" sx={{ color: TEXT_COLOR }}>
                          <CropFreeIcon sx={{ fontSize: 16, verticalAlign: 'middle', mr: 0.5, color: RESULT_PURPLE }} />
                          Área Afectada (km²)
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>

                  {/* Víctimas Estimadas - Amarillo */}
                  <Grid item xs={6}>
                    <Card sx={{ bgcolor: 'rgba(255, 241, 118, 0.1)', border: `1px solid ${RESULT_YELLOW}` }}>
                      <CardContent sx={{ textAlign: 'center', py: 2 }}>
                        <Typography variant="h4" sx={{ color: RESULT_YELLOW, fontWeight: 'bold' }}>
                          {formatNumber(results.casualties_estimate)}
                        </Typography>
                        <Typography variant="body2" sx={{ color: TEXT_COLOR }}>
                          <GroupIcon sx={{ fontSize: 16, verticalAlign: 'middle', mr: 0.5, color: RESULT_YELLOW }} />
                          Víctimas Estimadas
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>

                  {/* Daño Económico - Verde */}
                  <Grid item xs={12}>
                    <Card sx={{ bgcolor: 'rgba(165, 214, 167, 0.1)', border: `1px solid ${RESULT_GREEN}` }}>
                      <CardContent sx={{ textAlign: 'center', py: 2 }}>
                        <Typography variant="h4" sx={{ color: RESULT_GREEN, fontWeight: 'bold' }}>
                          ${formatNumber(results.economic_damage)}
                        </Typography>
                        <Typography variant="body2" sx={{ color: TEXT_COLOR }}>
                          <AttachMoneyIcon sx={{ fontSize: 16, verticalAlign: 'middle', mr: 0.5, color: RESULT_GREEN }} />
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
          <Card sx={{ 
            bgcolor: CARD_BG, 
            border: `1px solid ${BORDER_COLOR}`,
            borderRadius: '16px',
            boxShadow: '0 4px 10px rgba(0, 0, 0, 0.3)',
          }}>
            <CardContent>
              <Typography variant="h5" component="h2" gutterBottom sx={{ color: PURE_WHITE, borderBottom: `2px solid ${BORDER_COLOR}`, pb: 1, mb: 3 }}>
                <InfoIcon sx={{ fontSize: 24, verticalAlign: 'middle', mr: 1, color: PURE_WHITE }} />
                Detalles del Asteroide
              </Typography>
              
              {(() => {
                const asteroid = asteroids.find(a => a.id === selectedAsteroid);
                if (!asteroid) return null;
                
                return (
                  <Grid container spacing={3}>
                    <Grid item xs={12} md={3}>
                      <Typography variant="body1" sx={{ color: TEXT_COLOR }}>
                        <strong>Nombre:</strong> {asteroid.name}
                      </Typography>
                    </Grid>
                    <Grid item xs={12} md={3}>
                      <Typography variant="body1" sx={{ color: TEXT_COLOR }}>
                        <strong>Diámetro:</strong> <span style={{ color: PURE_WHITE }}>{asteroid.diameter} km</span>
                      </Typography>
                    </Grid>
                    <Grid item xs={12} md={3}>
                      <Typography variant="body1" sx={{ color: TEXT_COLOR }}>
                        <strong>Velocidad Orbital:</strong> {asteroid.velocity} km/s
                      </Typography>
                    </Grid>
                    <Grid item xs={12} md={3}>
                      <Typography variant="body1" sx={{ color: TEXT_COLOR }}>
                        <strong>Nivel de Riesgo:</strong> <span style={{ color: PURE_WHITE }}>{asteroid.risk_level}</span>
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