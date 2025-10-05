import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Box,
  Alert,
  CircularProgress,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  LinearProgress
} from '@mui/material';
import { useSearchParams } from 'react-router-dom';
import * as api from '../services/api';
import WarningIcon from '@mui/icons-material/Warning';
import SecurityIcon from '@mui/icons-material/Security';
import TimelineIcon from '@mui/icons-material/Timeline';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import RocketLaunchIcon from '@mui/icons-material/RocketLaunch';

const RiskAnalysisPage = () => {
  const [searchParams] = useSearchParams();
  const [asteroids, setAsteroids] = useState([]);
  const [selectedAsteroid, setSelectedAsteroid] = useState('');
  const [riskAnalysis, setRiskAnalysis] = useState(null);
  const [mitigationStrategies, setMitigationStrategies] = useState(null);
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

  useEffect(() => {
    if (selectedAsteroid) {
      fetchAnalysis();
    }
  }, [selectedAsteroid]);

  const fetchAnalysis = async () => {
    if (!selectedAsteroid) return;

    setLoading(true);
    setError('');
    
    try {
      const [riskData, mitigationData] = await Promise.all([
        api.getRiskAnalysis(selectedAsteroid),
        api.getMitigationStrategies(selectedAsteroid)
      ]);
      
      setRiskAnalysis(riskData);
      setMitigationStrategies(mitigationData);
    } catch (error) {
      setError('Error al cargar el análisis de riesgos');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (score) => {
    if (score >= 0.7) return '#ff4444';
    if (score >= 0.4) return '#ffaa00';
    return '#00ff88';
  };

  const getUrgencyColor = (urgency) => {
    switch (urgency) {
      case 'HIGH': return 'error';
      case 'MEDIUM': return 'warning';
      case 'LOW': return 'success';
      default: return 'default';
    }
  };

  const formatCost = (cost) => {
    if (cost >= 1e9) return `$${(cost / 1e9).toFixed(1)}B`;
    if (cost >= 1e6) return `$${(cost / 1e6).toFixed(1)}M`;
    return `$${cost.toLocaleString()}`;
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h3" component="h1" gutterBottom sx={{ color: '#ff6b35', textAlign: 'center' }}>
        Análisis de Riesgos
      </Typography>

      {/* Selector de Asteroide */}
      <Box sx={{ mb: 4 }}>
        <FormControl fullWidth>
          <InputLabel>Seleccionar Asteroide</InputLabel>
          <Select
            value={selectedAsteroid}
            label="Seleccionar Asteroide"
            onChange={(e) => setSelectedAsteroid(e.target.value)}
          >
            {asteroids.map((asteroid) => (
              <MenuItem key={asteroid.id} value={asteroid.id}>
                {asteroid.name} - Riesgo: {asteroid.risk_level}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 4 }}>
          {error}
        </Alert>
      )}

      {loading && (
        <Box sx={{ textAlign: 'center', py: 4 }}>
          <CircularProgress sx={{ color: '#ff6b35' }} />
          <Typography variant="body1" sx={{ mt: 2 }}>
            Analizando riesgos...
          </Typography>
        </Box>
      )}

      {riskAnalysis && mitigationStrategies && (
        <Grid container spacing={4}>
          {/* Panel de Análisis de Riesgo */}
          <Grid item xs={12} md={6}>
            <Card sx={{ bgcolor: 'rgba(26, 26, 46, 0.95)', border: '1px solid #ff6b35', height: '100%' }}>
              <CardContent>
                <Typography variant="h5" component="h2" gutterBottom sx={{ color: '#ff6b35' }}>
                  <WarningIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Evaluación de Riesgo
                </Typography>

                {/* Score General de Riesgo */}
                <Box sx={{ mb: 3, textAlign: 'center' }}>
                  <Typography variant="h2" sx={{ 
                    color: getRiskColor(riskAnalysis.overall_risk_score),
                    fontWeight: 'bold'
                  }}>
                    {(riskAnalysis.overall_risk_score * 100).toFixed(0)}%
                  </Typography>
                  <Typography variant="h6" color="text.secondary">
                    Puntuación General de Riesgo
                  </Typography>
                  <Chip 
                    label={riskAnalysis.mitigation_urgency}
                    color={getUrgencyColor(riskAnalysis.mitigation_urgency)}
                    sx={{ mt: 1 }}
                  />
                </Box>

                {/* Factores de Riesgo */}
                <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
                  Factores de Riesgo
                </Typography>

                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" gutterBottom>
                    Tamaño: {(riskAnalysis.risk_factors.size * 100).toFixed(0)}%
                  </Typography>
                  <LinearProgress 
                    variant="determinate" 
                    value={riskAnalysis.risk_factors.size * 100} 
                    sx={{ 
                      height: 8, 
                      backgroundColor: 'rgba(255, 255, 255, 0.1)',
                      '& .MuiLinearProgress-bar': { backgroundColor: '#00ff88' }
                    }} 
                  />
                </Box>

                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" gutterBottom>
                    Velocidad: {(riskAnalysis.risk_factors.velocity * 100).toFixed(0)}%
                  </Typography>
                  <LinearProgress 
                    variant="determinate" 
                    value={riskAnalysis.risk_factors.velocity * 100} 
                    sx={{ 
                      height: 8, 
                      backgroundColor: 'rgba(255, 255, 255, 0.1)',
                      '& .MuiLinearProgress-bar': { backgroundColor: '#ffaa00' }
                    }} 
                  />
                </Box>

                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" gutterBottom>
                    Proximidad: {(riskAnalysis.risk_factors.proximity * 100).toFixed(0)}%
                  </Typography>
                  <LinearProgress 
                    variant="determinate" 
                    value={riskAnalysis.risk_factors.proximity * 100} 
                    sx={{ 
                      height: 8, 
                      backgroundColor: 'rgba(255, 255, 255, 0.1)',
                      '& .MuiLinearProgress-bar': { backgroundColor: '#ff4444' }
                    }} 
                  />
                </Box>

                {/* Información Temporal */}
                <Box sx={{ mt: 3 }}>
                  <Typography variant="body1" sx={{ mb: 1 }}>
                    <TimelineIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                    <strong>Tiempo de Detección:</strong> {riskAnalysis.estimated_detection_time}
                  </Typography>
                  <Typography variant="body1">
                    <strong>Línea de Tiempo de Decisión:</strong> {mitigationStrategies.decision_timeline}
                  </Typography>
                </Box>

                {/* Acciones Recomendadas */}
                <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
                  Acciones Recomendadas
                </Typography>
                <List dense>
                  {riskAnalysis.recommended_actions.map((action, index) => (
                    <ListItem key={index}>
                      <ListItemIcon>
                        <SecurityIcon sx={{ color: '#00ff88' }} />
                      </ListItemIcon>
                      <ListItemText primary={action} />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Grid>

          {/* Panel de Estrategias de Mitigación */}
          <Grid item xs={12} md={6}>
            <Card sx={{ bgcolor: 'rgba(26, 26, 46, 0.95)', border: '1px solid #00ff88', height: '100%' }}>
              <CardContent>
                <Typography variant="h5" component="h2" gutterBottom sx={{ color: '#00ff88' }}>
                  <RocketLaunchIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Estrategias de Mitigación
                </Typography>

                {/* Estrategia Recomendada */}
                <Box sx={{ mb: 3, p: 2, bgcolor: 'rgba(0, 255, 136, 0.1)', borderRadius: 2 }}>
                  <Typography variant="h6" sx={{ color: '#00ff88' }}>
                    Estrategia Recomendada
                  </Typography>
                  <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
                    {mitigationStrategies.recommended_strategy}
                  </Typography>
                </Box>

                {/* Lista de Estrategias Disponibles */}
                <Typography variant="h6" gutterBottom>
                  Opciones Disponibles
                </Typography>

                {mitigationStrategies.available_strategies.map((strategy, index) => (
                  <Card key={index} sx={{ 
                    mb: 2, 
                    bgcolor: 'rgba(0, 0, 0, 0.3)', 
                    border: strategy.name === mitigationStrategies.recommended_strategy ? 
                      '2px solid #00ff88' : '1px solid rgba(255, 255, 255, 0.2)'
                  }}>
                    <CardContent sx={{ py: 2 }}>
                      <Typography variant="h6" component="h3" gutterBottom>
                        {strategy.name}
                        {strategy.name === mitigationStrategies.recommended_strategy && (
                          <Chip 
                            label="RECOMENDADA" 
                            color="success" 
                            size="small" 
                            sx={{ ml: 2 }} 
                          />
                        )}
                      </Typography>
                      
                      <Typography variant="body2" color="text.secondary" paragraph>
                        {strategy.description}
                      </Typography>

                      <Grid container spacing={2}>
                        <Grid item xs={6}>
                          <Typography variant="caption" display="block">
                            Probabilidad de Éxito
                          </Typography>
                          <Typography variant="body1" sx={{ color: '#00ff88' }}>
                            {(strategy.success_probability * 100).toFixed(0)}%
                          </Typography>
                        </Grid>
                        <Grid item xs={6}>
                          <Typography variant="caption" display="block">
                            Costo Estimado
                          </Typography>
                          <Typography variant="body1" sx={{ color: '#ffaa00' }}>
                            {formatCost(strategy.cost_estimate)}
                          </Typography>
                        </Grid>
                        <Grid item xs={6}>
                          <Typography variant="caption" display="block">
                            Tiempo de Preparación
                          </Typography>
                          <Typography variant="body1">
                            {strategy.preparation_time}
                          </Typography>
                        </Grid>
                        <Grid item xs={6}>
                          <Typography variant="caption" display="block">
                            Efectividad
                          </Typography>
                          <Typography variant="body1">
                            {strategy.effectiveness}
                          </Typography>
                        </Grid>
                      </Grid>
                    </CardContent>
                  </Card>
                ))}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

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
                    <Grid item xs={12} md={2}>
                      <Typography variant="body1">
                        <strong>Nombre:</strong><br />{asteroid.name}
                      </Typography>
                    </Grid>
                    <Grid item xs={12} md={2}>
                      <Typography variant="body1">
                        <strong>Diámetro:</strong><br />{asteroid.diameter} km
                      </Typography>
                    </Grid>
                    <Grid item xs={12} md={2}>
                      <Typography variant="body1">
                        <strong>Velocidad:</strong><br />{asteroid.velocity} km/s
                      </Typography>
                    </Grid>
                    <Grid item xs={12} md={2}>
                      <Typography variant="body1">
                        <strong>Distancia:</strong><br />{(asteroid.distance_from_earth / 1000000).toFixed(2)}M km
                      </Typography>
                    </Grid>
                    <Grid item xs={12} md={2}>
                      <Typography variant="body1">
                        <strong>Probabilidad:</strong><br />{(asteroid.impact_probability * 100).toFixed(1)}%
                      </Typography>
                    </Grid>
                    <Grid item xs={12} md={2}>
                      <Typography variant="body1">
                        <strong>Nivel de Riesgo:</strong><br />
                        <Chip 
                          label={asteroid.risk_level} 
                          color={
                            asteroid.risk_level === 'HIGH' ? 'error' :
                            asteroid.risk_level === 'MEDIUM' ? 'warning' : 'success'
                          }
                          size="small"
                        />
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

export default RiskAnalysisPage;