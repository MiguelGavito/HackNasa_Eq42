import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Slider,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Button,
  Chip,
  Grid,
  Tooltip,
  Alert
} from '@mui/material';
import { 
  Tune as TuneIcon,
  Speed as SpeedIcon,
  Straighten as SizeIcon,
  LocationOn as LocationIcon,
  PlayArrow as LaunchIcon
} from '@mui/icons-material';

const AsteroidControls = ({ 
  asteroidData, 
  onAsteroidChange, 
  onLaunch,
  impactLocation,
  isSimulating
}) => {
  const [localData, setLocalData] = useState({
    diameter: 1.0,        // km
    velocity: 20.0,       // km/s
    angle: 45,            // grados
    composition: 'rocky', // tipo de asteroide
    density: 2500,        // kg/m³
    ...asteroidData
  });

  const compositions = {
    rocky: { name: 'Rocoso', density: 2500, color: '#8B4513' },
    metallic: { name: 'Metálico', density: 7800, color: '#C0C0C0' },
    icy: { name: 'Helado', density: 900, color: '#E0F6FF' }
  };

  const predefinedAsteroids = [
    { name: 'Tunguska (1908)', diameter: 0.06, velocity: 27, composition: 'rocky' },
    { name: 'Chelyabinsk (2013)', diameter: 0.02, velocity: 19, composition: 'rocky' },
    { name: 'Chicxulub (Dinosaurios)', diameter: 10, velocity: 20, composition: 'rocky' },
    { name: 'Apophis (Hipotético)', diameter: 0.34, velocity: 12.8, composition: 'rocky' },
    { name: 'Asteroide Personalizado', diameter: localData.diameter, velocity: localData.velocity, composition: localData.composition }
  ];

  const [selectedPreset, setSelectedPreset] = useState('Asteroide Personalizado');

  const handleDataChange = (field, value) => {
    const newData = { ...localData, [field]: value };
    
    // Actualizar densidad automáticamente según composición
    if (field === 'composition') {
      newData.density = compositions[value].density;
    }
    
    setLocalData(newData);
    onAsteroidChange(newData);
  };

  const handlePresetChange = (presetName) => {
    setSelectedPreset(presetName);
    const preset = predefinedAsteroids.find(p => p.name === presetName);
    if (preset && presetName !== 'Asteroide Personalizado') {
      const newData = {
        ...localData,
        diameter: preset.diameter,
        velocity: preset.velocity,
        composition: preset.composition,
        density: compositions[preset.composition].density
      };
      setLocalData(newData);
      onAsteroidChange(newData);
    }
  };

  const calculateEnergy = () => {
    // Energía cinética aproximada en megatones TNT
    const mass = (4/3) * Math.PI * Math.pow((localData.diameter * 500), 3) * localData.density; // kg
    const energyJoules = 0.5 * mass * Math.pow(localData.velocity * 1000, 2);
    const energyMegatons = energyJoules / (4.184e15);
    return energyMegatons;
  };

  const calculateImpactForce = () => {
    // Fuerza de impacto aproximada
    const energy = calculateEnergy();
    if (energy > 1000000) return 'Extinción masiva';
    if (energy > 100000) return 'Devastación global';
    if (energy > 1000) return 'Devastación regional';
    if (energy > 100) return 'Destrucción local masiva';
    if (energy > 1) return 'Destrucción local';
    return 'Daño menor';
  };

  const getRiskColor = () => {
    const energy = calculateEnergy();
    if (energy > 100000) return 'error';
    if (energy > 1000) return 'warning';
    if (energy > 1) return 'info';
    return 'success';
  };

  const formatNumber = (num) => {
    if (num >= 1e6) return (num / 1e6).toFixed(2) + 'M';
    if (num >= 1e3) return (num / 1e3).toFixed(2) + 'K';
    return num.toFixed(2);
  };

  return (
    <Card sx={{ bgcolor: 'rgba(26, 26, 46, 0.95)', border: '1px solid #00ff88' }}>
      <CardContent>
        <Typography variant="h5" gutterBottom sx={{ color: '#00ff88', display: 'flex', alignItems: 'center' }}>
          <TuneIcon sx={{ mr: 1 }} />
          Configuración del Asteroide
        </Typography>

        {/* Asteroides Predefinidos */}
        <Box sx={{ mb: 3 }}>
          <FormControl fullWidth margin="normal">
            <InputLabel>Asteroide Predefinido</InputLabel>
            <Select
              value={selectedPreset}
              label="Asteroide Predefinido"
              onChange={(e) => handlePresetChange(e.target.value)}
            >
              {predefinedAsteroids.map((preset) => (
                <MenuItem key={preset.name} value={preset.name}>
                  {preset.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Box>

        {/* Tamaño del Asteroide */}
        <Box sx={{ mb: 3 }}>
          <Typography gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
            <SizeIcon sx={{ mr: 1 }} />
            Diámetro: {localData.diameter} km
          </Typography>
          {/* Custom marks con Tooltip para mostrar label solo en hover */}
          <Slider
            value={localData.diameter}
            onChange={(e, value) => handleDataChange('diameter', value)}
            min={0.01}
            max={15}
            step={0.01}
            marks={[
              { value: 0.02, label: Math.abs(localData.diameter - 0.02) < 0.0001 ? 'Chelyabinsk' : '' },
              { value: 0.06, label: Math.abs(localData.diameter - 0.06) < 0.0001 ? 'Tunguska' : '' },
              { value: 0.34, label: Math.abs(localData.diameter - 0.34) < 0.0001 ? 'Apophis' : '' },
              { value: 1, label: Math.abs(localData.diameter - 1) < 0.0001 ? '1 km' : '' },
              { value: 10, label: Math.abs(localData.diameter - 10) < 0.0001 ? 'Chicxulub' : '' }
            ]}
            sx={{ color: '#00ff88',
              '& .MuiSlider-markLabel': {
                textAlign: 'right !important',
                width: '30%',
                display: 'block'
              }
            }}
          />
          <Typography variant="caption" color="text.secondary">
            Referencia: Chelyabinsk (20m), Tunguska (60m), Chicxulub (10km)
          </Typography>
        </Box>

        {/* Velocidad de Impacto */}
        <Box sx={{ mb: 3 }}>
          <Typography gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
            <SpeedIcon sx={{ mr: 1 }} />
            Velocidad: {localData.velocity} km/s
          </Typography>
          <Slider
            value={localData.velocity}
            onChange={(e, value) => handleDataChange('velocity', value)}
            min={11}
            max={72}
            step={0.1}
            marks={[
              { value: 11, label: 'Mín' },
              { value: 20, label: 'Típico' },
              { value: 40, label: 'Rápido' },
              { value: 72, label: 'Máx' }
            ]}
            sx={{ color: '#ff6b35' }}
          />
          <Typography variant="caption" color="text.secondary">
            Velocidad de escape terrestre: 11 km/s | Máxima observada: ~72 km/s
          </Typography>
        </Box>

        {/* Ángulo de Impacto */}
        <Box sx={{ mb: 3 }}>
          <Typography gutterBottom>
            Ángulo de Impacto: {localData.angle}°
          </Typography>
          <Slider
            value={localData.angle}
            onChange={(e, value) => handleDataChange('angle', value)}
            min={15}
            max={90}
            step={5}
            marks={[
              { value: 15, label: '15°' },
              { value: 45, label: '45°' },
              { value: 90, label: '90°' }
            ]}
            sx={{ color: '#ffaa00' }}
          />
          <Typography variant="caption" color="text.secondary">
            Ángulos bajos son más destructivos horizontalmente
          </Typography>
        </Box>

        {/* Composición */}
        <Box sx={{ mb: 3 }}>
          <FormControl fullWidth margin="normal">
            <InputLabel>Composición</InputLabel>
            <Select
              value={localData.composition}
              label="Composición"
              onChange={(e) => handleDataChange('composition', e.target.value)}
            >
              {Object.entries(compositions).map(([key, comp]) => (
                <MenuItem key={key} value={key}>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <Box 
                      sx={{ 
                        width: 16, 
                        height: 16, 
                        backgroundColor: comp.color, 
                        borderRadius: '50%', 
                        mr: 2 
                      }} 
                    />
                    {comp.name} ({comp.density} kg/m³)
                  </Box>
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Box>

        {/* Ubicación de Impacto */}
        <Box sx={{ mb: 3 }}>
          <Typography gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
            <LocationIcon sx={{ mr: 1 }} />
            Ubicación de Impacto
          </Typography>
          {impactLocation ? (
            <Box>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <TextField
                    label="Latitud"
                    value={impactLocation.lat.toFixed(4)}
                    size="small"
                    InputProps={{ readOnly: true }}
                  />
                </Grid>
                <Grid item xs={6}>
                  <TextField
                    label="Longitud"
                    value={impactLocation.lon.toFixed(4)}
                    size="small"
                    InputProps={{ readOnly: true }}
                  />
                </Grid>
              </Grid>
            </Box>
          ) : (
            <Alert severity="info">
              Haz clic en la Tierra para seleccionar ubicación de impacto
            </Alert>
          )}
        </Box>

        {/* Estadísticas del Impacto */}
        <Box sx={{ mb: 3, p: 2, bgcolor: 'rgba(0,0,0,0.3)', borderRadius: 2 }}>
          <Typography variant="h6" gutterBottom>
            Predicción de Impacto
          </Typography>
          
          <Grid container spacing={2}>
            <Grid item xs={6}>
              <Tooltip title="Energía cinética total liberada">
                <Chip 
                  label={`${formatNumber(calculateEnergy())} MT TNT`}
                  color={getRiskColor()}
                  size="small"
                />
              </Tooltip>
            </Grid>
            <Grid item xs={6}>
              <Tooltip title="Nivel de destrucción estimado">
                <Chip 
                  label={calculateImpactForce()}
                  color={getRiskColor()}
                  size="small"
                />
              </Tooltip>
            </Grid>
          </Grid>

          <Typography variant="caption" display="block" sx={{ mt: 1 }}>
            Masa estimada: {formatNumber((4/3) * Math.PI * Math.pow((localData.diameter * 500), 3) * localData.density / 1e12)} millones de toneladas
          </Typography>
        </Box>

        {/* Botón de Lanzar */}
        <Button
          variant="contained"
          size="large"
          fullWidth
          onClick={onLaunch}
          disabled={!impactLocation || isSimulating}
          sx={{ 
            bgcolor: '#ff4444',
            '&:hover': { bgcolor: '#cc3333' },
            '&:disabled': { bgcolor: '#666' }
          }}
          startIcon={<LaunchIcon />}
        >
          {isSimulating ? 'Simulando...' : '🚀 Lanzar Asteroide'}
        </Button>

        {!impactLocation && (
          <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block', textAlign: 'center' }}>
            Selecciona una ubicación en la Tierra para habilitar el lanzamiento
          </Typography>
        )}
      </CardContent>
    </Card>
  );
};

export default AsteroidControls;