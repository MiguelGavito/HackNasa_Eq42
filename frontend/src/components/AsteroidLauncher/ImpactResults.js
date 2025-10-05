import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Grid,
  Box,
  LinearProgress,
  Chip,
  Divider,
  Alert
} from '@mui/material';
import {
  FlashOn as ExplosionIcon,
  Landscape as LandscapeIcon,
  People as PeopleIcon,
  AttachMoney as MoneyIcon,
  Speed as SpeedIcon,
  Warning as WarningIcon
} from '@mui/icons-material';

const ImpactResults = ({ results, asteroidData, impactLocation }) => {
  if (!results) {
    return (
      <Card sx={{ bgcolor: 'rgba(26, 26, 46, 0.95)', border: '1px solid #666' }}>
        <CardContent>
          <Typography variant="h5" gutterBottom color="text.secondary">
            Resultados del Impacto
          </Typography>
          <Alert severity="info">
            Configura el asteroide y lanza la simulación para ver los resultados del impacto.
          </Alert>
        </CardContent>
      </Card>
    );
  }

  const formatNumber = (num) => {
    if (num >= 1e12) return (num / 1e12).toFixed(2) + 'T';
    if (num >= 1e9) return (num / 1e9).toFixed(2) + 'B';
    if (num >= 1e6) return (num / 1e6).toFixed(2) + 'M';
    if (num >= 1e3) return (num / 1e3).toFixed(2) + 'K';
    return num.toFixed(2);
  };

  const getDestructionLevel = (energy) => {
    if (energy > 100000) return { level: 'Extinción Global', color: '#ff0000', severity: 10 };
    if (energy > 10000) return { level: 'Devastación Continental', color: '#ff4400', severity: 9 };
    if (energy > 1000) return { level: 'Devastación Regional', color: '#ff6600', severity: 8 };
    if (energy > 100) return { level: 'Destrucción Masiva', color: '#ff8800', severity: 7 };
    if (energy > 10) return { level: 'Destrucción Severa', color: '#ffaa00', severity: 6 };
    if (energy > 1) return { level: 'Destrucción Local', color: '#ffcc00', severity: 5 };
    if (energy > 0.1) return { level: 'Daño Significativo', color: '#ccff00', severity: 4 };
    return { level: 'Daño Menor', color: '#88ff00', severity: 3 };
  };

  const destruction = getDestructionLevel(results.energy_released);

  const getLocationInfo = (lat, lon) => {
    // Determinar océano o continente basado en coordenadas aproximadas
    if ((lat >= -60 && lat <= 70) && (lon >= -20 && lon <= 50)) return 'África/Europa';
    if ((lat >= -55 && lat <= 70) && (lon >= -170 && lon <= -30)) return 'Américas';
    if ((lat >= -50 && lat <= 50) && (lon >= 60 && lon <= 150)) return 'Asia/Oceanía';
    if (Math.abs(lat) > 60) return lat > 0 ? 'Ártico' : 'Antártica';
    
    // Verificar si es océano (aproximación muy básica)
    const isOcean = (
      (lat >= -40 && lat <= 40 && lon >= -180 && lon <= -60) || // Pacífico
      (lat >= -40 && lat <= 60 && lon >= -40 && lon <= 20) ||   // Atlántico
      (lat >= -40 && lat <= 30 && lon >= 40 && lon <= 120)      // Índico
    );
    
    return isOcean ? 'Océano' : 'Continente';
  };

  return (
    <Card sx={{ bgcolor: 'rgba(26, 26, 46, 0.95)', border: '2px solid #ff4444' }}>
      <CardContent>
        <Typography variant="h5" gutterBottom sx={{ color: '#ff4444', display: 'flex', alignItems: 'center' }}>
          <ExplosionIcon sx={{ mr: 1 }} />
          ¡Impacto Confirmado!
        </Typography>

        {/* Nivel de Destrucción */}
        <Box sx={{ mb: 3, textAlign: 'center' }}>
          <Chip 
            label={destruction.level}
            sx={{ 
              fontSize: '1.2rem', 
              padding: '20px 15px', 
              bgcolor: destruction.color,
              color: '#000',
              fontWeight: 'bold'
            }}
          />
          <Box sx={{ mt: 2 }}>
            <Typography variant="body2" color="text.secondary">
              Escala de Destrucción
            </Typography>
            <LinearProgress 
              variant="determinate" 
              value={(destruction.severity / 10) * 100}
              sx={{ 
                height: 10, 
                borderRadius: 5,
                bgcolor: 'rgba(255,255,255,0.1)',
                '& .MuiLinearProgress-bar': {
                  bgcolor: destruction.color
                }
              }}
            />
          </Box>
        </Box>

        <Divider sx={{ my: 2 }} />

        {/* Métricas Principales */}
        <Grid container spacing={3}>
          {/* Energía Liberada */}
          <Grid item xs={12} md={6}>
            <Card sx={{ bgcolor: 'rgba(255, 68, 68, 0.1)', border: '1px solid #ff4444' }}>
              <CardContent sx={{ textAlign: 'center', py: 2 }}>
                <ExplosionIcon sx={{ fontSize: 40, color: '#ff4444', mb: 1 }} />
                <Typography variant="h4" sx={{ color: '#ff4444', fontWeight: 'bold' }}>
                  {formatNumber(results.energy_released)}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Megatones TNT
                </Typography>
                <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                  Equivale a {formatNumber(results.energy_released / 0.015)} bombas de Hiroshima
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          {/* Diámetro del Cráter */}
          <Grid item xs={12} md={6}>
            <Card sx={{ bgcolor: 'rgba(255, 107, 53, 0.1)', border: '1px solid #ff6b35' }}>
              <CardContent sx={{ textAlign: 'center', py: 2 }}>
                <LandscapeIcon sx={{ fontSize: 40, color: '#ff6b35', mb: 1 }} />
                <Typography variant="h4" sx={{ color: '#ff6b35', fontWeight: 'bold' }}>
                  {results.crater_diameter.toFixed(2)}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  km de diámetro
                </Typography>
                <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                  Cráter visible desde el espacio
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          {/* Área Afectada */}
          <Grid item xs={12} md={6}>
            <Card sx={{ bgcolor: 'rgba(255, 170, 0, 0.1)', border: '1px solid #ffaa00' }}>
              <CardContent sx={{ textAlign: 'center', py: 2 }}>
                <SpeedIcon sx={{ fontSize: 40, color: '#ffaa00', mb: 1 }} />
                <Typography variant="h4" sx={{ color: '#ffaa00', fontWeight: 'bold' }}>
                  {formatNumber(results.affected_area)}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  km² afectados
                </Typography>
                <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                  {(results.affected_area / 1000000 * 100).toFixed(2)}% del territorio de México
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          {/* Víctimas Estimadas */}
          <Grid item xs={12} md={6}>
            <Card sx={{ bgcolor: 'rgba(255, 255, 255, 0.1)', border: '1px solid #fff' }}>
              <CardContent sx={{ textAlign: 'center', py: 2 }}>
                <PeopleIcon sx={{ fontSize: 40, color: '#fff', mb: 1 }} />
                <Typography variant="h4" sx={{ color: '#fff', fontWeight: 'bold' }}>
                  {formatNumber(results.casualties_estimate)}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  víctimas estimadas
                </Typography>
                <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                  Basado en densidad poblacional
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        <Divider sx={{ my: 3 }} />

        {/* Información Adicional */}
        <Box sx={{ mb: 2 }}>
          <Typography variant="h6" gutterBottom sx={{ color: '#ffaa00' }}>
            Detalles del Impacto
          </Typography>
          
          <Grid container spacing={2}>
            <Grid item xs={12} md={4}>
              <Typography variant="body2">
                <strong>Ubicación:</strong><br />
                {impactLocation ? `${impactLocation.lat.toFixed(2)}°, ${impactLocation.lon.toFixed(2)}°` : 'N/A'}
              </Typography>
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography variant="body2">
                <strong>Región:</strong><br />
                {impactLocation ? getLocationInfo(impactLocation.lat, impactLocation.lon) : 'N/A'}
              </Typography>
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography variant="body2">
                <strong>Daño Económico:</strong><br />
                ${formatNumber(results.economic_damage)}
              </Typography>
            </Grid>
          </Grid>
        </Box>

        {/* Características del Asteroide */}
        {asteroidData && (
          <Box sx={{ p: 2, bgcolor: 'rgba(0,0,0,0.3)', borderRadius: 2 }}>
            <Typography variant="h6" gutterBottom sx={{ color: '#00ff88' }}>
              Características del Asteroide
            </Typography>
            
            <Grid container spacing={2}>
              <Grid item xs={6} md={3}>
                <Typography variant="body2">
                  <strong>Diámetro:</strong><br />
                  {asteroidData.diameter} km
                </Typography>
              </Grid>
              <Grid item xs={6} md={3}>
                <Typography variant="body2">
                  <strong>Velocidad:</strong><br />
                  {asteroidData.velocity} km/s
                </Typography>
              </Grid>
              <Grid item xs={6} md={3}>
                <Typography variant="body2">
                  <strong>Ángulo:</strong><br />
                  {asteroidData.angle}°
                </Typography>
              </Grid>
              <Grid item xs={6} md={3}>
                <Typography variant="body2">
                  <strong>Composición:</strong><br />
                  {asteroidData.composition || 'Rocky'}
                </Typography>
              </Grid>
            </Grid>
          </Box>
        )}

        {/* Advertencias */}
        {results.energy_released > 1000 && (
          <Alert severity="error" sx={{ mt: 2 }}>
            <WarningIcon sx={{ mr: 1 }} />
            <strong>Alerta Crítica:</strong> Este impacto causaría efectos globales incluyendo 
            cambio climático, lluvia ácida y posible colapso de ecosistemas.
          </Alert>
        )}
      </CardContent>
    </Card>
  );
};

export default ImpactResults;