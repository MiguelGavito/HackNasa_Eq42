import React, { useState, useEffect } from 'react';
import { 
  Container, 
  Typography, 
  Grid, 
  Card, 
  CardContent, 
  Button, 
  Box,
  Chip,
  LinearProgress,
  Paper
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import * as api from '../services/api';
import PublicIcon from '@mui/icons-material/Public';
import TimelineIcon from '@mui/icons-material/Timeline';
import WarningIcon from '@mui/icons-material/Warning';

const HomePage = () => {
  const [asteroids, setAsteroids] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchAsteroids = async () => {
      try {
        const data = await api.getAsteroids();
        setAsteroids(data);
      } catch (error) {
        console.error('Error fetching asteroids:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchAsteroids();
  }, []);

  const getRiskColor = (riskLevel) => {
    switch (riskLevel) {
      case 'HIGH': return 'error';
      case 'MEDIUM': return 'warning';
      case 'LOW': return 'success';
      default: return 'default';
    }
  };

  const formatDistance = (distance) => {
    return (distance / 1000000).toFixed(2) + 'M km';
  };

  return (
    <Container maxWidth="lg" sx={{
      py: 4,
      background: '#181c2b',
      minHeight: '100vh'
    }}>
      {/* Hero Section */}
      <Box textAlign="center" mb={6}>
        <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
          <span style={{ color: '#00ff88' }}>Meteor </span>
          <span style={{ color: '#fff' }}>Madness</span>
        </Typography>
        <Typography variant="h5" color="text.secondary" paragraph>
          Herramienta Interactiva de Simulación de Impactos de Asteroides
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          Utiliza datos reales de la NASA para modelar escenarios de impacto, 
          predecir consecuencias y evaluar estrategias de mitigación.
        </Typography>
        <Box mt={3}>
          <Button 
            variant="contained" 
            size="large" 
            onClick={() => navigate('/asteroid-launcher')}
            sx={{ mr: 2, bgcolor: '#00ff88', color: '#181c2b', fontWeight: 700 }}
          >
            Asteroid Launcher
          </Button>
          <Button 
            variant="outlined" 
            size="large" 
            onClick={() => navigate('/simulation')}
            sx={{ mr: 2, borderColor: '#fff', color: '#fff', fontWeight: 700 }}
          >
            Simulación Avanzada
          </Button>
          <Button 
            variant="outlined" 
            size="large"
            onClick={() => navigate('/risk-analysis')}
            sx={{ borderColor: '#fff', color: '#fff', fontWeight: 700 }}
          >
            Análisis de Riesgos
          </Button>
        </Box>

      </Box>

      {/* Features Section */}
      <Grid container spacing={4} mb={6}>
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%', bgcolor: 'rgba(26, 26, 46, 0.9)', border: '1px solid #00ff88' }}>
            <CardContent sx={{ textAlign: 'center' }}>
              <PublicIcon sx={{ fontSize: 60, color: '#00ff88', mb: 2 }} />
              <Typography variant="h5" component="h2" gutterBottom>
                Visualización 3D
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Representa la Tierra y asteroides en tiempo real con gráficos interactivos 3D.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%', bgcolor: 'rgba(26, 26, 46, 0.9)', border: '1px solid #fff' }}>
            <CardContent sx={{ textAlign: 'center' }}>
              <TimelineIcon sx={{ fontSize: 60, color: '#fff', mb: 2 }} />
              <Typography variant="h5" component="h2" gutterBottom>
                Simulación Avanzada
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Modela diferentes escenarios de impacto con cálculos físicos precisos.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%', bgcolor: 'rgba(26, 26, 46, 0.9)', border: '1px solid #fff' }}>
            <CardContent sx={{ textAlign: 'center' }}>
              <WarningIcon sx={{ fontSize: 60, color: '#fff', mb: 2 }} />
              <Typography variant="h5" component="h2" gutterBottom>
                Análisis de Riesgos
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Evalúa y predice consecuencias de impactos con datos científicos.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

        {/* Inspiración */}
        <Box textAlign="center" mt={2} mb={4}>
          <Typography variant="body2" color="text.secondary">
            Inspirado en neal.fun/asteroid-launcher • Simulación científicamente precisa
          </Typography>
        </Box>
      
      {loading ? (
        <Box sx={{ width: '100%', mt: 2 }}>
          <LinearProgress sx={{ bgcolor: 'rgba(0, 255, 136, 0.2)', height: 8, borderRadius: 4 }} />
        </Box>
      ) : (
        <Grid container spacing={3}>
          {asteroids.map((asteroid) => (
            <Grid item xs={12} md={6} key={asteroid.id}>
              <Card 
                sx={{ 
                  bgcolor: 'rgba(26, 26, 46, 0.9)', 
                  border: `1px solid ${asteroid.risk_level === 'HIGH' ? '#fff' : asteroid.risk_level === 'MEDIUM' ? '#fff' : '#00ff88'}`,
                  transition: 'all 0.3s ease',
                  '&:hover': {
                    transform: 'translateY(-5px)',
                    boxShadow: '0 8px 25px rgba(0, 255, 136, 0.4)'
                  }
                }}
              >
                <CardContent>
                  <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                    <Typography variant="h6" component="h3">
                      {asteroid.name}
                    </Typography>
                    <Chip 
                      label={asteroid.risk_level} 
                      color={getRiskColor(asteroid.risk_level)}
                      size="small"
                    />
                  </Box>
                  
                  <Typography variant="body2" color="text.secondary" paragraph>
                    <strong>ID:</strong> {asteroid.id}
                  </Typography>
                  
                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <Typography variant="body2">
                        <strong>Diámetro:</strong> {asteroid.diameter} km
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2">
                        <strong>Velocidad:</strong> {asteroid.velocity} km/s
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2">
                        <strong>Distancia:</strong> {formatDistance(asteroid.distance_from_earth)}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2">
                        <strong>Probabilidad:</strong> {(asteroid.impact_probability * 100).toFixed(1)}%
                      </Typography>
                    </Grid>
                  </Grid>

                  <Box mt={2}>
                    <Button 
                      variant="outlined" 
                      size="small"
                      onClick={() => navigate(`/simulation?asteroid=${asteroid.id}`)}
                      sx={{ mr: 1, borderColor: '#00ff88', color: '#00ff88' }}
                    >
                      Simular Impacto
                    </Button>
                    <Button 
                      variant="outlined" 
                      size="small"
                      onClick={() => navigate(`/risk-analysis?asteroid=${asteroid.id}`)}
                      sx={{ borderColor: '#fff', color: '#fff' }}
                    >
                      Ver Riesgos
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Container>
  );
};

export default HomePage;